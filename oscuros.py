import os
import requests
from bs4 import BeautifulSoup
import json

# Define la carpeta temporal
temp_folder = "temp"

# Verifica si la carpeta temporal ya existe, y si no, créala
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)

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
        # Diccionario para almacenar los datos de la tabla
        all_data_dict = {}

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
                    "traduccion": ""  # Puedes inicializarlo con una cadena vacía
                }

                # Obtener o inicializar la lista para este tipo
                type_list = all_data_dict.get(data[0], [])
                type_list.append(row_data)
                # Actualizar el diccionario con la lista actualizada
                all_data_dict[data[0]] = type_list

        # Leer el archivo de traducciones
        with open('datos/oscuros.json', 'r', encoding='utf-8') as translation_file:
            translations = json.load(translation_file)

        # Agregar traducciones al diccionario original
        for entry_list in all_data_dict.values():
            for entry in entry_list:
                matching_translation = next(
                    (t["traduccion"] for t in translations if t["texto"] == entry["texto"]),
                    None
                )
                if matching_translation:
                    entry["traduccion"] = matching_translation

        # Define la ruta completa del archivo JSON en la carpeta temporal
        json_file_path = os.path.join(temp_folder, "oscuros.json")

        # Guardar el diccionario en un archivo JSON en la carpeta temporal
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(all_data_dict, json_file, ensure_ascii=False, indent=2)

        print(f"Datos guardados en {json_file_path}")

    else:
        print("No se encontró la tabla en la página.")

else:
    print(f"Error al obtener la página. Código de estado: {response.status_code}")
