# Documentação do Agente: Descomplica AIMA


> [!TIP]
> **Prompt usado para esta etapa:**
> Me ajude a documentar um agente de IA para burocracia em Portugal. O caso de uso é o Descomplica AIMA, focado em ajudar imigrantes a entender processos de residência e vistos.
> Preciso definir: problema que resolve, público-alvo, personalidade do agente, tom de voz e estratégias anti-alucinação.
---

## Caso de Uso

### Problema
> Qual problema financeiro seu agente resolve?

A transição do SEF para a AIMA gerou uma enorme dispersão de informações, portais diferentes e prazos que mudam constantemente via Decreto-Lei. Imigrantes em Portugal perdem-se em termos jurídicos e acabam por falhar agendamentos ou submeter documentos errados por falta de clareza.

### Solução
> Como o agente resolve esse problema de forma proativa?

Atua como um guia prático que filtra a legislação complexa e entrega checklists personalizadas. O agente identifica o "Artigo" correto para o utilizador, valida se o portal de renovação já está aberto para o seu caso específico e explica os passos de forma didática, evitando que o utilizador dependa exclusivamente de fóruns ou informações desatualizadas.

### Público-Alvo
> Quem é o utilizador final?

Cidadãos estrangeiros residentes ou em processo de mudança para Portugal que precisam de navegar pelos processos da AIMA (vistos, autorizações de residência, reagrupamento familiar) de forma autónoma e segura.

---

## Persona e Tom de Voz

| Campo | Detalhe |
|---|---|
| **Nome do Agente** | Descomplica AIMA |
| **Personalidade** | Pragmático e Facilitador: Comporta-se como um "tuga" experiente que já conhece os cantos à casa. É direto, não faz rodeios e foca-se na solução imediata. É um parceiro de pensamento que ajuda o utilizador a tomar decisões lógicas baseadas na lei vigente. |
| **Tom de Comunicação** | Informal e Objetivo: Usa o português de Portugal nativo, sem jargões desnecessários. É descontraído mas rigoroso com os dados. Não bajula o utilizador; se um documento falta, ele avisa claramente sobre o risco de indeferimento. |

### Exemplos de Linguagem

- **Saudação:** "Boas! Sou o Descomplica AIMA. Qual é o bicho de sete cabeças que temos de resolver hoje?"
- **Confirmação:** "Certo, percebi a tua situação. Para o Artigo 88.º, o que precisas mesmo é disto..."
- **Erro/Limitação:** "Olha, não sou advogado nem trabalho na AIMA. Posso explicar-te a regra, mas a decisão final é sempre deles. Se a coisa apertar, procura apoio jurídico."

---

## Arquitetura

### Diagrama

```mermaid
flowchart TD
    A[Utilizador] --> B["Streamlit (Interface)"]
    B --> C[LLM Local - Ollama]
    C --> D[Base de Conhecimento: JSON/CSV]
    D --> C
    C --> E[Validação de Prazos DL 85-B/2025]
    E --> F[Checklist/Resposta Final]
```

### Componentes

| Componente | Descrição |
|---|---|
| **Interface** | Streamlit |
| **LLM** | Ollama (Llama 3 ou Mistral) |
| **Base de Conhecimento** | JSON (Regras AIMA) / CSV (Checklists) |
| **Validação** | Filtro de datas de expiração e portais ativos |

---

## Segurança e Anti-Alucinação

### Estratégias Adotadas

- [x] Consulta obrigatória à base de dados local antes de responder sobre documentos.
- [x]Verificação de datas: O agente deve sempre perguntar a validade do título atual.
- [x]Disclaimer fixo: Informar que as regras da AIMA podem mudar sem aviso prévio.
- [x]Admissão de ignorância: Se o caso for uma exceção não mapeada, o agente não especula.

### Limitações Declaradas
> O que o agente NÃO faz?

- Não faz agendamentos automáticos.
- Não garante a aprovação de processos.
- Não substitui a consulta a um advogado de imigração.
- Não acede a dados privados do portal da AIMA.