from datetime import datetime
from bson.objectid import ObjectId
from db import medicines_collection
def add_medicine(name, generic, company, category, quantity, price, expiry_date, description):
    medicine = {
        "name": name,
        "generic": generic,
        "company": company,
        "category": category,
        "quantity": int(quantity),
        "price": float(price),
        "expiry_date": expiry_date,
        "description": description
    }
    medicines_collection.insert_one(medicine)
def get_all_medicines():
    return list(medicines_collection.find().sort("name", 1))
def get_medicine_by_id(medicine_id):
    return medicines_collection.find_one({"_id": ObjectId(medicine_id)})
def search_medicines(keyword):
    keyword = keyword.strip()
    return list(medicines_collection.find({
        "$or": [
            {"name": {"$regex": keyword, "$options": "i"}},
            {"generic": {"$regex": keyword, "$options": "i"}},
            {"company": {"$regex": keyword, "$options": "i"}},
            {"category": {"$regex": keyword, "$options": "i"}}
        ]
    }))
def update_medicine(medicine_id, name, generic, company, category, quantity, price, expiry_date, description):
    new_data = {
        "name": name,
        "generic": generic,
        "company": company,
        "category": category,
        "quantity": int(quantity),
        "price": float(price),
        "expiry_date": expiry_date,
        "description": description
    }
    medicines_collection.update_one(
        {"_id": ObjectId(medicine_id)},
        {"$set": new_data}
    )
def delete_medicine(medicine_id):
    medicines_collection.delete_one({"_id": ObjectId(medicine_id)})
def get_low_stock_medicines(limit=10):
    return list(medicines_collection.find({"quantity": {"$lt": limit}}).sort("quantity", 1))
def get_expired_medicines():
    today = datetime.today().strftime("%Y-%m-%d")
    return list(medicines_collection.find({"expiry_date": {"$lt": today}}).sort("expiry_date", 1))
