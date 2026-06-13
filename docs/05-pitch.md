# Pitch (3 minutos)

> [!TIP]
> Podes usar alguns slides para apoiar o teu Pitch e mostrar a solução na prática.

---

## Roteiro Sugerido

### 1. O Problema (30 seg)
> Qual dor do utilizador resolve?

Portugal recebe milhares de imigrantes por ano — mas o sistema de imigração é um labirinto.
Com a extinção do SEF e a criação da AIMA, os portais mudaram, os prazos foram alterados por Decreto-Lei e a informação está dispersa por dezenas de fontes diferentes. O resultado? Imigrantes que submetem documentos errados, perdem agendamentos e, em alguns casos, entram em situação irregular sem perceber que o seu título tinha sido prorrogado automaticamente.

---

### 2. A Solução (1 min)
> Como o agente resolve este problema?

O **Descomplica AIMA** é um assistente de IA local que funciona como um "tuga experiente" sempre disponível. Em vez de obrigar o utilizador a ler PDFs de legislação ou a depender de fóruns desatualizados, o agente:

- **Identifica o artigo correto** para cada situação (trabalho, estudo, família) através de perguntas de triagem simples;
- **Gera checklists personalizadas** com os documentos obrigatórios para cada processo, retiradas diretamente dos ficheiros de dados locais (`checklists_docs.csv`, `procedimentos_aima.json`);
- **Valida prazos e prorrogações** com base no Decreto-Lei n.º 85-B/2025, evitando que o utilizador entre em situação irregular por desconhecimento;
- **Informa as taxas atualizadas** (Portaria n.º 204/2024) antes de qualquer submissão;
- **Nunca inventa informações** — se o caso for uma exceção não mapeada, admite a limitação e sugere apoio jurídico.

A solução corre localmente com **Ollama + Streamlit**, sem enviar dados pessoais para a cloud.

---

### 3. Demonstração (1 min)
> O que será mostrado na gravação de ecrã:

1. Abertura da interface Streamlit no browser (`localhost:8501`);
2. Utilizador escreve: *"Vim trabalhar numa empresa em Lisboa. Tenho visto mas não sei o que fazer a seguir."*;
3. O agente faz triagem e identifica o Artigo 88.º;
4. Resposta com checklist completa de documentos, portal correto e taxa de 155€;
5. Utilizador pergunta: *"A minha AR expirou em março de 2024. Estou ilegal?"*;
6. O agente valida com o DL 85-B/2025 e explica a janela de prorrogação;
7. Utilizador testa um edge case: *"Qual o Golden Visa?"* — o agente admite a limitação sem alucinar.

---

### 4. Diferencial e Impacto (30 seg)
> Por que esta solução é inovadora e qual o impacto?

A maioria dos chatbots de imigração baseia-se em informações genéricas ou em RAG sobre documentos desatualizados. O **Descomplica AIMA** diferencia-se por:

- **Dados estruturados e verificáveis** — qualquer resposta sobre documentos ou taxas tem origem num ficheiro local auditável;
- **Rodar 100% offline** — privacidade garantida, sem dependência de APIs pagas;
- **Design anti-alucinação por arquitetura** — o LLM nunca responde sem contexto injetado da base de conhecimento.

O impacto social é direto: menos processos indeferidos por erro, menos imigrantes em situação irregular por desinformação e mais autonomia para quem mais precisa de clareza num momento de vida já de si complexo.

---

## Checklist do Pitch

- `[ ]` Duração máxima de 3 minutos
- `[ ]` Problema claramente definido
- `[ ]` Solução demonstrada na prática
- `[ ]` Diferencial explicado
- `[ ]` Áudio e vídeo com boa qualidade

---

## Link do Vídeo

> Cola aqui o link do teu pitch (YouTube, Loom, Google Drive, etc.)

[Link do vídeo]
