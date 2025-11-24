# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href="https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# YOUVISA – Plataforma Inteligente de Atendimento Multicanal (Sprint2)
## Beginner Coders
## 👨‍🎓 Integrantes:
- <a href="https://www.linkedin.com/in/luana-porto-pereira-gomes/">Luana Porto Pereira Gomes</a>
- <a href="https://www.linkedin.com/in/luma-x">Luma Oliveira</a>
- <a href="https://www.linkedin.com/in/priscilla-oliveira-023007333/">Priscilla Oliveira </a>
- <a href="https://www.linkedin.com/in/paulobernardesqs?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app">Paulo Bernardes</a>

## 👩‍🏫 Professores:
### Tutor(a)
- <a href="https://www.linkedin.com/in/leonardoorabona/">Leonardo Ruiz</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/in/profandregodoi/">André Godoi</a>

---

## 📘 Introdução

Nesta Sprint 2, começamos a construir a versão funcional da plataforma YOUVISA. O foco agora é integrar chatbot, automação, visão computacional e um painel web para simular um atendimento real de solicitação de visto.

O sistema passa a receber documentos enviados pelo usuário, classificar cada arquivo, validar sua estrutura com OpenCV e criar tarefas automáticas dentro do pipeline. Além disso, usamos NLP para interpretar mensagens no chat e IA Generativa para gerar respostas mais claras e contextualizadas. A interface em React exibe o status do processo em tempo real, enquanto o backend em Python gerencia todo o fluxo.

Esta etapa consolida a arquitetura proposta na Sprint 1 e demonstra, na prática, como a YOUVISA pode automatizar etapas do atendimento consular usando tecnologias de IA e RPA.

---

## 📌 Escopo do Protótipo

Fluxo principal simulado:

1. Usuário inicia atendimento no chatbot pedindo **visto de turismo**;
2. Chatbot explica os documentos necessários:
   - Passaporte
   - Comprovante de residência
   - Comprovante financeiro
   - Formulário de visto YOUVISA
3. Usuário envia os documentos pela interface;
4. Backend:
   - Classifica o tipo de documento;
   - Valida visualmente (OpenCV);
   - Atualiza o status do documento e do processo;
   - Cria/atualiza tarefas internas;
   - Envia e-mails automáticos (confirmação ou correção);
5. Painel em React exibe os arquivos recebidos e o status geral da solicitação.

---

## 🎯 Objetivos

Simular, de ponta a ponta, o fluxo de atendimento da YOUVISA para **solicitação de visto de turismo**, automatizando:

- Recebimento de documentos via chatbot / interface web;
- Organização dos arquivos em classes (passaporte, comprovantes, formulário);
- Criação de tarefas automáticas para cada documento;
- Validação de documentos com visão computacional (OpenCV);
- Geração de respostas inteligentes usando NLP e IA Generativa (simulada ou real);
- Envio automático de e-mails de confirmação ou pedido de reenvio;
- Visualização, em um painel React, dos documentos recebidos e status do processo.

---

## 🧩 Requisitos Técnicos

A Sprint 2 exige a construção de um protótipo funcional que conecte chatbot, automação, IA e visão computacional. Os principais requisitos são:

- **Chatbot funcional** capaz de receber mensagens e permitir upload de documentos.
- **Pipeline de automação em Python** para classificar arquivos, criar tarefas e gerenciar o fluxo.
- **NLP** para identificar intenções e apoiar as respostas do atendimento.
- **IA Generativa** para gerar mensagens personalizadas e contextualizadas.
- **Validação visual com OpenCV**, verificando estrutura/formato básico dos documentos.
- **Envio automático de e-mails** via SMTP, confirmando recebimento ou solicitando correções.
- **Interface web em React + Vite**, exibindo o chatbot e o painel de status dos documentos.
- **Fluxograma completo da arquitetura do pipeline**, documentado em `/docs/sprint2`.

---

## 🏗 Arquitetura Geral da Solução

A Sprint 2 conecta quatro grandes blocos:

### **Frontend – React + Vite**
- Interface do chatbot  
- Upload de documentos  
- Painel com status do processo  
- Comunicação com o backend via API REST  

### **Backend – Python**
- Endpoints para upload, chat e status  
- Pipeline de automação  
- Validação visual com OpenCV  
- NLP e IA Generativa (ou simulação estruturada)  
- Envio de e-mails via SMTP  

### **NLP / IA Generativa**
- Detecta intenções do usuário  
- Monta respostas contextualizadas  

### **Visão Computacional (OpenCV)**
- Validação básica do documento  
- Verificação de estrutura, proporção e formato 

O fluxograma completo está disponível em:  
`docs/sprint2/arquitetura-pipeline-youvisa.png`

---

## 📂 Estrutura das Pastas

```
desafio-youvisa-sprint2/
├── backend/
│   ├── src/
│   │   ├── api/
│   │   ├── pipeline/
│   │   ├── nlp/
│   │   ├── vision/
│   │   ├── email_service/
│   │   ├── models/
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chatbot/
│   │   │   ├── UploadArea/
│   │   │   └── TaskPanel/
│   │   ├── pages/
│   │   └── services/
│   ├── index.html
│   ├── package.json
│   └── vite.config.(js|ts)
├── docs/
│   ├── sprint2/
│   │   ├── escopo-fluxo-principal-youvisa-sprint2.md
│   │   ├── arquitetura-pipeline-youvisa.drawio
│   │   ├── arquitetura-pipeline-youvisa.png
│   │   └── relatorio-tecnico-sprint2.md   
├── assets/
│   ├── prints/
│   └── diagramas/
├── .gitignore
└── README.md

```
---

## ⚙️ Tecnologias Utilizadas
### Frontend
- React
- Vite
- Axios / Fetch API

### Backend
- Python
- Flask ou FastAPI
- OpenCV (visão computacional)
- spaCy / NLTK ou NLP baseado em regras
- smtplib para envio de e-mails

---

## 🚀 Como Rodar o Projeto

### 🔧 Backend

```bash
cd backend/

# criar ambiente virtual
python -m venv .venv

# ativar ambiente virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# instalar dependências
pip install -r requirements.txt

# rodar API
python src/main.py

```

### 💻 Frontend

```bash
cd frontend/

# instalar dependências
npm install

# rodar o projeto em modo desenvolvimento
npm run dev

```
A URL local será exibida automaticamente no terminal pelo Vite.

---

## 📄 Documentação da Sprint 2

- **Escopo do Fluxo Principal:**  
  [`docs/sprint2/escopo-fluxo-principal-youvisa-sprint2.md`](docs/sprint2/escopo-fluxo-principal-youvisa-sprint2.md)

- **Arquitetura do Pipeline (fluxograma):**  
  [`docs/sprint2/arquitetura-pipeline-youvisa.png`](docs/sprint2/arquitetura-pipeline-youvisa.png)

- **Relatório Técnico:**  
  [`docs/sprint2/relatorio-tecnico-sprint2.md`](docs/sprint2/relatorio-tecnico-sprint2.md)





