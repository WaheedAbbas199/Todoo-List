from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

app = FastAPI(title="Todo API", version="1.0")

# =======================
# Pydantic Models
# =======================

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=5)
    completed: bool = False

class Todo(TodoCreate):
    id: int
    created_at: datetime


# =======================
# Fake Database
# =======================

todos: List[Todo] = []
todo_id_counter = 1


# =======================
# Create Todo
# =======================

@app.post("/todos", response_model=Todo)
def create_todo(todo: TodoCreate):
    global todo_id_counter

    new_todo = Todo(
        id=todo_id_counter,
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        created_at=datetime.now()
    )

    todos.append(new_todo)
    todo_id_counter += 1

    return new_todo


# =======================
# Get All Todos
# =======================

@app.get("/todos", response_model=List[Todo])
def get_all_todos():
    return todos


# =======================
# Get Single Todo
# =======================

@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


# =======================
# Update Todo
# =======================

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_todo: TodoCreate):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index] = Todo(
                id=todo_id,
                title=updated_todo.title,
                description=updated_todo.description,
                completed=updated_todo.completed,
                created_at=todo.created_at
            )
            return todos[index]

    raise HTTPException(status_code=404, detail="Todo not found")


# =======================
# Delete Todo
# =======================

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(index)
            return {"message": "Todo deleted successfully"}

    raise HTTPException(status_code=404, detail="Todo not found")
