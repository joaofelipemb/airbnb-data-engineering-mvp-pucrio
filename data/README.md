
# Diretório `data/` — Airbnb Data Engineering MVP (PUC-Rio)

Este diretório concentra os **dados utilizados ou gerados** no MVP de Engenharia de Dados aplicado ao dataset do Inside Airbnb, referente às cidades:

- **Rio de Janeiro**
- **New York City**

Por questões de tamanho e boas práticas, **os arquivos brutos não são versionados no GitHub**.  
Aqui mantemos apenas arquivos **processados, leves** e todas as instruções para reconstrução completa do pipeline.

---

## Estrutura do diretório
data/
│
├── processed/
│ ├── neighbourhoods_rj.csv
│ ├── neighbourhoods_nyc.csv
│ └── neighbourhoods.geojson (opcional — amostra leve)
│
└── README.md

##  Links oficiais para download dos dados originais

Todos os datasets foram obtidos do projeto **Inside Airbnb**:

https://insideairbnb.com/get-the-data/

### **New York City**
- `listings.csv.gz`  
- `calendar.csv.gz`  
- `reviews.csv.gz`  
- `neighbourhoods.geojson`  

### **Rio de Janeiro**
- `listings.csv.gz`  
- `calendar.csv.gz`  
- `reviews.csv.gz`  
- `neighbourhoods.geojson`

---

## Dados presentes neste repositório

Como parte do processamento realizado no notebook de engenharia de dados:

### **`processed/neighbourhoods_rj.csv`**
- Conversão de GeoJSON → CSV  
- Usado para construção de mapas no Databricks  
- Possui colunas:
  - `city`
  - `neighbourhood`
  - `neighbourhood_group`
  - `geometry_json`

### **`processed/neighbourhoods_nyc.csv`**
- Estrutura similar à versão RJ  
- Utilizada nos mapas e análises de localização

### **(Opcional) `processed/neighbourhoods.geojson`**
- Disponível apenas se desejar demonstrar o arquivo original antes da conversão

---

## Script utilizado para gerar os arquivos processados

O script responsável pela conversão de `.geojson` → `.csv` está em:
/scripts/geojson_to_csv.py


3. **Subir os dados processados** para o Databricks (Unity Catalog / Volumes gerenciados)

4. **Executar o notebook de criação de tabelas**:  
- `notebooks/criacao_tabelas`  
  → gera as camadas **Bronze**, **Silver** e **Gold**

5. (Opcional) **Executar as análises**:  
- `notebooks/analise_qualidade_dados`  
- `notebooks/analise_dados`

Esses notebooks reproduzem todas as validações e análises do MVP.

---

## Observação sobre reprodutibilidade

Este diretório foi projetado para:

- documentar as fontes e artefatos necessários,
- manter apenas dados leves e processados,
- permitir que qualquer pessoa execute **o pipeline completo** usando:
- arquivos originais baixados do Inside Airbnb,
- os scripts,
- e os notebooks presentes no repositório.

Os dados brutos **não são armazenados aqui**, mas **todas as instruções e scripts necessários** para aplicá-los estão incluídos no projeto.

---