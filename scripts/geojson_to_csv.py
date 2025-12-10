import json
import csv

input_file = "neighbourhoods.geojson"      # nome do arquivo de entrada
output_file = "neighbourhoods_rio.csv"     # nome do arquivo de saída

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

features = data.get("features", [])

# Definimos as colunas que queremos extrair das propriedades
# Ajuste os nomes se o arquivo tiver variações
header = [
    "neighbourhood",
    "neighbourhood_group",
    "geometry_json"
]

with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)

    for feat in features:
        props = feat.get("properties", {})
        geom = feat.get("geometry", {})

        neighbourhood = props.get("neighbourhood", "")
        neighbourhood_group = props.get("neighbourhood_group", "")
        geometry_json = json.dumps(geom, ensure_ascii=False)

        writer.writerow([neighbourhood, neighbourhood_group, geometry_json])

print(f"Arquivo CSV gerado com sucesso: {output_file}")
