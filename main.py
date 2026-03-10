from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date
import pymongo
from bson import ObjectId


class server(BaseModel):
    vendor: str 
    serial:  str
    arrival_date:  date
    warranty_end_date: date
    part_number: str

app= FastAPI(title="Omer's API", version="2.0.0")
client = pymongo.MongoClient("mongodb://mongodb:27017/")
db=client["inventory"]
collection = db["servers"]


@app.post("/add")
async def create_new_server(item: server): 
    print(f"Saving {item.vendor} with serial {item.serial} to DataBase...")
    item.arrival_date=str(item.arrival_date)
    item.warranty_end_date=str(item.warranty_end_date)
    collection.insert_one(item.model_dump())
    return {"status": "Database updated", "server_serial": item.serial}

@app.get("/get_all")
async def get_all_servers():
    servers_cursor = collection.find({})
    all_servers = list(servers_cursor)
    for server in all_servers:
        server["_id"] = str(server["_id"])
    return all_servers

@app.get("/get_by_id")
async def get_server_by_Id(id: str):
    server = collection.find_one({"_id": ObjectId(id)})
    if server:
        server["_id"] = str(server["_id"]) 
        return server   
    return {"error": f"No server found with document id: {id}"}

@app.delete("/delete/{id}")
async def delete_server(id: str):
        result = collection.delete_one({"_id": ObjectId(id)})   
        if result.deleted_count == 1:
            return {"status": "Success", "message": f"Server with ID {id} has been deleted"}
        return {"status": "Error", "message": "No server found with that ID"}

@app.put("/equipment/{id}")
async def update_full_server(id: str, item: server):
    new_server = item.model_dump()
    new_server["arrival_date"] = str(new_server["arrival_date"])
    new_server["warranty_end_date"] = str(new_server["warranty_end_date"])
    result = collection.replace_one({"_id": ObjectId(id)}, new_server)
    if result.matched_count != 0:
        return {"message": "Server succesfully  updated"}
    return {"error": "Server not found"}

@app.patch("/equipment/{id}")
async def patch_server(id: str, field: dict): 
    if not field:
        return {"error": "Field not provided"}
    if len(field) != 1:
        return {"error": "You must provide exactly one field to update"}
    allowed_fields = ["vendor", "serial", "arrival_date", "warranty_end_date", "part_number"]
    update_key = list(field.keys())[0]
    if update_key not in allowed_fields:
        return {"error": f"Field '{update_key}' is not a valid equipment field"}
    result = collection.update_one({"_id": ObjectId(id)}, {"$set": field})
    return {"message": "Field succesfully  updated"}





        





