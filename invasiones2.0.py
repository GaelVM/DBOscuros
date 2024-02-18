import os
import json
import requests

# Define la carpeta temporal
temp_folder = "temp"

# Verifica si la carpeta temporal ya existe, y si no, créala
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)

# Define la ruta completa del archivo JSON en la carpeta temporal
json_file_path = os.path.join(temp_folder, "invasiones2.0.json")


# Diccionario typo
typo_list = [
    (4, "Sin tipo"), (5, "Sin tipo"), (6, "Bicho"), (7, "Bicho"), (10, "Siniestro"),
    (11, "Siniestro"), (12, "Dragón"), (13, "Dragón"), (14, "Hada"), (15, "Hada"),
    (16, "Lucha"), (17, "Lucha"), (18, "Fuego"), (19, "Fuego"), (20, "Volador"),
    (21, "Volador"), (22, "Planta"), (23, "Planta"), (24, "Tierra"), (25, "Tierra"),
    (26, "Hielo"), (27, "Hielo"), (28, "Acero"), (29, "Acero"), (30, "Normal"),
    (31, "Normal"), (32, "Veneno"), (33, "Veneno"), (34, "Psíquico"), (35, "Psíquico"),
    (36, "Roca"), (37, "Roca"), (38, "Agua"), (39, "Agua"), (41, "Cliff"), (42, "Arlo"),
    (43, "Sierra"), (44, "Giovanni"), (45, "Señuelo"), (46, "Señuelo"), (47, "Fantasma"),
    (48, "Fantasma"), (49, "Eléctrico"), (50, "Eléctrico")
]

# Convertir la lista de tuplas en un diccionario
typo = dict(typo_list)

# Diccionario de frases
frase_list = [
    (6, "¡Vamos, mi poderoso Pokémon de tipo Bicho!"), 
    (7, "¡Vamos, mi poderoso Pokémon de tipo Bicho!"), 
    (10, "Ya sé que es una frase manida, pero... Donde quiera que hay luz, también hay sombras..."), 
    (11, "Ya sé que es una frase manida, pero... Donde quiera que hay luz, también hay sombras..."), 
    (12, "¡GRRR! ¿Qué te pareció eso?"), 
    (13, "¡GRRRR! ¿Qué te pareció eso?"), 
    (14, "¡Mira a mi Pokémon tan mono!"), 
    (15, "¡Mira a mi Pokémon tan mono!"), 
    (16, "Estos músculos no son solo para impresionar."), 
    (17, "Estos músculos no son solo para impresionar."), 
    (18, "¿Sabes lo caliente que puede llegar a ser el aliento de fuego de los Pokémon?"), 
    (19, "¿Sabes lo caliente que puede llegar a ser el aliento de fuego de los Pokémon?"), 
    (20, "¡Mis Pokémon pájaro quieren combatir contigo!"), 
    (21, "¡Mis Pokémon pájaro quieren combatir contigo!"), 
    (22, "¡No nos vaciles!"), 
    (23, "¡No nos vaciles!"), 
    (24, "¡Haré que te comas el polvo!"), 
    (25, "¡Haré que te comas el polvo!"), 
    (26, "El frío puede paralizarte, ¿no lo sabes?"), 
    (27, "El frío puede paralizarte, ¿no lo sabes?"), 
    (28, "¡No eres rival para mi voluntad de hierro!"), 
    (29, "¡No eres rival para mi voluntad de hierro!"), 
    (30, "Normal no significa débil. "), 
    (31, "Normal no significa débil."), 
    (32, "¡En posición y listo para atacar!"), 
    (33, "¡En posición y listo para atacar!"), 
    (34, "¿Te asustan los psíquicos que usan un poder invisible?"), 
    (35, "¿Te asustan los psíquicos que usan un poder invisible?"), 
    (36, "¡Soy fuerte como una roca!"), 
    (37, "¡Soy fuerte como una roca!"), 
    (38, "¡Estas aguas son traicioneras!"), 
    (39, "¡Estas aguas son traicioneras!"), 
    (47, "Ja, ja, ja..."), 
    (48, "Ja, ja, ja..."), 
    (49, "¡Prepárate para alucinar!"), 
    (50, "¡Prepárate para alucinar!"), 
    (4, [
        "Ganar es para los ganadores.",
        "No te molestes, ya he ganado.",
        "¡Prepárate para la derrota!"
    ]),
    (5, [
        "Ganar es para los ganadores.",
        "No te molestes, ya he ganado.",
        "¡Prepárate para la derrota!"
    ]),
    (42, [
        "Es hora de que aprendas cuál es tu lugar en el mundo.",
        "Yo nunca pierdo.",
        "Prepárate para un buen escarmiento.",
        "La arrogancia conduce al fracaso.",
        "Tu derrota viene volando."
    ]),
    (41, [
        "Mi fuerza proviene de mi lealtad al Team GO Rocket.",
        "Haré cualquier cosa por el Team GO Rocket.",
        "Le debo la vida al jefe. Haría cualquier cosa por él.",
        "El Team GO Rocket me salvó. ¡Es hora de devolver el favor!",
        "Añade mi nombre a tu lista de debilidades."
    ]),
    (44, [
        "No toleraré tu intromisión.",
        "No puedes detenerme..., pero me divierte tu intento.",
        "Tu profesor no te ha preparado para lo que está por venir.",
        "Has llegado hasta aquí. Déjame ver cuán fuerte eres.",
        "Nunca vencerás al Team GO Rocket."
    ]),
    (45, [
        "Te engañé, papanatas.",
        "Qué, ¿pensabas que encontrar al jefe iba a ser tan fácil?",
        "¡No me puedo creer que hayas caído en la trampa!",
        "¡Te voy a destruir en el nombre del jefe!",
        "¡Nunca llegarás hasta él!",
        "Me gusta ver tu decepción.",
        "Quieres llegar hasta el jefe, ¿eh? ¡Tendrás que derrotarme!",
        "¡Haré cualquier cosa para proteger al jefe!",
        "¡Te han engañado, canalla!",
        "¡Piérdete! Nunca lo encontrarás."
    ]),
    (46, [
        "Te engañé, papanatas.",
        "Qué, ¿pensabas que encontrar al jefe iba a ser tan fácil?",
        "¡No me puedo creer que hayas caído en la trampa!",
        "¡Te voy a destruir en el nombre del jefe!",
        "¡Nunca llegarás hasta él!",
        "Me gusta ver tu decepción.",
        "Quieres llegar hasta el jefe, ¿eh? ¡Tendrás que derrotarme!",
        "¡Haré cualquier cosa para proteger al jefe!",
        "¡Te han engañado, canalla!",
        "¡Piérdete! Nunca lo encontrarás."
    ]),
    (43, [
        "Te envidio, ¡tienes la oportunidad de combatir conmigo!",
        "Este será un combate que estoy segura que nunca olvidarás.",
        "Ya lo sabes, pero no tienes ninguna posibilidad.",
        "No puedes igualar mi destreza, amorcito.",
        "¡Espero que te guste el sabor del fracaso!"
    ])
]

# Convertir la lista de tuplas en un diccionario
frase = dict(frase_list)


# Hacer la solicitud a la API
url = "https://rocket.malte.im/api/characters?hours=24"
response = requests.get(url)

# Verificar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    data = response.json()  # Convertir la respuesta a JSON
    # Recorrer la lista de personajes y agregar el tipo y la frase correspondiente
    for character in data["characters"]:
        character_value = character["character"]["value"]
        if character_value in typo:
            character["character"]["typo"] = typo[character_value]
        else:
            character["character"]["typo"] = "Desconocido"
        
        if character_value in frase:
            if isinstance(frase[character_value], list):
                character["character"]["frase"] = "\n".join(frase[character_value])
            else:
                character["character"]["frase"] = frase[character_value]
        else:
            character["character"]["frase"] = "Frase no definida"
        
        # Verificar si el personaje tiene una clave 'team'
        if "team" in character:
            team_pokemon_values = [team_member["pokemon"]["value"] for team_member in character["team"]]
            # Comprobar si el valor del pokemon en 'rewards' coincide con alguno en 'team'
            for team_member in character["team"]:
                if team_member["form"]["value"] == 0:
                    team_member["img"] = team_member["pokemon"]["value"]
                else:
                    team_member["img"] = f"{team_member['pokemon']['value']}_f{team_member['form']['value']}"
                team_member["capturable"] = "si" if any(reward["pokemon"]["value"] == team_member["pokemon"]["value"] for reward in character["rewards"]) else "no"
                team_member["shiny"] = "si" if any(reward["pokemon"]["value"] == team_member["pokemon"]["value"] and reward["shinies"] != 0 for reward in character["rewards"]) else "no"
        
        # Eliminar la clave "rewards" si existe
        if "rewards" in character:
            del character["rewards"]

    # Crear un nuevo diccionario con la estructura deseada
    new_json = {
        "total": data["total"],
        "since": data["since"],
        "characters": data["characters"]
    }
    # Guardar el nuevo JSON en un archivo en la carpeta temporal
    with open(json_file_path, "w") as json_file:
        json.dump(new_json, json_file, indent=4)
    print("JSON creado exitosamente en la carpeta temporal.")
else:
    print("Error al obtener datos de la API:", response.status_code)
