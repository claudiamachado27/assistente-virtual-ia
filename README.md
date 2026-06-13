# 🇵🇹 Descomplica AIMA

Um assistente virtual alimentado por Inteligência Artificial (Ollama / Llama 3.1) desenhado para ajudar os cidadãos estrangeiros a navegar pelos processos de autorização de residência da AIMA em Portugal (Artigo 88, 89, 90 e 98).

## 🚀 Funcionalidades
- **Triagem Inteligente**: O agente é capaz de direcionar o utilizador para o artigo correto.
- **Consultas Personalizadas**: Informa sobre documentos obrigatórios e condicionais para cada tipo de processo.
- **Prazos e Taxas**: Tabela atualizada de valores e estimativas de prazos.
- **Sem Alucinações (RAG-like)**: Utiliza uma estratégia determinística para consultar os ficheiros locais e injetá-los no contexto do agente.

## 🛠️ Tecnologias Utilizadas
- **[Python 3.14](https://www.python.org/)**
- **[Streamlit](https://streamlit.io/)**: Para a interface de conversação gráfica.
- **[Ollama](https://ollama.com/)** (Modelo Llama 3.1): Motor do Large Language Model a correr localmente.
- **Pandas**: Para a manipulação dos dados CSV da base de conhecimento.

## 📁 Estrutura do Projeto

```
assistente-virtual-ia/
│
├── data/                    # Base de Conhecimento (JSON e CSV)
│   ├── checklists_docs.csv
│   ├── prazos_vistos.csv
│   ├── procedimentos_aima.json
│   └── taxas_aima.json
│
├── docs/                    # Documentação do Agente e Projeto
│   ├── 01-documentacao-agente.md
│   ├── 02-base-conhecimento.md
│   ├── 03-prompts.md
│   ├── 04-metricas.md
│   └── 05-pitch.md
│
├── src/
│   └── app.py               # Aplicação principal (Streamlit)
│
├── requirements.txt         # Dependências de Python
└── README.md                # Este ficheiro
```

## ⚙️ Como Correr Localmente

### 1. Pré-requisitos
- Python instalado na máquina.
- [Ollama](https://ollama.com/) instalado e a correr em `localhost`.
- O modelo Llama 3.1 descarregado no Ollama (`ollama pull llama3.1`).

### 2. Instalação
No terminal, clona o repositório e entra na pasta:
```bash
git clone https://github.com/claudiamachado27/assistente-virtual-ia.git
cd assistente-virtual-ia
```

Cria um ambiente virtual e instala as dependências:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Iniciar a Aplicação
Ainda com o ambiente virtual ativado, executa o Streamlit:
```bash
streamlit run src/app.py
```
A aplicação deverá abrir automaticamente no teu navegador (tipicamente em http://localhost:8501).

Desenvolvido por Claudia Machado