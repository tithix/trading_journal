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

    html_path = 'economic_calendar.html'
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Formater les données en une chaîne JSON pour JavaScript
        json_string = json.dumps(data, indent=None, ensure_ascii=False)
        
        # Remplacer l'ancienne variable jsonData par la nouvelle
        # Utilisation d'une expression régulière pour être robuste
        new_content = re.sub(
            r'const jsonData = .*?;',
            f'const jsonData = {json_string};',
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
    # Planifier la tâche pour s'exécuter tous les lundis à 01:00 EST
    est = pytz.timezone('US/Eastern')
    
    # Note: `schedule` utilise l'heure locale du serveur. 
    # Pour une exécution précise basée sur EST, il faudrait une logique plus complexe
    # ou un service comme cron qui gère mieux les fuseaux horaires.
    # Pour cet exemple, nous planifions à une heure fixe.
    # L'utilisateur devra s'assurer que le serveur est synchronisé.
    
    schedule.every().monday.at("01:00").do(run_threaded, job)
    
    print("Le script de mise à jour est en cours d'exécution.")
    print("La mise à jour est planifiée pour chaque lundi à 01:00 EST.")
    
    # Exécuter la tâche une fois au démarrage
    run_threaded(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
