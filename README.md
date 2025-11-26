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

Este repositório reúne o protótipo funcional desenvolvido para a Sprint 2 do Enterprise Challenge – YOUVISA, cuja proposta é criar um sistema de análise inicial de documentos para solicitação de visto de turismo.

O projeto foi pensado como um MVP realista, simulando o comportamento de sistemas modernos que usam:
- NLP (Processamento de Linguagem Natural)
- IA Generativa (simulada de forma guiada)
- Pipeline inteligente de decisão
- RPA / Agente virtual
- Validação automática de documentos
- Chatbot orientado ao contexto do usuário

Mesmo sem utilizar modelos generativos reais (como GPT, Claude, Gemini ou LLaMA), implementamos fielmente os conceitos ensinados pela FIAP, como:
- interpretação de intenção,
- aprendizado em contexto,
- raciocínio baseado no estado atual,
- respostas dinâmicas,
- pipeline de processamento,
- simulação de agente de e-mail,
- simulação de generative prompting.

---

## 🎯 Objetivo do Projeto

Criar um sistema funcional e demonstrável que permita:

- o envio de documentos obrigatórios (passaporte, residência, financeiro e formulário);
- validação automática do formato e classificação inteligente;
- exibição do status do processo em tempo real;
- simulação de envio de e-mail após uploads;
- chatbot inteligente com comportamento semelhante a IA Generativa;
- interface moderna, simples e orientada ao usuário;
- fluxo de decisão inspirado em pipelines reais de IA e RPA.

## 📌 Escopo do Protótipo

### Fluxo principal simulado:
- Upload de arquivos JPEG/PNG, com bloqueio de PDF;
- Classificação automática baseada em NLP simbólico;
- Identificação dos documentos faltantes;
- Tratamento automático de pendências (arquivo inválido ou errado);
- Simulação de IA Generativa para respostas do chatbot YOUVISA;
- Chatbot com raciocínio contextual, baseado no status do processo;
- Pipeline inspirado em arquiteturas de agentes LLM;
- Simulação de RPA para envio automático de e-mails;
- UI refinada com comportamento dinâmico e respostas condicionadas.

---

## 🧩 Simulações Inteligentes (NLP, IA Generativa, RPA)

### NLP (Processamento de Linguagem Natural)
O projeto utiliza NLP simbólico, totalmente integrado ao backend e ao chatbot, para:
- interpretar mensagens como:
“qual documento falta?”,
“posso enviar PDF?”,
“status do processo?”,
“enviei o documento”.
- classificar documentos pelo nome do arquivo usando dicionário semântico.

O classificador identifica automaticamente:
- Passaporte
- Comprovante de residência
- Comprovante financeiro
- Formulário YOUVISA

---

### 🤖 IA Generativa (Simulada)
Embora não utilize modelos de linguagem reais (como OpenAI ou Gemini), o chatbot YOUVISA implementa comportamento generativo simulado, baseado nos conceitos ensinados pela FIAP:
- respostas adaptadas ao contexto do processo
- raciocínio condicional baseado no status_global
- mensagens personalizadas
- explicações estruturadas
- interação humanizada
- respostas dinâmicas, não fixas
Exemplo:
Se faltar somente o comprovante financeiro, o chatbot responde especificamente sobre esse documento.
Se tudo estiver correto, ele celebra com o usuário.

---

### 🟦 RPA (Automação Robótica de Processos – Simulada)
Implementamos um agente automático que:
- recebe o documento
- valida formato
- classifica
- gera status
- dispara um e-mail automático (simulado)
Essa função imita o comportamento de um robô corporativo real, como os vistos em pipelines de RPA.

---

## 🏗 Arquitetura Geral da Solução

Usuário
   ↓
Frontend (React + TS)
   ↓ API calls
Backend (FastAPI)
   ↓
Pipeline de Processamento:
   • validação de imagem
   • NLP simbólico
   • classificação
   • decisão do status
   • simulação de e-mail
   ↓
Status atualizado em tempo real

O fluxograma completo está disponível em:  
`docs/sprint2/arquitetura-pipeline-youvisa.png`

---

## 📂 Estrutura das Pastas

```
DESAFIO-YOUVISA-SPRINT2/
│── assets/
│   ├── diagramas/
│   ├── prints/
│   └── logo-fiap.png
│
│── backend/
│   ├── venv/
│   ├── src/
│   │   ├── api/
│   │   │   └── router.py
│   │   ├── email_service/
│   │   │   └── sender.py
│   │   ├── models/
│   │   │   ├── document.py
│   │   │   └── models.py
│   │   ├── nlp/
│   │   │   └── classifier.py
│   │   ├── pipeline/
│   │   │   ├── pipeline.py
│   │   │   ├── processor.py
│   │   │   └── repository.py
│   │   ├── vision/
│   │   │   └── validator.py
│   │   └── main.py
│   │   ├── uploads/
│   ├── requirements.txt
│   
│── frontend/
│   └── src/
│   │   ├── assets/
│   |   ├── components/
|   |   |   ├── chatbot.tsx
│   │   │   ├── statuspanel.tsx
│   │   │   └── uploadarea.tsx
│   |   ├── services/
│   |   |   └── api.ts
│── docs/
│   ├── sprint2/
|   |   ├── relatório-técnico
│   |   └── escopo-fluxo-principal-youvisa-sprint2.md
│
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
- FastAPI
- OpenCV (visão computacional)
- spaCy / NLTK ou NLP baseado em regras
- smtplib para envio de e-mails

---

## 🚀 Como Executar o Backend (FastAPI)
Pré-requisitos
- Python 3.10+
- FastAPI / Uvicorn (instalados automaticamente via requirements.txt)


# 1- Ativar o ambiente virtual
Abra o terminal na raiz do projeto:
cd backend/

Windows (PowerShell)
.\venv\Scripts\activate

Linux/macOS
source venv/bin/activate

# 2- Instalar dependências (se necessário)
pip install -r requirements.txt

# 3- Entrar na pasta src
cd src

# 4- Rodar o servidor FastAPI
uvicorn main:app --reload

# 5- Acessar a API
🔹 Swagger UI (Interface de testes)

http://127.0.0.1:8000/docs

🔹 OpenAPI JSON

http://127.0.0.1:8000/openapi.json


## 🔌 Endpoints Disponíveis

GET /health: Verifica se o servidor está ativo.

POST /upload; Recebe documento e envia para o pipeline.

GET /status: Retorna status global da solicitação + documentos enviados.

---

### 💻 Como Executar o Frontend

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





