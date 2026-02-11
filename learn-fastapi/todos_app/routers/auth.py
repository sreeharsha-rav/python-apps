from pydantic import BaseModel, Field
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from todos_app.database import get_db
from todos_app.models import User

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=3, max_length=100)

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "myuser",
                "password": "mypassword"
            }
        }
    }

class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=3, max_length=100)

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "myuser",
                "password": "mypassword"
            }
        }
    }

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(register_request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    try:
        new_user = User(username=register_request.username)
        new_user.password = register_request.password
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User created successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    """
    Login a user.
    """
    try:
        user = db.query(User).filter(User.username == login_request.username).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        if not user.verify_password(login_request.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password.")
        return {"message": "Login successful."}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
