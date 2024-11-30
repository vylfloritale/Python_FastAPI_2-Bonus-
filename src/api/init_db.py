import os
import requests
from fastapi import APIRouter
from elasticsearch import Elasticsearch

router = APIRouter(tags=['Get all CVE from Elasticsearch'])

@router.get("/init-db")
def init_db():

    # Завантаження JSON-файла
    URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

    # Отримання даних з URL та перетворення їх у JSON-формат
    response = requests.get(URL).json()
        
    # Пошук даних, вони мають містити ключ "vulnerabilities", 
    # якщо йог не буде, то повернеться порожній список
    vulnerabilities = response.get("vulnerabilities", [])

    ELASTIC_URL = os.getenv("ELASTIC_URL")
    API_KEY = os.getenv("API_KEY")
    client = Elasticsearch(ELASTIC_URL, api_key=API_KEY)

    # Функція для завантаження даних у Elasticsearch
    def load_data():
        
        # Перебір коженого елемента списка vulnerabilities
        for vulnerability in vulnerabilities:

            # Реалізована обробка помилок для того, щоб у разі, 
            # наприклад, відстуності cveID, програма не звершила роботу
            try:
                # Отримується значення cveID, воно передається як id документа
                # Сам документ це елемент списку vulnerabilities
                cve_id = vulnerability.get("cveID")

                # Тобто, кожен переданий документ в Elasticsearch буде 
                # мати унікальний id та вміст 
                client.index(index='first_index', id=cve_id, document=vulnerability)
            
            # У випадку помилки виводиться повідомлення, задане в цьому коді, 
            # cveID або "unknown", а також текст самої помилки
            except Exception as e:
                print(f"Error while indexing CVE {vulnerability.get('cveID', 'unknown')}: {e}")
    
    # Завантаження даних з vulnerabilities у базу даних Elasticsearch
    load_data()

    # Завершення виконання функції обробки запиту /init-db
    return
