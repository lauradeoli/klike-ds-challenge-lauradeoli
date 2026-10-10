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

🚧 Em desenvolvimento — configuração inicial do ambiente.