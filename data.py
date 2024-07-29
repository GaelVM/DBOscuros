import os
import requests
from bs4 import BeautifulSoup
import json

# Define la carpeta temporal
temp_folder = "temp"

# Verifica si la carpeta temporal ya existe, y si no, créala
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)

url = "https://www.serebii.net/pokemongo/shadowpokemon.shtml"
response = requests.get(url)

# Diccionario de traducción
translation_dict = {
    "Available when encountered": "Disponible cuando se encuentra",
    "Evolve Shadow": "Al evolucionar ",
    "Evolution": "Evolución"
}

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table', class_='tab')  # Buscar todas las tablas con la clase 'tab'
    
    if len(tables) > 1:
        table = tables[1]  # Seleccionar la segunda tabla

        data = []

        for row in table.find_all('tr')[1:]:  # Ignorar la primera fila que contiene los encabezados
            columns = row.find_all('td')
            
            if len(columns) == 6:
                type_imgs = columns[3].find_all("img")
                
                # Obtener el valor de Stats y traducir si es necesario
                stats_value = columns[5].text.strip()
                translated_stats = stats_value

                for key in translation_dict:
                    if key in stats_value:
                        translated_stats = stats_value.replace(key, translation_dict[key])
                        break

                entry = {
                    "No.": columns[0].text.strip(),
                    "Pic": "https://www.serebii.net" + columns[1].find('img')['src'].strip() if columns[1].find('img') else "",
                    "Name": columns[3].find('a').text.strip(),
                    "Stats": translated_stats
                }
                data.append(entry)
            else:
                print(f"Advertencia: Fila incompleta con {len(columns)} columnas, se omite.")

        # Define la ruta completa del archivo JSON en la carpeta temporal
        json_file_path = os.path.join(temp_folder, "oscurosdata.json")

        # Guardar el diccionario en un archivo JSON en la carpeta temporal
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=2)

        print(f"Datos guardados en {json_file_path}")
    else:
        print("No se encontró la segunda tabla.")

else:
    print(f"Error al obtener la página. Código de estado: {response.status_code}")
