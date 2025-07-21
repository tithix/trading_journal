import requests
import json
import re
from datetime import datetime
import schedule
import time
import pytz
import threading

def fetch_calendar_data():
    """
    Récupère les données du calendrier économique pour la semaine en cours.
    """
    url = 'https://nfs.faireconomy.media/ff_calendar_thisweek.json'
    try:
        response = requests.get(url)
        response.raise_for_status()
        print("Données de la semaine actuelle récupérées avec succès.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération des données : {e}")
        return None

def update_html_file(data):
    """Met à jour le fichier HTML avec les nouvelles données JSON."""
    if not data:
        print("Aucune donnée à mettre à jour.")
        return

    html_path = 'webapp/journal_v2.html'
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Formater les données en une chaîne JSON pour JavaScript
        json_string = json.dumps(data)
        
        # Remplacer l'ancienne variable economicCalendarJsonData par la nouvelle
        # Utilisation d'une expression régulière pour être robuste
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
    except Exception as e:
        print(f"Une erreur est survenue lors de la mise à jour du fichier HTML : {e}")

def job():
    """Tâche à exécuter."""
    print("Exécution de la tâche de mise à jour du calendrier...")
    calendar_data = fetch_calendar_data()
    if calendar_data:
        update_html_file(calendar_data)
        print("Mise à jour terminée.")
    else:
        print("La mise à jour a échoué car les données n'ont pas pu être récupérées.")

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

if __name__ == '__main__':
    job()
