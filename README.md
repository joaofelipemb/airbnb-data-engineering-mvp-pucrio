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
│   ├── autoavaliacao.md     # Reflexão sobre o aprendizado e desafios
│   └── relatorio_final.md   # Relatório técnico completo do MVP
│
├── data/                    # Metadados e dados auxiliares processados
│   ├── data_catalog.md      # Dicionário de dados da camada Gold
│   ├── processed/           # Arquivos CSV convertidos (GeoJSON -> CSV)
│   └── data-model/          # Documentação da modelagem dimensional
│       ├── diagram.pdf      # Diagrama Visual do Schema (ER)
│       └── README.md        # Explicação detalhada das tabelas e relacionamentos
│
├── notebooks/               # Pipeline de Engenharia e Análise (Databricks)
│   ├── 01_criacao_tabelas.ipynb         # Ingestão, tratamento e criação (Bronze/Silver/Gold)
│   ├── 02_analise_qualidade_dados.ipynb # QA, validação de completude e consistência
│   ├── 03_analise_dados.ipynb           # Análise exploratória e respostas ao negócio
│   └── 03_analise_dados.html            # Versão HTML com mapas interativos renderizados
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
* Quais fatores influenciam o preço da diária e a receita estimada?
* Como a localização afeta o preço, demanda e competitividade?

> **Nota:** Como o GitHub não renderiza mapas interativos em arquivos `.ipynb`, está também disponível a versão **`notebooks/03_analise_dados.html`**. Baixe este arquivo para visualizar os mapas geoespaciais completos.
---

## Modelagem de Dados

O projeto utiliza um **Esquema Estrela (Star Schema)**.

* Para visualizar o diagrama ER completo, acesse: [data/data-model/diagram.pdf](data/data-model/diagram.pdf).
* Para detalhes das tabelas e cardinalidades, leia: [data/data-model/README.md](data/data-model/README.md).

O Catálogo de Dados completo das tabelas finais encontra-se em: [data/data_catalog.md](data/data_catalog.md).

---

## Como Executar

### Pré-requisitos
* Conta no [Databricks Community Edition](https://community.cloud.databricks.com/).
* Python 3.x instalado localmente (apenas para o script auxiliar).

### Passos
1.  **Preparação dos Dados:**
    * Acesse o [Inside Airbnb](http://insideairbnb.com/get-the-data/).
    * Localize as seções do **Rio de Janeiro** e **New York City**.
    * Baixe os seguintes arquivos para **ambas** as cidades (certifique-se de pegar a versão completa/detalhada):
        * `listings.csv.gz` (Detailed Listings data)
        * `calendar.csv.gz` (Detailed Calendar data)
        * `reviews.csv.gz` (Detailed Reviews data)
        * `neighbourhoods.geojson` (GeoJSON file)
    * Converta os arquivos `.geojson` usando o script `scripts/geojson_to_csv.py`.
    * Faça o upload dos CSVs para um Volume no Databricks.
2.  **Execução:**
    * Importe os notebooks da pasta `notebooks/` para o seu Workspace.
    * Execute-os na ordem numérica sequencial (`01` -> `02` -> `03`).

---

## Autor

**João Felipe Maia Barbosa**
*Projeto de Engenharia de Dados - PUC-Rio (Dezembro/2025)*
