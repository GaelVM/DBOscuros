import requests
from bs4 import BeautifulSoup
import json

# URL de la página web
url = "https://pokemondb.net/go/shadow#shadow-grunts"

# Realizar la solicitud HTTP
response = requests.get(url)

# Verificar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Analizar el contenido HTML de la página web
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar la tabla con la clase "data-table block-wide"
    table = soup.find('table', class_='data-table block-wide')

    # Verificar si se encontró la tabla
    if table:
        # Lista para almacenar los datos de la tabla como diccionarios
        table_data = []

        # Iterar sobre las filas de la tabla
        for row in table.find_all('tr'):
            # Obtener los datos de cada celda en la fila
            cells = row.find_all('td')
            if cells:
                data = [cell.text.strip() for cell in cells]
                # Crear un diccionario con los datos de la fila
                row_data = {
                    "Typo": data[0],
                    "texto": data[1],
                    "Slot1": data[2],
                    "Slot2": data[3],
                    "Slot3": data[4],
                    # Agregar más columnas según sea necesario
                }
                table_data.append(row_data)

        # Leer el archivo de traducciones
        with open('datos/oscuros.json', 'r', encoding='utf-8') as translation_file:
            translations = json.load(translation_file)

        # Agregar traducciones al diccionario original
        for entry in table_data:
            matching_translation = next(
                (t["traduccion"] for t in translations if t["texto"] == entry["texto"]),
                None
            )
            if matching_translation:
                entry["traduccion"] = matching_translation

        # Escribir los datos en un archivo JSON
        with open('oscuros.json', 'w', encoding='utf-8') as json_file:
            json.dump(table_data, json_file, ensure_ascii=False, indent=2)

        print("Los datos se han guardado en 'oscuros.json'.")
    else:
        print("No se encontró la tabla en la página.")
else:
    print(f"Error al realizar la solicitud HTTP. Código de estado: {response.status_code}")
