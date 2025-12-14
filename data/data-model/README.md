# Modelo Dimensional — Airbnb Data Engineering MVP (PUC-Rio)

Este documento descreve o modelo dimensional adotado no MVP de Engenharia de Dados do Airbnb, detalhando o racional da modelagem, a estrutura das tabelas e como o modelo suporta as análises de negócio propostas.

---

## 1. Objetivo da Modelagem

A etapa de modelagem tem como finalidade transformar os dados brutos (camada Bronze) e tratados (camada Silver) em uma estrutura analítica organizada, consistente e alinhada aos objetivos de negócio do MVP.

O modelo foi projetado para permitir:

- compreender padrões de ocupação e rentabilidade;
- identificar fatores que influenciam preço e desempenho;
- investigar diferenças entre tipos de hosts;
- avaliar o impacto de reviews e localização;
- comparar duas cidades distintas (Rio de Janeiro e New York City) dentro de um mesmo framework analítico.

Para atender a esses objetivos, foi adotado um **Esquema Estrela (Star Schema)**, amplamente utilizado em Business Intelligence e Data Warehousing por sua simplicidade, clareza e eficiência para análises multidimensionais.

---

## 2. Justificativa da Escolha: Esquema Estrela

O Star Schema foi escolhido porque:

- separa claramente **medidas numéricas** (tabelas fato) de **atributos descritivos** (tabelas dimensão);
- facilita análises exploratórias, agregações e construção de dashboards;
- reflete de forma natural a estrutura de marketplace do Airbnb;
- permite consultas mais simples e performáticas em ferramentas analíticas;
- evita normalizações excessivas (Snowflake), mantendo o foco analítico.

Mesmo com a presença de **duas tabelas fato**, o modelo permanece um Star Schema, pois:
- as dimensões não foram desmembradas em subdimensões;
- todos os relacionamentos seguem o padrão **dimensão → fato**;
- não há encadeamento entre dimensões.

---

## 3. Visão Geral do Modelo Dimensional

O modelo foi construído com base nos dados do Inside Airbnb e nas necessidades analíticas definidas no escopo do MVP.

Ele é composto por:

### Tabelas Fato

- **fact_calendar** — ocupação e estimativa de receita diária  
  *Grão: listing × date × city*

- **fact_reviews** — reviews individuais de usuários  
  *Grão: listing × review_id × city*

### Tabelas Dimensão

- **dim_listings** — detalhes do imóvel e do anúncio
- **dim_hosts** — características do anfitrião
- **dim_neighbourhoods** — informações espaciais e categorização dos bairros

Todas as tabelas possuem a coluna **city**, permitindo análises integradas entre Rio de Janeiro e New York City dentro do mesmo modelo.

---

## 4. Relacionamentos e Cardinalidades

- Um **host** pode possuir vários **listings**
- Um **bairro** pode conter vários **listings**
- Um **listing** aparece várias vezes no **fact_calendar** (um registro por dia)
- Um **listing** pode possuir vários **reviews**

Essas relações garantem integridade referencial e suportam análises temporais, geográficas e comportamentais.

---

## 5. Descrição e Racional de Cada Tabela

### 5.1 Dimensão: `dim_listings`

**Grão:** 1 linha por anúncio (`listing_id` + `city`)

**Descrição:**  
Contém todas as características relevantes do imóvel e do anúncio.

**Justificativa:**  
É a dimensão central do modelo, pois concentra os principais atributos usados para explicar:

- variações de preço;
- tipo de imóvel;
- capacidade;
- qualidade e reviews;
- localização;
- perfil do host;
- performance histórica.

**Responde a perguntas como:**

- O que diferencia anúncios de alta performance?
- Quais fatores influenciam o preço da diária?
- Como a localização impacta valor e ocupação?

---

### 5.2 Dimensão: `dim_hosts`

**Grão:** 1 linha por host (`host_id` + `city`)

**Descrição:**  
Armazena informações sobre os anfitriões, incluindo status de superhost e tamanho do portfólio.

**Justificativa:**  
Hosts profissionais tendem a adotar estratégias diferentes de precificação e operação em relação a hosts individuais.

Essa dimensão é essencial para análises de:

- profissionalização do mercado;
- impacto do status de superhost;
- comportamento do host sobre desempenho e receita.

**Responde a:**

- Existe diferença entre hosts profissionais e hosts casuais?
- Superhosts apresentam melhor desempenho?

---

### 5.3 Dimensão: `dim_neighbourhoods`

**Grão:** 1 linha por bairro (`neighbourhood` + `city`)

**Descrição:**  
Contém informações espaciais e categorização dos bairros, incluindo geometrias em formato GeoJSON.

**Justificativa:**  
Localização é um dos fatores mais determinantes de preço, ocupação e rentabilidade no Airbnb.

Essa dimensão permite:

- análises geográficas;
- criação de mapas interativos;
- identificação de clusters de alta performance.

**Responde a:**

- Como a localização impacta o preço?
- Existem bairros mais produtivos ou mais competitivos?

---

### 5.4 Fato: `fact_calendar`

**Grão:** 1 linha por anúncio por dia por cidade

**Descrição:**  
Representa a combinação diária `listing × date`, contendo informações de disponibilidade, ocupação e estimativa de receita.

**Justificativa:**  
É o núcleo das análises temporais do projeto.

Permite medir:

- ocupação diária;
- sazonalidade;
- rentabilidade estimada;
- impacto de eventos, feriados e períodos específicos.

**Responde a:**

- Padrões de variação da ocupação ao longo do tempo
- Relação entre preço, disponibilidade e receita
- Diferenças temporais entre cidades e bairros

---

### 5.5 Fato: `fact_reviews`

**Grão:** 1 linha por review por cidade

**Descrição:**  
Armazena os reviews dos usuários, incluindo data e texto do comentário.

**Justificativa:**  
Reviews impactam diretamente visibilidade, ranking e confiança nos anúncios.

Essa tabela permite análises sobre:

- volume e frequência de reviews;
- recência das avaliações;
- relação entre reviews, preço e ocupação.

**Responde a:**

- Qual o papel dos reviews na performance?
- Existe relação entre avaliação, demanda e receita?

---

## 6. Diagrama e Script do Modelo

- O diagrama conceitual do modelo está disponível em **PDF**, exportado do dbdiagram.io.
- Na sequência, o script usado para a construção do modelo no dbdiagram.io:

Table dim_hosts {
  city                     varchar
  host_id                  bigint [pk]
  host_name                varchar
  host_since               date
  host_is_superhost_bool   boolean
  host_total_listings_count int
  calculated_host_listings_count int
  host_type                varchar // ex: 'professional', 'individual'
}

Table dim_neighbourhoods {
  city               varchar
  neighbourhood      varchar [pk]
  neighbourhood_group varchar
  geometry_json      text
}

Table dim_listings {
  city                               varchar
  listing_id                         bigint [pk]
  host_id                            bigint  // FK -> dim_hosts
  neighbourhood_cleansed             varchar // FK -> dim_neighbourhoods.neighbourhood
  property_type                      varchar
  room_type                          varchar
  accommodates                       int
  bathrooms                          double
  bedrooms                           double
  beds                               int
  price_numeric                      double
  review_scores_rating               double
  reviews_per_month                  double
  estimated_occupancy_l365d          int
  estimated_revenue_l365d            double
  is_entire_home                     boolean
  is_private_room                    boolean
  is_shared_room                     boolean
  is_hotel_room                      boolean
  host_is_superhost_bool             boolean
  host_identity_verified_bool        boolean
  instant_bookable_bool              boolean
  last_review_date                   date
  review_recency_days                int
}

Table fact_calendar {
  city               varchar
  listing_id         bigint  // FK -> dim_listings
  date_date          date
  available_bool     boolean
  is_occupied        boolean
  price_numeric      double
  adjusted_price_numeric double
  revenue_estimated  double
  minimum_nights     int
  maximum_nights     int
}

Table fact_reviews {
  city            varchar
  listing_id      bigint  // FK -> dim_listings
  review_id       bigint [pk]
  review_date     date
  comments_clean  text
}

Ref: dim_hosts.host_id < dim_listings.host_id
Ref: dim_neighbourhoods.neighbourhood < dim_listings.neighbourhood_cleansed
Ref: dim_listings.listing_id < fact_calendar.listing_id
Ref: dim_listings.listing_id < fact_reviews.listing_id


Esses artefatos complementam a documentação e servem como evidência formal da etapa de modelagem do MVP.
