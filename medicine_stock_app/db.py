from pymongo import MongoClient
MONGO_URL = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URL)
database = client["medicine_stock_db"]
medicines_collection = database["medicines"]