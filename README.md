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