import requests
import json
import re

def fetch_and_update():
    """
    Récupère les données du calendrier économique et met à jour le fichier HTML.
    """
    # 1. Récupérer les données
    url = 'https://nfs.faireconomy.media/ff_calendar_thisweek.json'
    try:
        response = requests.get(url)
        response.raise_for_status()
        print("Données de la semaine actuelle récupérées avec succès.")
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération des données : {e}")
        return

    # 2. Mettre à jour le fichier HTML
    # Note: Le chemin pointe maintenant vers 'index.html' à la racine
    html_path = 'index.html'
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()

        json_string = json.dumps(data)
        
        # Remplacer l'ancienne variable de données
        new_content = re.sub(
            r'const economicCalendarJsonData = .*?;',
            f'const economicCalendarJsonData = {json_string};',
            content,
            flags=re.DOTALL
        )

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Le fichier '{html_path}' a été mis à jour avec succès.")

    except FileNotFoundError:
        print(f"Erreur : le fichier '{html_path}' n'a pas été trouvé.")
        print("Assurez-vous que le fichier 'index.html' existe bien à la racine du projet.")
    except Exception as e:
        print(f"Une erreur est survenue lors de la mise à jour du fichier HTML : {e}")

if __name__ == '__main__':
    fetch_and_update()
