import os
from fastapi import APIRouter
from elasticsearch import Elasticsearch

router = APIRouter(tags=['10 latest CVEs'])

ELASTIC_URL = os.getenv("ELASTIC_URL")
API_KEY = os.getenv("API_KEY")
client = Elasticsearch(ELASTIC_URL, api_key=API_KEY)

@router.get("/get/new")
def latest_cve():

    # Пошук всіх документів в Elasticsearch.
    # Встановлено обмеження на 10 документів.
    # Немає потреби сортувати за датою, тому що 
    # останні CVE є найновішими за замовчуванням
    response = client.search(index='first_index', body={
        "query": {"match_all": {}},
        "size": 10
    })

    hits = response.get("hits", {}).get("hits", [])
    return [doc["_source"] for doc in hits]  