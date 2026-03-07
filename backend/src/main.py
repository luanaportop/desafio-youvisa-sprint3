@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_extension = file.filename.split(".")[-1].lower()
    is_image = file_extension in ["jpg", "jpeg", "png"]
    
    doc_type = detectar_tipo_documento(file.filename)

    if doc_type == "desconhecido":
        raise HTTPException(status_code=400, detail="Tipo de documento não reconhecido.")

    doc_id = str(uuid.uuid4())
    ensure_uploads_dir()
    
    saved_filename = f"{doc_id}.{file_extension}"
    file_path = os.path.join(UPLOADS_DIR, saved_filename)
    
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    # 1. Validação Técnica (Visão Computacional)
    reason = ""
    if is_image:
        valid, reason = validate_image(file_path)
        # Se a imagem é válida, ela vai para EM_ANALISE (individual) antes de CONCLUIDO
        status_proposto = DocumentStatus.CONCLUIDO if valid else DocumentStatus.PENDENTE_CORRECAO
    else:
        status_proposto = DocumentStatus.PENDENTE_CORRECAO
        reason = "Formato inválido. Use JPG ou PNG."

    # 2. VERIFICAÇÃO DA FSM (Corrigida)
    from process.fsm import validar_transicao
    
    # O status inicial de um novo documento no fluxo é sempre AGUARDANDO_VALIDACAO
    status_base = DocumentStatus.AGUARDANDO_VALIDACAO.value
    
    # Validamos se o documento pode ir de "Aguardando" para o status proposto
    if not validar_transicao(status_base, status_proposto.value):
        # Fallback: Se a FSM barrar o CONCLUIDO direto, tentamos colocar em AGUARDANDO_VALIDACAO
        status_proposto = DocumentStatus.AGUARDANDO_VALIDACAO
        reason = "Documento recebido, aguardando processamento da fila."

    # 3. Criação e Persistência
    document = Document(
        id=doc_id,
        filename=file.filename,
        type=doc_type,
        status=status_proposto,
        created_at=datetime.utcnow().isoformat(),
        validation_reason=reason,
        file_path=file_path
    )

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO documents (id, filename, type, status, created_at, validation_reason, file_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (document.id, document.filename, document.type, document.status.value, 
              document.created_at, document.validation_reason, file_path))
        
        conn.commit()
    finally:
        conn.close()

    return document
