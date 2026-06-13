import json
import os
import pandas as pd
import requests
import streamlit as st

# =========== CONFIGURAÇÃO ===========
MODELO = "llama3.1"
OLLAMA_URL = "http://localhost:11434/api/generate"

# Caminho base relativo ao ficheiro app.py (em /src)
BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


# =========== CARREGAR DADOS ===========
@st.cache_data
def carregar_base_conhecimento():
    with open(os.path.join(BASE_DIR, "procedimentos_aima.json"), "r", encoding="utf-8") as f:
        procedimentos = json.load(f)

    with open(os.path.join(BASE_DIR, "taxas_aima.json"), "r", encoding="utf-8") as f:
        taxas = json.load(f)

    checklists = pd.read_csv(os.path.join(BASE_DIR, "checklists_docs.csv"))
    prazos = pd.read_csv(os.path.join(BASE_DIR, "prazos_vistos.csv"))

    return procedimentos, taxas, checklists, prazos


# =========== MONTAR CONTEXTO ===========
def construir_contexto(artigo: str, procedimentos: dict, taxas: dict, checklists: pd.DataFrame) -> str:
    """
    Filtra os dados da base de conhecimento pelo artigo identificado
    e monta um bloco de contexto para injetar no system prompt.
    """
    # Procurar o procedimento pelo artigo
    proc = next((p for p in procedimentos["artigos"] if p["artigo"] == artigo), None)

    # Filtrar documentos obrigatórios do CSV
    docs_df = checklists[
        checklists["processo"].str.contains(f"Art. {artigo}", na=False)
    ]
    docs_obrigatorios = docs_df[docs_df["obrigatoriedade"] == "Obrigatório"]["documento"].tolist()
    docs_condicionais = docs_df[docs_df["obrigatoriedade"] == "Condicional"]["documento"].tolist()

    # Filtrar taxa pelo artigo
    taxa = next((t for t in taxas["taxas"] if t["artigo"] == artigo), None)

    if not proc:
        return ""

    contexto = f"""
ARTIGO: {proc['artigo']} — {proc['titulo']}
DESCRIÇÃO: {proc['descricao']}
ELEGIBILIDADE: {'; '.join(proc['elegibilidade'])}

DOCUMENTOS OBRIGATÓRIOS:
{chr(10).join(f'- {d}' for d in docs_obrigatorios)}

DOCUMENTOS CONDICIONAIS (verificar se aplicável):
{chr(10).join(f'- {d}' for d in docs_condicionais) if docs_condicionais else '- (nenhum)'}

PORTAL DE SUBMISSÃO: {proc['portal']} ({proc['url_portal']})
PRAZO DE RESPOSTA AIMA: até {proc['prazo_resposta_aima_dias']} dias úteis

TAXAS:
- Emolumento: {taxa['taxa_emolumento']:.2f}€
- Cartão de residência: {taxa['taxa_cartao']:.2f}€
- TOTAL: {taxa['total']:.2f}€
- Nota: {taxa['notas']}
"""
    return contexto


# =========== SYSTEM PROMPT ===========
def construir_system_prompt(contexto: str = "") -> str:
    base = """És o Descomplica AIMA, um guia prático para imigrantes em Portugal.

OBJETIVO:
Ajudar cidadãos estrangeiros a entender e navegar os processos da AIMA
(autorizações de residência, renovações, reagrupamento familiar e vistos)
de forma clara, sem jargão desnecessário e sempre com base na legislação vigente.

REGRAS:
1. NUNCA inventes documentos, prazos ou taxas — usa apenas os dados fornecidos no CONTEXTO abaixo;
2. Se não souberes o artigo do utilizador, faz triagem: "O teu caso é de trabalho, estudo ou família?";
3. Usa português de Portugal: informal, direto, sem "você";
4. Se um documento faltar, avisa claramente sobre o risco de indeferimento;
5. Sempre que deres prazos ou taxas, acrescenta: "Confirma sempre no portal oficial da AIMA (aima.gov.pt), as regras podem mudar.";
6. Se o caso for uma exceção não mapeada, admite: "Este caso específico foge ao que consigo mapear. Recomendo apoio jurídico ou a linha de apoio da AIMA: 808 202 653.";
7. No final de cada resposta com checklist, pergunta: "Tens todos estes documentos prontos ou precisas de ajuda com algum?".
"""
    if contexto:
        base += f"\n\nCONTEXTO DA BASE DE CONHECIMENTO:\n{contexto}"
    else:
        base += "\n\n[Sem artigo identificado ainda — faz as perguntas de triagem necessárias.]"

    return base


# =========== CHAMAR OLLAMA ===========
def chamar_ollama(mensagens: list, system_prompt: str) -> str:
    """
    Envia o histórico de mensagens e o system prompt para o Ollama
    e devolve a resposta em texto.
    """
    # Formatar o histórico como texto para o prompt
    historico_texto = ""
    for msg in mensagens:
        papel = "Utilizador" if msg["role"] == "user" else "Descomplica AIMA"
        historico_texto += f"\n{papel}: {msg['content']}"

    prompt_completo = f"{system_prompt}\n\nCONVERSA ATÉ AGORA:{historico_texto}\n\nDescomplica AIMA:"

    payload = {
        "model": MODELO,
        "prompt": prompt_completo,
        "stream": False,
        "options": {
            "temperature": 0.3,   # Baixa temperatura para respostas mais factuais
            "num_predict": 1024,
        }
    }

    try:
        resposta = requests.post(OLLAMA_URL, json=payload, timeout=120)
        resposta.raise_for_status()
        return resposta.json().get("response", "").strip()
    except requests.exceptions.ConnectionError:
        return "⚠️ Não consigo ligar ao Ollama. Garante que está a correr com `ollama serve` e que o modelo está instalado (`ollama pull llama3.1`)."
    except requests.exceptions.Timeout:
        return "⚠️ O Ollama demorou demasiado a responder. Tenta novamente."
    except Exception as e:
        return f"⚠️ Erro inesperado: {str(e)}"


# =========== INTERFACE ===========
def main():
    st.set_page_config(
        page_title="Descomplica AIMA",
        page_icon="🇵🇹",
        layout="centered",
    )

    st.title("🇵🇹 Descomplica AIMA")
    st.caption("O teu guia prático para processos de residência em Portugal · Powered by Claudia Machado")
    st.divider()

    # Carregar dados
    procedimentos, taxas, checklists, prazos = carregar_base_conhecimento()

    # --- Sidebar: selecionar artigo manualmente (opcional) ---
    with st.sidebar:
        st.header("⚙️ Configuração")
        artigo_selecionado = st.selectbox(
            "Artigo (opcional — o agente também deteta pela conversa):",
            options=["", "88", "89", "90", "98"],
            format_func=lambda x: {
                "": "Não sei / deixar o agente identificar",
                "88": "Art. 88 — Trabalho Subordinado",
                "89": "Art. 89 — Trabalho Independente",
                "90": "Art. 90 — Estudo",
                "98": "Art. 98 — Reagrupamento Familiar",
            }.get(x, x)
        )
        st.divider()
        st.markdown("📞 **Linha de apoio AIMA:** 808 202 653")
        st.markdown("🔗 [Portal oficial AIMA](https://aima.gov.pt)")
        st.markdown("---")
        if st.button("🗑️ Limpar conversa"):
            st.session_state.mensagens = []
            st.rerun()
        st.markdown(
            """
            <div style="position: fixed; bottom: 20px;">
                <p style="font-size: 0.8rem; color: #888;">Desenvolvido por <a href="https://claudiamachado.me" target="_blank" style="color: #3d9dfe; text-decoration: none;">Claudia Machado</a></p>
            </div>
            """,
            unsafe_allow_html=True
        )


    # --- Inicializar histórico de mensagens ---
    if "mensagens" not in st.session_state:
        st.session_state.mensagens = []

    # --- Mostrar histórico ---
    for msg in st.session_state.mensagens:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # --- Mensagem de boas-vindas (apenas na primeira vez) ---
    if not st.session_state.mensagens:
        with st.chat_message("assistant"):
            boas_vindas = "Boas! Sou o **Descomplica AIMA** 🇵🇹\n\nEstou aqui para te ajudar a navegar pelos processos de residência em Portugal — documentos, prazos, taxas e portais, tudo com base na legislação vigente.\n\nQual é o bicho de sete cabeças que temos de resolver hoje?"
            st.markdown(boas_vindas)

    # --- Input do utilizador ---
    pergunta = st.chat_input("Escreve a tua dúvida aqui...")

    if pergunta:
        # Adicionar mensagem do utilizador ao histórico
        st.session_state.mensagens.append({"role": "user", "content": pergunta})
        with st.chat_message("user"):
            st.markdown(pergunta)

        # Montar contexto com base no artigo selecionado (se houver)
        contexto = ""
        if artigo_selecionado:
            contexto = construir_contexto(artigo_selecionado, procedimentos, taxas, checklists)

        # Construir system prompt com contexto injetado
        system_prompt = construir_system_prompt(contexto)

        # Chamar Ollama
        with st.chat_message("assistant"):
            with st.spinner("A consultar a base de conhecimento..."):
                resposta = chamar_ollama(st.session_state.mensagens, system_prompt)
            st.markdown(resposta)

        # Adicionar resposta ao histórico
        st.session_state.mensagens.append({"role": "assistant", "content": resposta})


if __name__ == "__main__":
    main()
