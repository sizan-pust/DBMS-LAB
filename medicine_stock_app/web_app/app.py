from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["medicine_stock_db"]
medicines = db["medicines"]
@app.route("/", methods=["GET", "POST"])
def home():
    page = request.args.get("page", "add")
    edit_medicine = None
    medicine_list = []
    if request.method == "POST":
        action = request.form["action"]
        if action == "add":
            medicine = {
                "name": request.form["name"],
                "generic": request.form["generic"],
                "company": request.form["company"],
                "category": request.form["category"],
                "quantity": int(request.form["quantity"]),
                "price": float(request.form["price"]),
                "expiry_date": request.form["expiry_date"],
"description": request.form.get("description", "").strip()
            }

            medicines.insert_one(medicine)
            return redirect("/?page=view")
        
        elif action == "update":
            medicine_id = request.form["medicine_id"]

            updated_medicine = {
                "name": request.form["name"],
                "generic": request.form["generic"],
                "company": request.form["company"],
                "category": request.form["category"],
                "quantity": int(request.form["quantity"]),
                "price": float(request.form["price"]),
                "expiry_date": request.form["expiry_date"],
"description": request.form.get("description", "").strip()
            }

            medicines.update_one(
                {"_id": ObjectId(medicine_id)},
                {"$set": updated_medicine}
            )

            return redirect("/?page=view")

        elif action == "delete":
            medicine_id = request.form["medicine_id"]
            medicines.delete_one({"_id": ObjectId(medicine_id)})
            return redirect("/?page=view")

        elif action == "search":
            keyword = request.form["keyword"]

            medicine_list = list(medicines.find({
                "$or": [
                    {"name": {"$regex": keyword, "$options": "i"}},
                    {"generic": {"$regex": keyword, "$options": "i"}},
                    {"company": {"$regex": keyword, "$options": "i"}},
                    {"category": {"$regex": keyword, "$options": "i"}},
                    {"description": {"$regex": keyword, "$options": "i"}}
                ]
            }))

            page = "search_result"

    if page == "view":
        medicine_list = list(medicines.find())
    elif page == "edit":
        medicine_id = request.args.get("id")
        edit_medicine = medicines.find_one({"_id": ObjectId(medicine_id)})
    elif page == "low":
        medicine_list = list(medicines.find({"quantity": {"$lt": 10}}))
    elif page == "expired":
        today = datetime.today().strftime("%Y-%m-%d")
        medicine_list = list(medicines.find({"expiry_date": {"$lt": today}}))

    return render_template(
        "index.html",
        page=page,
        medicines=medicine_list,
        edit_medicine=edit_medicine
    )
if __name__ == "__main__":
    app.run(debug=True)