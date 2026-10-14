# Klike Data Science Challenge

Desafio técnico de Ciência de Dados desenvolvido como parte do processo seletivo para estágio de férias da Klike.ai.

O projeto tem como objetivo analisar dados de campanhas publicitárias em vídeo, identificar padrões de desempenho, desenvolver um modelo preditivo para o `klike_score` e construir um sistema de recomendações para otimização de criativos.

## Como executar o projeto

### Pré-requisitos

- Python 3.10 ou superior
- Git
- Ambiente virtual Python (`env`)

### Configuração do ambiente

**1. Clone o repositório**

```bash
git clone <URL_DO_REPOSITORIO>
cd klike-ds-challenge-lauradeoli
```

**2. Crie um ambiente virtual**

```bash
python -m venv env
```

**3. Ative o ambiente virtual**

No Windows (PowerShell):

```powershell
.\env\Scripts\Activate.ps1
```

No Linux/macOS:

```bash
source env/bin/activate
```

**4. Instale as dependências**

```bash
python -m pip install -r requirements.txt
```

**5. Execute o Jupyter Notebook**

```bash
jupyter notebook
```

Abra o arquivo `notebooks/01_eda.ipynb` para iniciar a exploração dos dados.

## Estrutura do projeto

```text
klike-data-science-challenge/
├── data/                 # Base de dados
├── notebooks/            # Análise exploratória e modelagem
├── src/                  # Sistema de recomendações
├── .gitignore
├── README.md
└── requirements.txt
```

## Status do projeto

🚧 Em desenvolvimento — parte 2 - modelagem.

## 1. Análise Exploratória dos Dados (EDA)

### 1.1 Qual o perfil geral dos dados?

O dataset contém 500 registros e 26 variáveis, abrangendo características dos criativos, informações das campanhas e métricas de performance.

Durante a exploração, foram identificados valores ausentes em sete variáveis, distribuições numéricas predominantemente assimétricas à direita e observações extremas, especialmente nas métricas de alcance e retorno financeiro. Não foram encontradas linhas completamente duplicadas.

**Decisões de tratamento:** Considerando o tamanho reduzido da base, optei por preservar os registros durante a EDA para evitar a perda de campanhas potencialmente relevantes. Valores ausentes poderão ser tratados conforme o tipo de variável e os requisitos dos modelos, enquanto outliers deverão ser investigados antes de possíveis correções ou exclusões.

Também foram identificadas inconsistências pontuais no CPC, que mereceriam investigação adicional em uma etapa de limpeza dos dados.

### 1.2 Quais atributos dos criativos mais se relacionam com boas métricas de performance?

Inicialmente, utilizei o CTR como referência para investigar características associadas à atração de cliques. Entretanto, percebi que essa métrica isoladamente não seria suficiente para avaliar campanhas com diferentes objetivos. Por isso, ampliei a investigação para incluir CPC, ROAS, conversões, receita, engajamento e tempo médio de visualização.

As principais associações identificadas foram:

- **Hook e rosto humano:** associados a maiores medianas de CTR, engajamento, conversões e tempo de visualização, mas a menores medianas de ROAS.
- **CTA:** associado a maiores medianas de conversões, receita e ROAS.
- **Densidade de texto:** criativos com alta densidade apresentaram menores medianas de CTR, ROAS, conversões e receita em comparação com os de baixa densidade.

A análise de correlação de Spearman não identificou associações monotônicas fortes entre os atributos numéricos dos criativos e as métricas de performance avaliadas.

Esses resultados demonstram que características associadas a mais cliques ou interações não necessariamente apresentam melhores resultados financeiros.

### 1.3 Existem padrões diferentes por plataforma? O que funciona no TikTok funciona no LinkedIn?

Sim, foram identificadas diferenças nos padrões de performance entre Meta, TikTok e LinkedIn.

A presença de hook esteve associada a CTR mediano superior nas três plataformas. Entretanto, a relação com o ROAS foi distinta:

- **TikTok:** ROAS mediano de 2,20x sem hook e 2,99x com hook.
- **Meta:** ROAS mediano de 1,81x sem hook e 1,32x com hook.
- **LinkedIn:** ROAS mediano de 0,53x em ambos os grupos.

Além disso, criativos com alta densidade de texto apresentaram CTR mediano inferior nas três plataformas, com diferença particularmente expressiva no Meta.

Portanto, embora algumas associações se repitam entre plataformas, outras variam conforme o contexto. Isso reforça a necessidade de considerar a plataforma, o objetivo e a métrica de interesse antes de formular recomendações de otimização.

### 1.4 Visualizações para o time de marketing

Foram selecionadas três visualizações para comunicar os principais insights da EDA de maneira acessível, priorizando descobertas com possíveis aplicações na otimização de criativos.

**Gráfico 1 — CTR mediano por presença de hook e plataforma**

![Gráfico 1 — CTR mediano por presença de hook e plataforma](images\CTR-hook-plataforma-1.png)


A presença de hook está associada a CTR mediano superior nas três plataformas, destacando sua possível relevância para campanhas que buscam atrair cliques.

**Gráfico 2 — ROAS mediano por presença de hook e plataforma**

![Gráfico 2 — ROAS mediano por presença de hook e plataforma](images\ROAS-hook-plataforma-2.png)

A associação entre hook e retorno financeiro varia conforme a plataforma. O resultado mostra por que não devemos utilizar apenas o CTR como referência para avaliar a performance.

**Gráfico 3 — CTR mediano por densidade de texto e plataforma**

![Gráfico 3 — CTR mediano por densidade de texto e plataforma](images\CTR-texto-plataforma-3.png)

Criativos com alta densidade de texto apresentam CTR mediano inferior aos demais grupos nas três plataformas, sugerindo uma possível oportunidade de otimização.

### Limitações da análise

Os resultados apresentados representam associações observadas nos dados e não permitem estabelecer causalidade. Além disso, métricas absolutas, como receita e conversões, podem ser influenciadas pela escala das campanhas.

Essas limitações deverão ser consideradas na construção do sistema de recomendações, evitando apresentar diferenças estatísticas observadas como melhorias garantidas.

## 2. Modelagem Preditiva

### 2.1 Quais features foram selecionadas e por quê?

O objetivo da modelagem foi prever o `klike_score` utilizando informações disponíveis **antes da veiculação da campanha**. Essa escolha considera um cenário em que o anunciante deseja avaliar e melhorar seu criativo antes de publicá-lo.

Foram selecionadas 13 features, divididas em dois grupos:

- **Contexto da campanha:** plataforma, categoria, objetivo, faixa etária do público-alvo e retargeting.
- **Características do criativo:** duração, formato, presença de legendas, CTA, hook, rosto humano, densidade de texto e proporção entre música e voz.

Métricas como CTR, ROAS e conversões foram excluídas por dependerem da veiculação da campanha. Utilizá-las tornaria o modelo incompatível com o cenário de uso escolhido.

**Pré-processamento:** foram utilizados imputação de valores ausentes, One-Hot Encoding para variáveis nominais, Ordinal Encoding para variáveis ordenadas e padronização das numéricas. As transformações foram ajustadas apenas nos dados de treinamento para evitar vazamento de informações.

Não foram criadas features derivadas adicionais. A engenharia de features concentrou-se na seleção e transformação das variáveis disponíveis.

### 2.2 Quais modelos foram treinados e como foram avaliados?

Foram comparados dois modelos de regressão:

- **Ridge Regression:** modelo linear com regularização L2, que oferece simplicidade e facilidade de interpretação.
- **Random Forest Regressor:** modelo baseado em árvores de decisão, capaz de capturar relações não lineares e interações entre variáveis.

Também foi utilizado um `DummyRegressor`, que prevê a média do alvo, como referência mínima de desempenho (*baseline*).

O dataset foi dividido em 80% para treinamento e 20% para teste. Os modelos foram avaliados utilizando MAE, RMSE e R².

**Resultados no conjunto de teste:**

| Modelo | MAE ↓ | RMSE ↓ | R² ↑ |
|---|---:|---:|---:|
| DummyRegressor | 13,84 | 16,80 | -0,001 |
| Ridge | 8,59 | **10,39** | **0,617** |
| Random Forest | **8,31** | 10,43 | 0,614 |

Ambos os modelos de regressão superaram o baseline, indicando que as features selecionadas contêm informações úteis para prever o `klike_score`, mesmo sem métricas de performance pós-veiculação.

**Interpretação prática:** considerando que o `klike_score` varia de 0 a 100, o MAE de 8,59 indica que as previsões do Ridge apresentam um erro absoluto médio de aproximadamente 8,6 pontos. Embora represente uma melhoria expressiva em relação ao baseline, essa margem de erro pode ser relevante para o produto, especialmente ao comparar criativos com pontuações próximas.

Por isso, o score previsto deve ser interpretado como uma estimativa de qualidade, e não como uma avaliação exata. Na aplicação prática, seria importante comunicar essa incerteza ao usuário, evitando que pequenas diferenças entre pontuações sejam tratadas como evidências conclusivas de superioridade de um criativo.

### 2.3 Qual modelo foi selecionado?

Embora o Random Forest tenha apresentado MAE ligeiramente inferior, a comparação entre treino e teste revelou sinais expressivos de *overfitting*: seu R² caiu de 0,940 para 0,614, enquanto o MAE aumentou de 2,93 para 8,31 pontos.

Para complementar a avaliação, foi realizada validação cruzada com cinco folds no conjunto de treinamento:

| Modelo | MAE médio | Desvio-padrão |
|---|---:|---:|
| Ridge | 8,06 | 0,50 |
| Random Forest | **7,80** | 0,53 |

Os modelos apresentaram resultados próximos, com pequena vantagem do Random Forest no MAE médio.

**O Ridge foi selecionado como modelo final.** Apesar da pequena vantagem preditiva do Random Forest, o Ridge apresentou menor diferença entre treino e teste e permite uma interpretação mais direta das relações entre as features e o score.

No conjunto de teste, o modelo selecionado obteve MAE de **8,59 pontos** e R² de **0,617**, reduzindo o erro absoluto médio em aproximadamente 38% em relação ao baseline.

### 2.4 Quais variáveis mais se relacionam com o score?

Para interpretar o modelo selecionado, foram analisados os coeficientes do Ridge.

Os maiores coeficientes positivos foram observados para:

| Atributo | Coeficiente |
|---|---:|
| Presença de hook | +16,88 |
| Presença de rosto humano | +10,42 |
| Presença de CTA | +8,06 |
| Presença de legendas | +7,48 |

Como esses atributos são booleanos, os coeficientes representam diferenças no score previsto entre a ausência e a presença de cada característica, mantendo as demais variáveis constantes.

Esses resultados apresentam conexões com a EDA: hooks e rostos humanos estiveram associados a maiores medianas de CTR e engajamento, enquanto CTAs apresentaram associações positivas com métricas de conversão e retorno financeiro.

A densidade de texto apresentou coeficiente negativo (-2,49), coerente com as associações negativas observadas na análise exploratória.

Entretanto, a magnitude dos coeficientes não representa uma medida diretamente comparável de importância entre todas as features, devido às diferenças de escala e codificação.

### Limitações da modelagem

O dataset contém apenas 500 campanhas, e a fórmula utilizada para calcular o `klike_score` não foi disponibilizada. Portanto, não é possível determinar todos os fatores que influenciam sua construção.

Além disso, os coeficientes descrevem associações aprendidas pelo modelo, não efeitos causais. Alterar uma característica do vídeo não garante a variação correspondente no score ou nas métricas de performance.

Essas limitações serão consideradas na construção do Recommendations Engine, que deverá utilizar os resultados como evidências para formular hipóteses de otimização, sem prometer melhorias garantidas.