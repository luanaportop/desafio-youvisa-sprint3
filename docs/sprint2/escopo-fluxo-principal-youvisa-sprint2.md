# Escopo e Fluxo Principal – Sprint 2 YOUVISA

## 1. Contexto do Atendimento

Nesta Sprint 2, a YOUVISA foca em simular o fluxo de atendimento para **solicitação de visto de turismo**, do ponto de vista do usuário e do sistema. O objetivo é mostrar como documentos enviados pelo usuário viram tarefas automáticas dentro da plataforma.

O fluxo acontece em três camadas principais:
- **Chatbot / Frontend**: interação com o usuário e envio de documentos.
- **Backend / Pipeline de automação**: classificação, validação e criação de tarefas.
- **Serviços de apoio**: visão computacional, NLP/IA e envio de e-mails.

---

## 2. Personagem e Cenário

- **Personagem**: Usuário final da YOUVISA solicitando visto de turismo.
- **Canal**: Chatbot web (interface React).
- **Objetivo do usuário**: Enviar documentos necessários e acompanhar o status do processo.

---

## 3. Documentos Envolvidos no Fluxo

O usuário deve enviar, no mínimo, os seguintes documentos:

1. **Passaporte**
2. **Comprovante de residência**
3. **Comprovante financeiro**
4. **Formulário YOUVISA** (simulando um formulário consular)

Cada documento enviado será tratado como uma **tarefa** dentro do pipeline.

---

## 4. Fluxo Principal do Usuário

1. O usuário acessa o chatbot e seleciona a opção **“Solicitar visto de turismo”**.
2. O chatbot explica quais documentos são necessários e a ordem sugerida de envio.
3. O usuário envia cada documento (upload pela interface).
4. A cada upload:
   - O frontend envia o arquivo para o backend.
   - O backend registra o documento e o vincula ao processo do usuário.
   - O pipeline classifica o tipo de documento.
   - A visão computacional valida estrutura/formato básico (OpenCV).
   - O status da tarefa é atualizado (ex.: “aguardando análise”, “válido”, “inválido”).
5. Se o documento for **válido**:
   - O sistema marca a tarefa como concluída.
   - O painel React atualiza o status para o usuário.
6. Se o documento for **inválido**:
   - O sistema marca a tarefa como “pendente correção”.
   - Um e-mail automático é enviado orientando o usuário a reenviar o documento.
7. Quando todos os documentos obrigatórios estiverem **válidos**:
   - O processo é marcado como **“concluído”**.
   - O painel mostra o status final e o chatbot envia uma mensagem de encerramento do atendimento.

---

## 5. Estados do Processo

Durante o fluxo, o processo do usuário pode assumir os seguintes estados:

- **AGUARDANDO_DOCUMENTOS** – usuário ainda não enviou todos os arquivos.
- **EM_ANALISE** – documentos recebidos, em validação.
- **PENDENTE_CORRECAO** – algum documento foi rejeitado e precisa ser reenviado.
- **CONCLUIDO** – todos os documentos obrigatórios foram validados com sucesso.

---

## 6. Papel dos Componentes da Plataforma

- **Chatbot (frontend)**  
  - Guia o usuário no passo a passo.
  - Recebe mensagens e arquivos.
  - Exibe status do processo em tempo (quase) real.

- **Backend (pipeline de automação)**  
  - Recebe e armazena os documentos.
  - Classifica o tipo de cada arquivo.
  - Atualiza tarefas e estados do processo.
  - Integra com visão computacional, NLP/IA e e-mail.

- **NLP / IA Generativa**  
  - Interpreta intenções básicas do usuário (ex.: dúvidas sobre documentos).
  - Gera respostas mais claras e humanizadas no chat.

- **Visão Computacional (OpenCV)**  
  - Faz validações simples de layout/estrutura dos documentos (ex.: proporções, presença de áreas principais).

- **Serviço de E-mail (SMTP)**  
  - Envia confirmação de recebimento.
  - Envia pedido de correção quando necessário.

---

## 7. Escopo da Sprint 2 (Limitações)

- Não serão implementadas regras reais de consulado ou análise jurídica.
- O foco é simular o fluxo de automação, não a decisão real do visto.
- As validações visuais serão simplificadas (checagens básicas, não OCR completo).
- O modelo de NLP/IA pode ser real ou simulado com regras, desde que o fluxo esteja funcional.
