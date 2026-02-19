from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone,timedelta
from jose import jwt, JWTError
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
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

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "mytoken",
                "token_type": "bearer"
            }
        }
    }

SECRET_KEY = "hello-world-2026-learn-fastapi"       # TODO: Move this to environment variables
ALGORITHM = "HS256"                                 # TODO: Move this to environment variables
ACCESS_TOKEN_EXPIRE_MINUTES = 120                   # TODO: Move this to environment variables

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT token for a user.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode a JWT token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return payload
    except JWTError:
        return None

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Get the current user from the token.
    """
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")
    user = db.query(User).filter(User.username == payload.get("sub")).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user

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

@router.post("/token", status_code=status.HTTP_200_OK, response_model=TokenResponse)
async def token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Get JWT token for a user.
    """
    try:
        user = db.query(User).filter(User.username == form_data.username).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        if not user.verify_password(form_data.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password.")

        # Generate JWT token
        payload = {"sub": user.username}
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(payload, access_token_expires)
        return TokenResponse(access_token=access_token, token_type="bearer")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/me", status_code=status.HTTP_200_OK)
async def me(user: User = Depends(get_current_user)):
    """
    Get the current user.
    """
    return { "username": user.username, "id": user.id, "is_active": user.is_active }
