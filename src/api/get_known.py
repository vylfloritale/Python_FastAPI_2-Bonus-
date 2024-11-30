import os
from fastapi import APIRouter
from elasticsearch import Elasticsearch

router = APIRouter(tags=['10 known CVEs'])

ELASTIC_URL = os.getenv("ELASTIC_URL")
API_KEY = os.getenv("API_KEY")
client = Elasticsearch(ELASTIC_URL, api_key=API_KEY)

@router.get("/get/known")
def known_cve():

    # Виконання запиту до Elasticsearch для пошуку документів, 
    # де knownRansomwareCampaignUse містить "Known"
    response = client.search(index='first_index', body={
            "query": {
                "bool": {
                    "must": [
                        {"match": {"knownRansomwareCampaignUse": "Known"}}
                    ]
                }
            },
            "size": 10
        }
    )

    hits = response.get("hits", {}).get("hits", [])
    return [doc["_source"] for doc in hits]  