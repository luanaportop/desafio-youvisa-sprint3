# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href="https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# YOUVISA – Plataforma Inteligente de Atendimento Multicanal (Sprint 1)
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
## 📜 Introdução
Este repositório contém a **proposta técnica inicial** da plataforma **YOUVISA** para um **atendimento cognitivo multicanal** (WhatsApp, Telegram, Web) com **NLP**, **RPA**, **visão computacional** para validação documental e **arquitetura cloud** escalável.  
Esta entrega foca em **escopo, arquitetura, fluxos e governança**.

--

## 🎯 Alinhamento de Escopo e Problema
O desafio proposto pela **YOUVISA** nasce de uma necessidade real do mercado: a complexidade e o alto volume de processos relacionados à emissão de vistos e serviços consulares.  
Hoje, boa parte dessas operações depende de atendimentos manuais, troca de e-mails, envio de documentos por diferentes canais e múltiplas etapas de verificação humana.  
Esse modelo é lento, suscetível a erros e oferece uma experiência fragmentada tanto para o cliente quanto para as equipes internas.

A YOUVISA busca modernizar esse cenário por meio de **inteligência cognitiva e automação**, utilizando tecnologias como **Processamento de Linguagem Natural (NLP)**, **RPA (Automação Robótica de Processos)** e **Visão Computacional** para leitura e validação de documentos.  
A meta é criar um ambiente digital que una empatia, segurança e eficiência — um atendimento que entende o usuário, automatiza o que é repetitivo e sabe quando é hora de chamar um humano.

Dentro dessa Sprint 1, o grupo definiu um **escopo inicial** que representa o conceito central da plataforma YOUVISA:

- Desenvolver a **proposta técnica** de uma plataforma multicanal de atendimento inteligente, com integração entre **Telegram**, **WhatsApp** e **Web Chat**;  
- Demonstrar como o **chatbot cognitivo** entende intenções, coleta documentos, e aciona processos automatizados ou encaminha para um atendente humano quando necessário;  
- Estruturar uma **arquitetura técnica escalável**, segura e alinhada à **LGPD**, com armazenamento dos dados em nuvem e controle de acesso por níveis;  
- Apresentar os **fluxos de conversa e componentes técnicos** que sustentam a automação — do reconhecimento de intenção ao fechamento do atendimento.

A solução proposta não tem como objetivo, nesta fase, implementar um código funcional, mas sim **documentar o planejamento e a viabilidade técnica** do sistema.  
Em resumo, o grupo se propõe a responder ao seguinte problema central:

> **“Como criar uma plataforma inteligente de atendimento multicanal, capaz de automatizar a solicitação e verificação de vistos, garantindo segurança, empatia e continuidade da experiência do usuário?”**

--

## 🎯 Objetivos da Sprint 1
O principal objetivo é propor uma **solução inteligente de atendimento multicanal** para a YOUVISA, capaz de unir **inteligência artificial, automação de processos e visão computacional** em uma experiência integrada.  
A plataforma será concebida para atender usuários que precisam de suporte durante processos de **emissão de vistos e serviços consulares**, mantendo a comunicação fluida entre canais digitais e reduzindo a necessidade de intervenção humana em tarefas repetitivas.

A proposta do nosso grupo é criar um **ecossistema cognitivo completo**, no qual diferentes tecnologias trabalham de forma orquestrada:

- **Automação e RPA:** reduzir o retrabalho manual e acelerar processos burocráticos;  
- **Processamento de Linguagem Natural (NLP):** compreender intenções e responder de forma contextual e empática;  
- **Visão Computacional:** validar documentos, passaportes e selfies com segurança e precisão;  
- **Integração Multicanal:** permitir que o atendimento iniciado em um canal (por exemplo, Telegram) possa continuar em outro (como WhatsApp ou Web), sem perda de histórico;  
- **Encaminhamento Inteligente:** acionar um atendente humano sempre que o sistema identificar dúvida, falha de compreensão ou caso sensível;  
- **Segurança e LGPD:** proteger os dados pessoais e sensíveis dos usuários, aplicando criptografia, controle de acesso e políticas de retenção.

Dentro da **Sprint 1**, o foco está na **documentação conceitual e técnica da solução**, demonstrando:

- O **planejamento da arquitetura** (com diagrama e justificativas de tecnologia);  
- Os **fluxos de atendimento** que simulam as interações entre usuário, chatbot, automação e agente humano;  
- A **definição dos dados** que serão coletados, tratados e armazenados com base na LGPD;  
- E o **plano inicial de desenvolvimento**, que guiará as próximas sprints rumo a um MVP funcional.

## ⚙️ Requisitos Técnicos e Funcionais

Os **requisitos técnicos e funcionais** definem os elementos essenciais que sustentam a solução YOUVISA, garantindo que a proposta seja tecnicamente viável, escalável e aderente às boas práticas de desenvolvimento de sistemas inteligentes.

Nesta Sprint 1, o foco é apresentar **como a plataforma seria estruturada** para integrar atendimento multicanal, automação de processos e inteligência cognitiva — sem ainda implementar o código, mas mostrando claramente o planejamento e a coerência entre as partes.

---

### 🔧 Requisitos Técnicos

A arquitetura foi concebida para operar em ambiente **em nuvem**, com componentes **modulares e integrados via APIs**, garantindo escalabilidade e segurança.  
Os principais pilares técnicos incluem:

- **Infraestrutura Cloud:** deploy modular com suporte a serviços de armazenamento, mensageria e monitoramento.  
- **Integração Multicanal:** conectores para WhatsApp, Telegram e Web Chat, unificados por um Gateway Omnicanal.  
- **Motor de NLP:** interpretação de intenções e entidades do usuário por meio de frameworks open source ou cloud.  
- **Orquestração de Processos (RPA):** automação de tarefas repetitivas e integração com sistemas internos.  
- **Visão Computacional:** validação de documentos com OCR e leitura de MRZ, garantindo autenticidade e antifraude.  
- **Segurança e LGPD:** criptografia em trânsito e em repouso, autenticação segura e políticas de retenção de dados.  

Os componentes da solução foram pensados para ser **substituível e escalável**, permitindo evolução futura sem reescrever toda a estrutura.

---

### 💬 Requisitos Funcionais

Os requisitos funcionais definem **como a plataforma YOUVISA deve se comportar na prática** e o que o usuário pode esperar da experiência:

- Oferecer **atendimento integrado entre canais**, mantendo continuidade e histórico da conversa.  
- Permitir que o usuário **solicite vistos, envie documentos e acompanhe protocolos** de forma automatizada.  
- Identificar **intenções e necessidades do usuário** por meio de NLP e direcionar corretamente o fluxo.  
- Realizar **validação documental automatizada**, com suporte a imagens e PDFs.  
- Efetuar **handoff humano** quando necessário, garantindo empatia e resolução eficiente.  
- Registrar e analisar métricas de uso, gerando **insights e relatórios** para melhoria contínua.  
- Manter conformidade com a **LGPD**, respeitando consentimento e direito ao esquecimento.

---

## 🧠 Arquitetura 
A arquitetura contempla:
<p align="center">
<a href=""><img src="assets/Arquitetura_YouVisa.png" alt="Arquitetura" border="0" width=50% height=50%></a>
</p>

A arquitetura representa o fluxo inteligente de atendimento multicanal, onde diferentes pontos de contato do usuário se integram de forma fluida a um núcleo cognitivo capaz de compreender intenções, automatizar processos e garantir continuidade entre canais.

---

### 1. Canais de Entrada  
Os canais representam as **portas de entrada do usuário**.  
Cada interação, seja por **WhatsApp (Cloud API)**, **Telegram Bot API** ou **Web Chat**, é capturada e encaminhada ao **Gateway Omnicanal**, que centraliza e padroniza as mensagens recebidas.  
Essa etapa garante que, independentemente do canal, a experiência do usuário seja uniforme e consistente.

---

### 2. Gateway Omnicanal / Orquestrador  
O gateway funciona como o **maestro da comunicação**.  
Ele recebe as mensagens, aplica verificações iniciais (como autenticação, logs e consentimento LGPD) e as direciona ao motor de processamento de linguagem natural (**NLP**).  
Aqui também se gerenciam **tokens de continuidade**, responsáveis por manter a conversa ativa quando o usuário muda de canal.

---

### 3. Motor NLP (Natural Language Processing)  
O **NLP Engine** interpreta o que o usuário quer dizer.  
Ele identifica **intenções** (por exemplo, solicitar visto, verificar status, reagendar) e **entidades** (país, tipo de visto, data).  
Essa camada pode ser implementada com bibliotecas como **spaCy**, **Rasa NLU** ou serviços cloud, dependendo das políticas de privacidade e da maturidade do projeto.

---

### 4. Policy / Context Manager  
Após o entendimento da intenção, o **gerenciador de contexto** mantém a coerência da conversa.  
Ele lembra o histórico, aplica regras de negócio e define se a próxima ação será automatizada, consultiva ou humana.  
Essa camada é essencial para garantir que o chatbot “pense antes de agir” e responda de acordo com o contexto do usuário.

---

### 5. Regras e Roteamento  
O módulo de **Regras & Roteamento** decide o destino de cada solicitação:  
- Se o usuário precisa enviar documentos, a mensagem é enviada à **Visão Computacional**;  
- Se envolve tarefas repetitivas, vai ao **Orquestrador RPA**;  
- Se requer integração com sistemas internos, segue para **Serviços Internos**.  

Quando a complexidade é alta ou há risco de erro, o sistema faz **handoff humano** para um atendente especializado.

---

### 6. Visão Computacional (OCR / MRZ / Antifraude)  
Essa camada trata a **validação de documentos** enviados pelo usuário.  
Ela realiza OCR (leitura automática), extrai informações da **MRZ do passaporte**, faz comparações de **face match** e aplica regras antifraude.  
Em casos suspeitos, o fluxo é pausado e encaminhado para **revisão manual**, mantendo segurança e conformidade com a **LGPD**.

---

### 7. Orquestrador RPA  
Responsável por **automatizar tarefas repetitivas**, como preenchimento de formulários, criação de protocolos e atualização de status.  
Ao liberar os atendentes dessas atividades, a RPA acelera processos e reduz custos operacionais.

---

### 8. Serviços Internos (Microserviços)  
Agrupa os sistemas corporativos integrados, como banco de dados, CRM e gestão de solicitações.  
Sua arquitetura modular permite que cada serviço funcione de forma independente, facilitando **atualizações** e **escalabilidade**.

---

### 9. Data Lake + Data Warehouse  
Todos os dados processados — logs, intenções, documentos e indicadores — são armazenados de forma segura e criptografada.  
O **Data Lake** guarda os dados brutos para análises posteriores, enquanto o **Data Warehouse** estrutura informações consolidadas para relatórios e insights.  
Essas camadas permitem criar **painéis de monitoramento** e **análises preditivas**, apoiando decisões estratégicas.

---

### 10. Fila / Mensageria  
A fila atua como um **sistema de mensagens assíncronas** (ex.: RabbitMQ, Pub/Sub, SQS), garantindo que os módulos troquem dados com segurança mesmo sob alta demanda.  
Isso evita travamentos, melhora o desempenho e permite que o sistema seja **altamente escalável**.

---

### 11. Handoff Humano
Por fim, o **handoff humano** garante que o usuário nunca fique sem resposta.  
Quando o chatbot não entende a intenção ou detecta uma situação sensível, a conversa é transferida para um atendente real.  
Esse atendente recebe o histórico completo da conversa, mantendo a **continuidade do atendimento** e a **experiência fluida** entre canais.

---

## 💬 Fluxos do Chatbot / NLP

Os fluxos do chatbot representam o **núcleo de interação entre o usuário e a plataforma YOUVISA**.  
Eles traduzem, de forma visual e funcional, **como o sistema entende, responde e age** diante de diferentes intenções do usuário.  
O chatbot atua como o primeiro ponto de contato do usuário e é responsável por identificar o contexto da conversa, compreender a necessidade apresentada e encaminhar a solicitação de forma automatizada ou assistida.

---

### Interpretação e Inteligência de Linguagem

O módulo de **NLP** é o responsável por interpretar o que o usuário diz, reconhecendo **intenções** (ex.: solicitar visto, verificar status, reagendar atendimento) e **entidades** (ex.: país, tipo de visto, data de viagem).  
Essa camada de IA permite que o chatbot compreenda a linguagem humana de forma mais próxima da conversa real, adaptando respostas e fluxos de acordo com o contexto.

Exemplo de intenções reconhecidas:

| Intenção | Exemplo de frase do usuário | Entidades extraídas |
|-----------|-----------------------------|---------------------|
| `solicitar_visto` | “Quero solicitar visto para os EUA.” | país = EUA |
| `status_processo` | “Qual o status do meu protocolo 2025-ABCD?” | protocolo = 2025-ABCD |
| `informar_documentos` | “Quais documentos preciso para o visto de turismo?” | tipo_visto = turismo |
| `falar_com_atendente` | “Quero falar com atendente.” | — |

O NLP identifica essas intenções e envia a resposta adequada para o **módulo de Regras e Roteamento**, que decide a próxima ação do fluxo.

---

### Principais Fluxos de Conversa

1. **Fluxo de Solicitação de Visto**
   - O usuário inicia o atendimento com frases como *“Quero solicitar um visto”*.  
   - O chatbot confirma o país e o tipo de visto desejado.  
   - Solicita o **consentimento LGPD** para processar os dados pessoais.  
   - Após o aceite, o usuário é orientado a **enviar documentos** (ex.: passaporte e selfie).  
   - O módulo de **Visão Computacional** valida os arquivos (OCR, MRZ, face match).  
   - Em caso de sucesso, o sistema gera um **protocolo de solicitação** e confirma o envio.  
   - Se houver suspeita de fraude ou inconsistência, o fluxo é encaminhado ao **atendimento humano**.

2. **Fluxo de Acompanhamento**
   - O usuário digita algo como *“Quero verificar o status do meu protocolo”*.  
   - O chatbot solicita o número do protocolo e busca as informações no sistema.  
   - Caso não encontre, oferece redirecionamento para um atendente humano.

3. **Fluxo de Dúvidas e Handoff Humano**
   - Sempre que o chatbot não compreende a intenção (fallback), ele reformula a pergunta e apresenta opções sugeridas.  
   - Após duas tentativas sem sucesso, o sistema oferece **transferência direta para um agente humano**, preservando o histórico da conversa.

---

### Continuidade entre Canais

A plataforma YOUVISA foi planejada para manter **a continuidade do atendimento**, mesmo quando o usuário muda de canal (por exemplo, começa a conversa pelo Telegram e continua no WhatsApp).  
Isso é feito por meio de um **token de continuidade**, que identifica o usuário e carrega o contexto da sessão de forma segura.  
Dessa forma, o atendimento é realmente multicanal — contínuo, sem repetições.

---

### Benefícios do Fluxo Conversacional

- Redução de tempo e custo por atendimento.  
- Experiência mais natural e empática com o usuário.  
- Automação de etapas burocráticas e repetitivas.  
- Detecção inteligente de situações que exigem contato humano.  
- Melhoria da qualidade do serviço e da satisfação do usuário.

---

## 🔐 Segurança e LGPD
- Princípios de **privacidade por design**, classificação de dados, base legal, retenção e descarte.  
- Criptografia em trânsito e em repouso, **controle de acesso**, auditoria e gestão de segredos.  
- Variáveis de ambiente: `.env.example` (**NUNCA** commitar `.env` real).  
Documento completo: `SECURITY.md`.
## 📈 Métricas & KPIs (inicial)
- **Tempo médio de primeira resposta (FRT)**  
- **Taxa de resolução sem humano (Self-service rate)**  
- **Taxa de handoff** e **SLA** de atendimento humano  
- **Precisão de OCR/NLP** e **taxa de falsos positivos** na validação


## 🔧 Estrutura do repositório
```
assets               # Imagens.
docs/                # Arquitetura, fluxos, segurança, timeline, pitch
nlp/                 # Intents, entidades e exemplos
data/schemas/        # JSON Schemas para registros e eventos
infra/               # IaC esqueleto e decisões
scripts/             # Utilitários (mock/seed)
```
