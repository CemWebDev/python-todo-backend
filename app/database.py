from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/todo_app")

try:
    client = MongoClient(MONGO_URI)
    db = client.todo_app
    users_collection = db.users
    todos_collection = db.todos
    client.admin.command('ping')
    
except Exception as e:
    raise