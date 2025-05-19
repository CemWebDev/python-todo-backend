from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from bson import ObjectId
from typing import List

from app.database import todos_collection
from app.models.todo import Todo, TodoCreate, TodoUpdate
from app.auth.auth import get_api_key

router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)

@router.post("", response_model=Todo)
async def create_todo(todo: TodoCreate, current_user: dict = Depends(get_api_key)):
    todo_data = todo.dict()
    todo_data.update({
        "user_id": current_user["id"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })
    
    try:
        result = todos_collection.insert_one(todo_data)
        
        created_todo = todo_data.copy()
        created_todo["id"] = str(result.inserted_id)
        
        return created_todo
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.get("", response_model=List[Todo])
async def read_todos(current_user: dict = Depends(get_api_key)):
    todos = []
    for todo in todos_collection.find({"user_id": current_user["id"]}):
        todo_dict = dict(todo)
        todo_dict["id"] = str(todo_dict.pop("_id"))
        todos.append(todo_dict)
    
    return todos

@router.get("/{todo_id}", response_model=Todo)
async def read_todo(todo_id: str, current_user: dict = Depends(get_api_key)):
    try:
        todo = todos_collection.find_one({"_id": ObjectId(todo_id), "user_id": current_user["id"]})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid todo ID."
        )
        
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found."
        )
    
    todo_dict = dict(todo)
    todo_dict["id"] = str(todo_dict.pop("_id"))
    
    return todo_dict

@router.put("/{todo_id}", response_model=Todo)
async def update_todo(todo_id: str, todo: TodoUpdate, current_user: dict = Depends(get_api_key)):
    try:
        existing_todo = todos_collection.find_one({"_id": ObjectId(todo_id), "user_id": current_user["id"]})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid todo ID."
        )
        
    if existing_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found."
        )
    
    todo_data = todo.dict()
    todo_data["updated_at"] = datetime.utcnow()
    
    todos_collection.update_one(
        {"_id": ObjectId(todo_id)},
        {"$set": todo_data}
    )
    
    updated_todo = todos_collection.find_one({"_id": ObjectId(todo_id)})
    updated_todo_dict = dict(updated_todo)
    updated_todo_dict["id"] = str(updated_todo_dict.pop("_id"))
    
    return updated_todo_dict

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: str, current_user: dict = Depends(get_api_key)):
    try:
        existing_todo = todos_collection.find_one({"_id": ObjectId(todo_id), "user_id": current_user["id"]})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid todo ID."
        )
        
    if existing_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found."
        )
    
    todos_collection.delete_one({"_id": ObjectId(todo_id)})
    
    return None