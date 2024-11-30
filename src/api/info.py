from fastapi import APIRouter

# Створено об'єкт з тегом, який пояснює призначення
router = APIRouter(tags=['Information about the application and the author'])

# Декоратор для /get запиту, він буде доступний за шляхом /info
@router.get("/info")
# Функція, яка повертає вказану інформацію
def info():
    return {
        "application": "CVE Viewer from Elasticsearch",
        "author": "Viktor Yurchyk"
    }