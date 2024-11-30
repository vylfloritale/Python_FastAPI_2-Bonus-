import os
from fastapi import APIRouter
from elasticsearch import Elasticsearch

router = APIRouter(tags=['CVEs that contain the keyword'])

ELASTIC_URL = os.getenv("ELASTIC_URL")
API_KEY = os.getenv("API_KEY")
client = Elasticsearch(ELASTIC_URL, api_key=API_KEY)

@router.get("/get")
def cve_by_keyword(keywordSearch):

    # Виконання запиту до Elasticsearch для пошуку документів, 
    # де shortDescription містить ключове слово
    response = client.search(index='first_index', body={
            "query": {
                "query_string": {
                    "query": f"*{keywordSearch}*"
                }
            },
            "size": 10000
    })

    hits = response.get("hits", {}).get("hits", [])
    return [doc["_source"] for doc in hits]  