# Engenharia de Dados: Análise de Mercado Airbnb (RJ & NYC)

![Status](https://img.shields.io/badge/Status-Concluído-success)
![Platform](https://img.shields.io/badge/Plataforma-Databricks-orange)
![Language](https://img.shields.io/badge/Linguagem-Python%20%7C%20SQL-blue)
![Architecture](https://img.shields.io/badge/Arquitetura-Medallion%20(Bronze%2FSilver%2FGold)-purple)

## Sobre o Projeto
Este repositório contém o MVP (Minimum Viable Product) desenvolvido como requisito final da disciplina de **Engenharia de Dados** da Pós-Graduação em *Data Science & Analytics* da **PUC-Rio**.

O projeto consiste em um pipeline de dados ponta a ponta (*End-to-End*) para analisar o mercado de *Short-Term Rentals* (STR) no **Rio de Janeiro**, utilizando **New York City** como base comparativa. A arquitetura implementada é um **Data Lakehouse** no Databricks, seguindo a metodologia Medallion (Bronze, Silver, Gold).

---

## Estrutura do Repositório

A organização dos arquivos segue a lógica do ciclo de vida dos dados:

```text
├── reports/                 # Documentação oficial do projeto
│   ├── autoavaliacao.pdf    # Reflexão sobre o aprendizado e desafios
│   └── relatorio_final.pdf  # Relatório técnico completo do MVP
│
├── data/                    # Metadados e dados auxiliares processados
│   ├── data_catalog.csv     # Dicionário de dados da camada Gold
│   ├── processed/           # Arquivos CSV convertidos (GeoJSON -> CSV)
│   └── data-model/          # Documentação da modelagem dimensional
│       ├── diagram.pdf      # Diagrama Visual do Schema (ER)
│       └── README.md        # Explicação detalhada das tabelas e relacionamentos
│
├── notebooks/               # Pipeline de Engenharia e Análise (Databricks)
│   ├── 01_criacao_tabelas.ipynb         # Ingestão, tratamento e criação (Bronze/Silver/Gold)
│   ├── 02_analise_qualidade_dados.ipynb # QA, validação de completude e consistência
│   └── 03_analise_dados.ipynb           # Análise exploratória e respostas ao negócio
│
├── scripts/                 # Scripts Python auxiliares
│   └── geojson_to_csv.py    # Conversor de dados geoespaciais para tabular
│
└── README.md                # Este arquivo
```
## Arquitetura e Pipeline

O projeto foi executado no **Databricks Community Edition** utilizando **Unity Catalog** para gerenciamento de volumes e tabelas Delta.

### 1. Ingestão e Processamento (`notebooks/01_criacao_tabelas.ipynb`)
Este notebook consolida todo o fluxo de engenharia:
* **Camada Bronze:** Carregamento dos dados brutos (`listings`, `calendar`, `reviews`) e integração dos dados geográficos processados.
* **Camada Silver:** Limpeza de dados (remoção de HTML), tipagem correta (colunas `_numeric`, `_date`) e padronização.
* **Camada Gold:** Criação do **Modelo Dimensional (Star Schema)** com tabelas Fato e Dimensão (`dim_hosts`, `dim_listings`, `fact_calendar`, etc.).

### 2. Qualidade de Dados (`notebooks/02_analise_qualidade_dados.ipynb`)
Notebook dedicado ao QA (*Quality Assurance*), contendo:
* Verificação de completude (nulos e brancos).
* Validação de integridade referencial (FKs e PKs).
* Diagnóstico de limitações do dataset original (ex: ausência de preços no calendário).

### 3. Análise de Negócio (`notebooks/03_analise_dados.ipynb`)
Notebook final com SQL e visualizações Python respondendo às perguntas de negócio:
* O que define um anúncio de alta performance?
* Correlação entre preço, ocupação e receita anual.
* Análise geoespacial e comparação RJ vs NYC.

---

## Modelagem de Dados

O projeto utiliza um **Esquema Estrela (Star Schema)**.

* Para visualizar o diagrama ER completo, acesse: [data/data-model/diagram.pdf](data/data-model/diagram.pdf).
* Para detalhes das tabelas e cardinalidades, leia: [data/data-model/README.md](data/data-model/README.md).

O Catálogo de Dados completo das tabelas finais encontra-se em: [data/data_catalog.csv](data/data_catalog.csv).

---

## Como Executar

### Pré-requisitos
* Conta no [Databricks Community Edition](https://community.cloud.databricks.com/).
* Python 3.x instalado localmente (apenas para o script auxiliar).

### Passos
1.  **Preparação:**
    * Baixe os dados do [Inside Airbnb](http://insideairbnb.com/get-the-data/) (Rio de Janeiro e NYC).
    * Converta os arquivos `.geojson` usando o script `scripts/geojson_to_csv.py`.
    * Faça o upload dos CSVs para um Volume no Databricks.
2.  **Execução:**
    * Importe os notebooks da pasta `notebooks/` para o seu Workspace.
    * Execute-os na ordem numérica sequencial (`01` -> `02` -> `03`).

---

## Autor

**João Felipe Maia Barbosa**
*Projeto de Engenharia de Dados - PUC-Rio (Dezembro/2025)*
