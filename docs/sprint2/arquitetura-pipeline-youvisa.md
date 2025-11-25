# Arquitetura do Pipeline – YOUVISA Sprint 2

A arquitetura da Sprint 2 conecta todos os módulos da plataforma YOUVISA em um fluxo contínuo que simula o atendimento completo do usuário: chatbot → backend → automações → validações → atualização do processo → feedback ao usuário.

Abaixo está a descrição do pipeline para criação do fluxograma.

---

## 1. Início do Fluxo – Chatbot / Frontend

### Responsabilidades:
- Exibir o chat e orientar o usuário.
- Mostrar a lista de documentos necessários.
- Receber arquivos via upload
- Enviar arquivos para o backend através de API REST
- Atualizar a interface com status do processo

### Principais ações:
1. Usuário seleciona “Solicitar visto de turismo”
2. Interface exibe documentos necessários
3. Usuário envia arquivos
4. O frontend chama:
   - `POST /upload`
   - `GET /status`

---

## 2. API Gateway (Backend)

### Responsabilidades:
- Receber requests do frontend
- Organizar rotas e endpoints
- Validar arquivos recebidos
- Passar os arquivos para o pipeline ide automação

### Endpoints principais:
- `POST /upload` → Recebe documentos enviados
- `GET /status` → Retorna estado atual do processo

Após receber o arquivo:

**API → Pipeline de Automação**

---

## 3. Pipeline de Automação (Core do Backend)

O pipeline é responsável por transformar *documentos* em *tarefas* e gerenciar todo o fluxo interno.

### Responsabilidades:
- Criar tarefa para cada documento
- Identificar tipo de documento (classificação)
- Chamar visão computacional
- Atualizar status da tarefa e do processo
- Disparar e-mails automáticos quando necessário

### Sequência de processamento:

1. **Receber arquivo**
Ao receber um arquivo da API, o pipeline cria um objeto interno como:
   ```json
   {
     "nome": "passaporte.jpg",
     "tipo": "desconhecido",
     "status": "em_validacao"
   }

---

## 4. Módulo de Classificação (NLP / IA)

### Responsabilidades:
- Identificar o tipo de documento enviado.
- Auxiliar o pipeline a decidir quais validações aplicar.

### Exemplos de Regras de Classificação:
- Se o nome contém “pass” → **Passaporte**
- Se houver endereço → **Comprovante de Residência**
- Se contiver valores bancários → **Comprovante Financeiro**
- Se o conteúdo lembrar formulários → **Formulário YOUVISA**

### Técnicas utilizadas:
- spaCy 
- NLTK 
- Regras simples 

Classificação retorna um dos tipos:
- `passaporte`
- `comprovante_residencia`
- `comprovante_financeiro`
- `formulario_youvisa`

---

## 5. Módulo de Visão Computacional (OpenCV)

### Validações realizadas:
- Dimensões mínimas do arquivo
- Proporção esperada (portrait/landscape)
- Checagem simulada de regiões-chave (ex.: área superior do passaporte)
- Verificação simples de nitidez / ruído

### Resultado retornado ao pipeline:
- `valido`
- `invalido` + motivo (ex.: “dimensão incorreta”, “documento ilegível”)

Se inválido:
→ pipeline marca tarefa como `pendente_correcao`  
→ Email Service é acionado  
→ Frontend exibe o alerta

---

## 6. Email Service (SMTP)

### Responsabilidades:
- Enviar e-mail de **confirmação de recebimento** de documentos.
- Enviar e-mail de **pendência / correção**, quando o documento for inválido.
- Padronizar os textos de notificação.

### Exemplo de formato de e-mail:
**Assunto:** Atualização YOUVISA – Documento Recebido  
**Mensagem:**  
Seu documento *X* foi processado.  
Status atual: *Y*.  

Pipeline → Email Service → Usuário.

---

## 7. Status Service (Gerenciamento do Processo)

O Status Service gerencia o andamento do processo de solicitação do visto.

### Atualiza:
- O status de cada documento individual.
- O status global da solicitação.

### Estados possíveis:
- **AGUARDANDO_DOCUMENTOS**
- **EM_ANALISE**
- **PENDENTE_CORRECAO**
- **CONCLUIDO**

### Disponibiliza:
O frontend acessa essas informações via: GET/status

O painel e o chatbot usam essas informações para atualizar a interface.

---

## 8. Retorno ao Frontend

Após processar documentos ou mensagens, o backend envia:

- Tipo classificado do documento  
- Status da tarefa  
- Lista completa de documentos enviados  
- Status global da solicitação  
- Mensagens automáticas geradas pelo pipeline/NLP  

O frontend então atualiza:

- Chatbot (conversa)  
- Painel do usuário (lista e status dos documentos)  

Isto garante que o usuário acompanha **em tempo real** o andamento do seu processo.

---

## 9. Finalização do Processo

O processo é concluído quando:

- Todos os documentos obrigatórios foram **recebidos**, e  
- Todos passaram nas validações.

Quando isso ocorre:
- O estado global muda para **CONCLUIDO**.
- O chatbot exibe mensagem final:
  > “Todos os documentos foram validados com sucesso.”
- O painel exibe o status final.

---

## 10. Mapa Visual para o Fluxograma (Draw.io)

### 🔹 Bloco 1 — Frontend (Chatbot + Painel)
- Chatbot 
- Componente de Upload
- Painel de Status

**Saídas do Frontend → API**
- GET /health
- POST /upload
- GET /status

---

### 🔹 Bloco 2 — API Gateway (Backend)
- Recebe uploads
- Retorna status
- Encaminha documentos ao pipeline

**API → Pipeline de Automação**

---

### 🔹 Bloco 3 — Pipeline de Automação
- Cria tarefas
- Orquestra validações
- Atualiza status

**Pipeline chama:**
1. Classificação (NLP)
2. Visão Computacional (OpenCV)
3. Email Service
4. Status Service

---

### 🔹 Bloco 4 — Módulo de Classificação (NLP/IA)
- Regras simples
- Identificação do tipo de documento
**Devolve tipo → Pipeline**

---

### 🔹 Bloco 5 — Validação Visual (OpenCV)
- Proporções
- Dimensões mínimas
- Regiões básicas
- Nitidez

**Retorno → Pipeline (válido ou inválido)**

---

### 🔹 Bloco 6 — Email Service
- Confirma recebimento
- Solicita correção se inválido

---

### 🔹 Bloco 7 — Status Service
- Mantém o estado global da solicitação
- Controla:
  - AGUARDANDO_DOCUMENTOS
  - EM_ANALISE
  - PENDENTE_CORRECAO
  - CONCLUIDO

**Retorno → Frontend via GET /status**

---

### 🔹 Bloco 8 — Retorno ao Frontend
- Atualização do painel
- Atualização do chatbot
- Exibição do progresso do processo

---

## 9. Encerramento

Este documento descreve todos os módulos, responsabilidades, fluxos e interações necessárias para a Sprint 2.  
O fluxograma pode ser resumido em:

**Usuário → Frontend → API → Pipeline → NPL/Visão → E-mail → Status → Frontend**

---



