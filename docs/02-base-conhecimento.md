# Estratégia da Base de Conhecimento: Descomplica AIMA

---

## 1. Fontes de Dados

Para garantir que a IA não alucina com regras antigas do SEF, a base de conhecimento foi construída exclusivamente a partir de:

- **Portal Oficial AIMA:** [aima.gov.pt](https://aima.gov.pt) — procedimentos e FAQs.
- **Diário da República:** Decreto-Lei n.º 85-B/2025 (prorrogação de validade).
- **Portaria n.º 204/2024:** Tabela de taxas e emolumentos atualizada.

---

## 2. Organização dos Ficheiros (`/data`)

A informação está segmentada para facilitar a recuperação (RAG):

| Ficheiro | Formato | Conteúdo |
|---|---|---|
| `procedimentos_aima.json` | JSON | Artigos 88, 89, 90 e 98 com elegibilidade, documentos obrigatórios e portais de submissão. |
| `checklists_docs.csv` | CSV | Mapeamento `[Processo]` → `[Documento]` → `[Obrigatoriedade]` com notas por documento. |
| `prazos_vistos.csv` | CSV | Correspondência entre data de expiração original e nova validade legal (DL 85-B/2025), com janelas de renovação e alertas de situação irregular. |
| `taxas_aima.json` | JSON | Emolumentos por tipo de título (1.ª concessão e renovação), taxa do cartão e multas por permanência irregular. |

---

## 3. Lógica de Recuperação e Filtros

O agente segue uma hierarquia de decisão para evitar respostas genéricas:

1. **Filtro de Validade:** Antes de sugerir um portal, o agente cruza a data de expiração do utilizador com o ficheiro `prazos_vistos.csv`.
2. **Identificação do Artigo:** Se o utilizador não souber o seu artigo, o agente faz perguntas de triagem baseadas no `procedimentos_aima.json` (Trabalho? Família? Estudo?).
3. **Prioridade de Portais:**
   - Títulos expirados (janela de renovação) → **Portal de Renovações**
   - Novos pedidos ou reagrupamentos → **Portal de Serviços**

---

## 4. Manutenção e Atualização

- **Frequência:** Revisão quinzenal dos anúncios na secção "Notícias" do portal AIMA.
- **Tratamento de Exceções:** Casos que não constam na base (ex: vistos de investidor ARI ou situações humanitárias complexas) são sinalizados para que o agente admita a limitação e sugira contacto direto com a linha de apoio da AIMA.

---

## 5. Estratégia de Integração

### Como os dados são carregados?

O carregamento é feito **uma única vez no arranque da aplicação** (`@st.cache_data`) para evitar leituras repetidas do disco a cada mensagem do utilizador.

```python
import json
import pandas as pd
import streamlit as st

@st.cache_data
def carregar_base_conhecimento():
    with open("data/procedimentos_aima.json", "r", encoding="utf-8") as f:
        procedimentos = json.load(f)

    with open("data/taxas_aima.json", "r", encoding="utf-8") as f:
        taxas = json.load(f)

    checklists = pd.read_csv("data/checklists_docs.csv")
    prazos    = pd.read_csv("data/prazos_vistos.csv")

    return procedimentos, taxas, checklists, prazos
```

> [!TIP]
> `@st.cache_data` guarda os dados em memória entre interações. Os ficheiros só são relidos se forem modificados ou se a sessão for reiniciada.

---

### Como o agente acede à base de conhecimento?

O agente **não faz pesquisa vetorial (RAG completo)**. Em vez disso, segue uma lógica de recuperação **determinista por filtros**, mais fiável para dados estruturados e legislação:

```
Mensagem do utilizador
        │
        ▼
┌─────────────────────────┐
│  1. Classificar intenção│  → "renovar" / "novo pedido" / "taxas" / "documentos"
└────────────┬────────────┘
             │
        ▼
┌─────────────────────────┐
│  2. Identificar artigo  │  → Perguntas de triagem → Art. 88 / 89 / 90 / 98
└────────────┬────────────┘
             │
        ▼
┌─────────────────────────┐
│  3. Filtrar dados reais │  → Busca no JSON/CSV correspondente
└────────────┬────────────┘
             │
        ▼
┌─────────────────────────┐
│  4. Injetar no prompt   │  → Dados reais passados ao LLM como contexto
└────────────┬────────────┘
             │
        ▼
   Resposta do LLM (Ollama)
```

### Injeção de contexto no prompt do LLM

Os dados filtrados são convertidos para texto e incluídos no **system prompt** antes de cada resposta:

```python
def construir_contexto(artigo: str, procedimentos: dict, checklists: pd.DataFrame) -> str:
    # Filtrar procedimento pelo artigo
    proc = next((p for p in procedimentos["artigos"] if p["artigo"] == artigo), None)
    docs = checklists[checklists["processo"].str.contains(f"Art. {artigo}")]

    contexto = f"""
    ARTIGO: {proc['artigo']} — {proc['titulo']}
    ELEGIBILIDADE: {', '.join(proc['elegibilidade'])}
    DOCUMENTOS OBRIGATÓRIOS:
    {docs[docs['obrigatoriedade'] == 'Obrigatório']['documento'].to_string(index=False)}
    PORTAL: {proc['portal']}
    """
    return contexto
```

> [!IMPORTANT]
> O LLM **nunca responde sem contexto injetado** sobre documentos ou prazos.
> Se o artigo não for identificado, o agente faz perguntas de triagem antes de consultar os ficheiros.