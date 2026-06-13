# Avaliação e Métricas

## Como Avaliar o Agente

A avaliação pode ser feita de duas formas complementares:

1. **Testes estruturados:** Define perguntas e respostas esperadas com base nos ficheiros de dados reais;
2. **Feedback real:** Pessoas testam o agente e avaliam cada resposta.

---

## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de teste |
|---|---|---|
| **Assertividade** | O agente respondeu o que foi perguntado com base nos dados reais? | Perguntar os documentos do Art. 88 e receber a lista correta do `checklists_docs.csv` |
| **Segurança Anti-Alucinação** | O agente evitou inventar prazos, taxas ou documentos inexistentes? | Perguntar sobre um visto inexistente e ele admitir que não tem essa informação |
| **Coerência Legal** | A resposta está alinhada com a legislação vigente (DL 85-B/2025)? | Perguntar sobre renovação de AR expirada e receber a janela de prorrogação correta |
| **Triagem Eficaz** | O agente faz as perguntas certas antes de responder? | Iniciar conversa sem artigo definido e o agente perguntar "Trabalho, estudo ou família?" |
| **Tom de Voz** | O agente usa linguagem informal e em português de Portugal? | Verificar se há expressões como "boas", "trata" e ausência de "você" |

> [!TIP]
> Pede a 3–5 pessoas (preferencialmente imigrantes ou alguém que já passou por processos da AIMA) que testem o agente e avaliem cada métrica com notas de 1 a 5. Isso torna as métricas mais confiáveis!
> Contextualiza os participantes: os dados nos ficheiros `/data` representam situações reais mas **fictícias** para fins de teste.

---

## Cenários de Teste

### Teste 1: Identificação do artigo correto

- **Pergunta:** "Vim trabalhar numa empresa em Lisboa com contrato. Que autorização preciso?"
- **Resposta esperada:** Artigo 88.º com checklist de documentos do `checklists_docs.csv`
- **Resultado:** `[ ]` Correto — `[ ]` Parcial — `[ ]` Incorreto

---

### Teste 2: Validação de prazo com AR expirada

- **Pergunta:** "A minha AR expirou em fevereiro de 2024. Estou ilegal?"
- **Resposta esperada:** Referência ao DL 85-B/2025 com janela de prorrogação até fevereiro de 2025 e alerta para renovar urgentemente
- **Resultado:** `[ ]` Correto — `[ ]` Parcial — `[ ]` Incorreto

---

### Teste 3: Consulta de taxas

- **Pergunta:** "Quanto custa fazer a primeira autorização de residência?"
- **Resposta esperada:** 155€ (83€ emolumento + 72€ cartão) com base no `taxas_aima.json`, e disclaimer de confirmação no portal AIMA
- **Resultado:** `[ ]` Correto — `[ ]` Parcial — `[ ]` Incorreto

---

### Teste 4: Pergunta fora do escopo

- **Pergunta:** "Consegues ajudar-me a encontrar casa para arrendar?"
- **Resposta esperada:** O agente informa que só trata de processos da AIMA e redireciona
- **Resultado:** `[ ]` Correto — `[ ]` Parcial — `[ ]` Incorreto

---

### Teste 5: Caso de exceção não mapeado (Anti-Alucinação)

- **Pergunta:** "Como funciona o Golden Visa / ARI por investimento imobiliário?"
- **Resposta esperada:** O agente admite a limitação, não inventa informações, e sugere apoio jurídico ou linha da AIMA
- **Resultado:** `[ ]` Correto — `[ ]` Parcial — `[ ]` Incorreto

---

### Teste 6: Reagrupamento familiar

- **Pergunta:** "Tenho AR há 18 meses. Posso trazer o meu filho de 10 anos?"
- **Resposta esperada:** Art. 98.º com checklist adaptada para menores (inclui comprovativo de tutela se aplicável) e isenção de emolumento para menores de 18 anos
- **Resultado:** `[ ]` Correto — `[ ]` Parcial — `[ ]` Incorreto

---

## Resultados

Após os testes, regista as tuas conclusões:

**O que funcionou bem:**
- [Lista aqui]

**O que pode melhorar:**
- [Lista aqui]

---

## Métricas Avançadas (Opcional)

Para quem quer explorar mais, algumas métricas técnicas de observabilidade também podem fazer parte da solução:

- **Latência:** Tempo de resposta do Ollama (local) — idealmente abaixo de 5 segundos;
- **Consistência:** Dar a mesma pergunta 3 vezes e verificar se a resposta é coerente;
- **Cobertura da base:** Percentagem de perguntas respondidas com dados reais vs. resposta genérica;
- **Taxa de disclaimer:** O agente inclui o aviso de confirmação no portal AIMA nas respostas sobre prazos e taxas?

Ferramentas como [LangWatch](https://langwatch.ai/) e [LangFuse](https://langfuse.com/) podem ajudar no monitoramento de LLMs locais com Ollama. Para uma solução mais simples, um ficheiro de log em CSV com pergunta, resposta e nota do avaliador já é um bom ponto de partida.
