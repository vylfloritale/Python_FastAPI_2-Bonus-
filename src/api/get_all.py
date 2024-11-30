import os
from fastapi import APIRouter
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta

router = APIRouter(tags=['Up to 40 CVE in the last 5 days'])

ELASTIC_URL = os.getenv("ELASTIC_URL")
API_KEY = os.getenv("API_KEY")
client = Elasticsearch(ELASTIC_URL, api_key=API_KEY)

@router.get("/get/all")
def last_five_days_cve():
    # Отримання поточного часу
    current_date = datetime.now()

    # Отримання дати, яка була 5 днів тому
    last_five_days = current_date - timedelta(days=5)

    # Форматування дати last_five_days до формату YYYY-MM-DD
    last_five_days_format = last_five_days.strftime('%Y-%m-%d')

    # Пошук документів в Elasticsearch, де "dateAdded" >= "last_five_days_format"
    response = client.search(index='first_index', body={
        "query": {
            "range": {
                "dateAdded": {
                    "gte": last_five_days_format
                }
            }
        },
        "size": 40  # кількість повернутих результатів до 40
    })

    # Отримання вмісту response уникаючи службової інформації
    hits = response.get("hits", {}).get("hits", [])

    # Повертається тільки вміст документа
    return [doc["_source"] for doc in hits]  