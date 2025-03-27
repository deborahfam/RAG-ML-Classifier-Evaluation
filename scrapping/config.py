import pymongo, os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = pymongo.MongoClient(MONGO_URI)
db = client["rag_db"]
collection = db["docs"]

models_dict = {
    "Llama V3 70B Instruct": "accounts/fireworks/models/llama-v3-70b-instruct",
    "Mixtral 8x7B Instruct": "accounts/fireworks/models/mixtral-8x7b-instruct",
    "FireFunction V1": "accounts/fireworks/models/firefunction-v1"
}
tokens_dict = {
    "Llama V3 70B Instruct": "4,096",
    "Mixtral 8x7B Instruct": "8,000",
    "FireFunction V1": "4,096"
}
