from typing import List
from fastapi import APIRouter, Path, HTTPException, status, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from todos_app.database import get_db
from todos_app.models import Todo, User
from todos_app.routers.auth import get_current_user

class TodoRequest(BaseModel):
    """
    Pydantic model for Todo request body validation.
    """
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    priority: int = Field(gt=0, lt=6, description="Priority between 1-5")
    completed: bool = Field(default=False)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "My Todo",
                "description": "My Todo Description",
                "priority": 1,
                "completed": False
            }
        }
    }

class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: int
    completed: bool
    owner: int

    model_config = {
        "from_attributes": True
    }

router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)

@router.get("", status_code=status.HTTP_200_OK, response_model=List[TodoResponse])
async def read_all_todos(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get all todos for the authenticated user.
    """
    try:
        return db.query(Todo).filter(Todo.owner == user.id).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{todo_id}", status_code=status.HTTP_200_OK, response_model=TodoResponse)
async def read_todo_by_id(user: User = Depends(get_current_user), 
                          todo_id: int = Path(gt=0), 
                          db: Session = Depends(get_db)):
    """
    Get a specific todo by ID for the authenticated user.
    """
    try:
        todo = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner == user.id).first()
        if todo is not None:
            return todo
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found.")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_todo(todo_request: TodoRequest, 
                      user: User = Depends(get_current_user), 
                      db: Session = Depends(get_db)):
    """
    Create a new todo for the authenticated user.
    """
    try:
        todo_model = Todo(**todo_request.model_dump(), owner=user.id)
        db.add(todo_model)
        db.commit()
        db.refresh(todo_model)
        return {"message": "Todo created successfully.", "todo": todo_model}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(todo_request: TodoRequest, 
                      user: User = Depends(get_current_user), 
                      todo_id: int = Path(gt=0), 
                      db: Session = Depends(get_db)):
    """
    Update an existing todo for the authenticated user.
    """
    try:
        todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner == user.id).first()
        if todo_model is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found.")
        
        todo_model.title = todo_request.title
        todo_model.description = todo_request.description
        todo_model.priority = todo_request.priority
        todo_model.completed = todo_request.completed
        
        db.add(todo_model)
        db.commit()
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: User = Depends(get_current_user), 
                      todo_id: int = Path(gt=0), 
                      db: Session = Depends(get_db)):
    """
    Delete a specific todo by ID for the authenticated user.
    """ 
    try:
        todo_model = db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner == user.id).first()
        if todo_model is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found.")
        
        db.delete(todo_model)
        db.commit()
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
