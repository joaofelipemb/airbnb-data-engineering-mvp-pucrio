# Catálogo de Dados (Data Dictionary)

Este documento detalha a estrutura da **Camada Gold**. Abaixo estão descritas as tabelas Dimensionais (Dim) e Fato (Fact), seus atributos, tipos de dados e regras de negócio.

---

## 1. Tabela: `dim_hosts`
**Descrição:** Dimensão de anfitriões. Contém um registro único por host por cidade.

| Atributo | Tipo | Descrição | Domínio / Regras | Cardinalidade | Origem / Linhagem | Observações Técnicas |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **city** | STRING | Cidade do anúncio (ex.: "Rio de Janeiro", "New York City") | Conjunto finito de cidades do projeto (inicialmente RJ, NYC). | Muitos hosts por cidade. | `silver_listings_*.city` (deduplicado por host) | Usado também como “filtro lógico” para separar mercados. |
| **host_id** | BIGINT | Identificador do anfitrião na plataforma Airbnb | Chave natural do host no Inside Airbnb. | Chave primária lógica (PK composta: city, host_id). | `silver_listings_*.host_id` | Em DW podemos tratar (city, host_id) como PK composta. |
| **host_name** | STRING | Nome do anfitrião | Livre, texto curto. | 1 valor por host. | `silver_listings_*.host_name` | Pode conter nulos ou valores genéricos (“Host”, “Company”). |
| **host_since** | DATE | Data em que o anfitrião entrou na plataforma | Data válida ≥ ano inicial da operação do Airbnb. | 1 valor por host. | `silver_listings_*.host_since` | Permite derivar antiguidade do host. |
| **host_is_superhost_bool** | BOOLEAN | Flag indicando se o host é superhost | `{TRUE, FALSE, NULL}`. | 1 valor por host. | `silver_listings_*.host_is_superhost_bool` | NULL significa “informação ausente” na origem. |
| **host_total_listings_count** | INT | Número de anúncios do host (campo original da fonte) | Inteiro ≥ 0. | 1 valor por host. | `silver_listings_*.host_total_listings_count` | Pode ser inconsistente; será comparado com `calculated_host_listings_count`. |
| **calculated_host_listings_count** | INT | Número de anúncios do host calculado a partir das tabelas | Inteiro ≥ 0. | 1 valor por host. | Contagem de `dim_listings` por (city, host_id) | Usado para detectar hosts “profissionais” (limiar a ser definido na Gold, ex.: ≥ 3 anúncios). |
| **host_type** | STRING | Classificação do host (ex.: professional, individual) | Conjunto finito (por ex.: professional, individual, unknown). | 1 valor por host. | Regra na Gold com base em `calculated_host_listings_count` | Regras claras no relatório: por exemplo, >= 3 listings → professional. |

---

## 2. Tabela: `dim_neighbourhoods`
**Descrição:** Dimensão de bairros e regiões, incluindo informação geoespacial em formato JSON.

| Atributo | Tipo | Descrição | Domínio / Regras | Cardinalidade | Origem / Linhagem | Observações Técnicas |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **city** | STRING | Cidade | Mesmos valores de `dim_hosts.city`. | Vários bairros por cidade. | `silver_neighbourhoods_*.city` | Ajuda a diferenciar bairros de cidades distintas com mesmo nome. |
| **neighbourhood** | STRING | Nome do bairro | Texto padronizado pela fonte (Inside Airbnb). | PK lógica junto com city. | `silver_neighbourhoods_*.neighbourhood` | Deve ser alinhado com `dim_listings.neighbourhood_cleansed`. |
| **neighbourhood_group** | STRING | Região agregada (subdivisão da cidade, quando existir) | Pode ser vazio / NULL (como ocorre no Rio). | 1 valor por bairro. | `silver_neighbourhoods_*.neighbourhood_group` | Em NYC costuma ter significado forte (ex.: Manhattan, Brooklyn, etc.). |
| **geometry_json** | TEXT | Geometria em formato JSON (polígonos geoespaciais) | JSON válido representando MultiPolygon/Polygon. | 1 valor por bairro. | Conversão de `neighbourhoods.geojson` → `*_neighbourhoods_*.csv` | Mantido como string; parsing geoespacial avançado pode ser feito em outro projeto. |

---

## 3. Tabela: `dim_listings`
**Descrição:** Dimensão principal do modelo – descreve cada anúncio (imóvel) por cidade.

| Atributo | Tipo | Descrição | Domínio / Regras | Cardinalidade | Origem / Linhagem | Observações Técnicas |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **city** | STRING | Cidade do anúncio | Mesmos valores de `dim_hosts.city`. | Muitos listings por cidade. | `silver_listings_*.city` | Útil para filtros e para construir métricas por mercado. |
| **listing_id** | BIGINT | Identificador do anúncio na plataforma | Chave natural fornecida pelo Inside Airbnb. | PK lógica (junto com city). | `silver_listings_*.id` | Usado como chave estrangeira em `fact_calendar` e `fact_reviews`. |
| **host_id** | BIGINT | Identificador do anfitrião responsável | Deve existir em `dim_hosts.host_id` para a mesma city. | N:1 em relação a `dim_hosts`. | `silver_listings_*.host_id` | FK lógica para `dim_hosts`. |
| **neighbourhood_cleansed** | STRING | Bairro do anúncio (padronizado pela fonte) | Deve casar com `dim_neighbourhoods.neighbourhood` para a mesma cidade. | N:1 em relação a `dim_neighbourhoods`. | `silver_listings_*.neighbourhood_cleansed` | Em caso de mismatch, será tratado na etapa de qualidade de dados. |
| **property_type** | STRING | Tipo de propriedade | Domínio finito conforme fonte (ex.: Apartment, House, Loft, etc.). | 1 valor por listing. | `silver_listings_*.property_type` | Usado em filtros analíticos e segmentações de mercado. |
| **room_type** | STRING | Tipo de quarto | Ex: Entire home/apt, Private room, Shared room, Hotel room. | 1 valor por listing. | `silver_listings_*.room_type` | Base para flags `is_entire_home`, `is_private_room`, etc. |
| **accommodates** | INT | Capacidade máxima de hóspedes | Inteiro ≥ 1. | 1 valor por listing. | `silver_listings_*.accommodates` | Pode ser usado pra segmentar por porte do imóvel. |
| **bathrooms** | DOUBLE | Número de banheiros | ≥ 0 (pode ter metade, ex.: 1.5). | 1 valor por listing. | `silver_listings_*.bathrooms` | Em alguns snapshots pode existir `bathrooms_text`; usar a métrica numérica consolidada se disponível. |
| **bedrooms** | DOUBLE | Número de quartos | ≥ 0. | 1 valor por listing. | `silver_listings_*.bedrooms` | Pode haver nulos em estúdios (0 bedrooms). |
| **beds** | INT | Número de camas | Inteiro ≥ 0. | 1 valor por listing. | `silver_listings_*.beds` | Relevante para análise de capacidade vs ocupação. |
| **price_numeric** | DOUBLE | Preço do anúncio (diária padrão), em moeda local | Rio → BRL; NYC → USD. Valores > 0 para anúncios ativos. | 1 valor por listing. | Conversão de `silver_listings_*.price` → numérico | Não há conversão de moeda na Silver. Conversão NYC→BRL será feita na Gold quando necessário. |
| **review_scores_rating** | DOUBLE | Nota média de avaliação | Range [0, 5] (ou NULL). | 1 valor por listing. | `silver_listings_*.review_scores_rating` | Pode ser usado para filtrar anúncios com poucas avaliações (NULL). |
| **reviews_per_month** | DOUBLE | Média de reviews por mês | ≥ 0 (pode ser fração). | 1 valor por listing. | `silver_listings_*.reviews_per_month` | Relaciona-se com liquidez / demanda do anúncio. |
| **estimated_occupancy_l365d** | INT | Ocupação estimada em dias nos últimos 365 dias | Entre 0 e 365 (inteiro). | 1 valor por listing. | Campo específico da fonte (`silver_listings_*`) | Quando presente, permite validar nossos cálculos de ocupação. |
| **estimated_revenue_l365d** | DOUBLE | Receita estimada nos últimos 365 dias (moeda local) | ≥ 0. | 1 valor por listing. | Campo específico da fonte (`silver_listings_*`) | Pode ser comparado com receita calculada a partir de `fact_calendar`. |
| **is_entire_home** | BOOLEAN | Flag: anúncio é “Entire home/apt” | TRUE se room_type = 'Entire home/apt'. | 1 valor por listing. | Derivado de `room_type` | Facilita análises segmentadas sem depender de string matching. |
| **host_is_superhost_bool** | BOOLEAN | Cópia da flag de superhost no contexto do anúncio | `{TRUE, FALSE, NULL}`. | 1 valor por listing. | `silver_listings_*.host_is_superhost_bool` | Redundância intencional (também aparece em dim_hosts), útil pra consultas só na dim_listings. |
| **last_review_date** | DATE | Data do último review | Data válida ou NULL (sem reviews). | 1 valor por listing. | Conversão de `silver_listings_*.last_review` | Combina com `review_recency_days`. |

*(Nota: Outras colunas como `is_private_room`, `is_shared_room`, `is_hotel_room`, `host_identity_verified_bool`, `instant_bookable_bool` e `review_recency_days` seguem lógica similar às listadas acima)*

---

## 4. Tabela: `fact_calendar`
**Descrição:** Fato de ocupação diária / disponibilidade. Grão: 1 linha por listing por dia por cidade.

| Atributo | Tipo | Descrição | Domínio / Regras | Cardinalidade | Origem / Linhagem | Observações Técnicas |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **city** | STRING | Cidade | Mesmos valores das dimensões. | Muitos registros por cidade. | De `silver_calendar_*.city` | A chave lógica completa é (city, listing_id, date_date). |
| **listing_id** | BIGINT | ID do anúncio | Deve existir em `dim_listings`. | N:1 em relação a `dim_listings`. | `silver_calendar_*.listing_id` | FK lógica. |
| **date_date** | DATE | Data da observação | Datas dentro do range do snapshot. | Vários registros por listing (1/dia). | `silver_calendar_*.date` | Chave temporal da tabela. |
| **available_bool** | BOOLEAN | Disponibilidade na data | TRUE = disponível, FALSE = indisponível. | 1 valor por linha. | `silver_calendar_*.available` | Ajuda em análises de disponibilidade. |
| **is_occupied** | BOOLEAN | O anúncio está ocupado nessa data? | TRUE quando available_bool = FALSE. | 1 valor por linha. | Derivado de `available_bool` | Métrica fundamental para cálculo de ocupação. |
| **price_numeric** | DOUBLE | Preço diário informado no calendar | Tipicamente NULL neste dataset (RJ/NYC). | 1 valor por linha. | Conversão de `silver_calendar_*.price` | Mantido por completude; usamos `dim_listings.price_numeric` como proxy. |
| **revenue_estimated** | DOUBLE | Receita estimada para o dia | CASE WHEN is_occupied THEN <preço> ELSE 0 END. | 1 valor por linha. | Calculado na Gold | Métrica Gold, serve de base para KPIs. |
| **minimum_nights** | INT | Mínimo de noites exigido | Inteiro ≥ 1. | 1 valor por linha. | `silver_calendar_*.minimum_nights` | Conecta com regras de negócio. |
| **maximum_nights** | INT | Máximo de noites permitido | Inteiro ≥ 1 (ou NULL). | 1 valor por linha. | `silver_calendar_*.maximum_nights` | Pode ser NULL para hosts sem limite. |

---

## 5. Tabela: `fact_reviews`
**Descrição:** Fato de reviews individuais. Grão: 1 linha por review por anúncio por cidade.

| Atributo | Tipo | Descrição | Domínio / Regras | Cardinalidade | Origem / Linhagem | Observações Técnicas |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **city** | STRING | Cidade do anúncio | Mesmos valores de `dim_listings.city`. | Muitos reviews por cidade. | Derivado de `silver_reviews_*` | Facilita análises comparativas. |
| **listing_id** | BIGINT | ID do anúncio | Deve existir em `dim_listings`. | N:1 em relação a `dim_listings`. | `silver_reviews_*.listing_id` | FK lógica. |
| **review_id** | BIGINT | Identificador do review | Chave única do review (por cidade). | PK lógica (city, review_id). | `silver_reviews_*.id` | Em alguns snapshots o ID vem como `id`. |
| **review_date** | DATE | Data do review | Datas dentro do range histórico. | 1 valor por review. | `silver_reviews_*.date` | Pode ser usado pra recência de feedback. |
| **comments_clean** | TEXT | Texto do review limpo | Texto livre, sem `<br>`, `\n`, etc. | 1 valor por review. | Derivado de `silver_reviews_*.comments` | Coluna original permanece na Silver; aqui usamos a limpa. |
