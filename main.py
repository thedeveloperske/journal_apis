from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from app import schemas, database, crud, auth
from app.auth import Token
from app.database import engine, Base
from fastapi import Depends, HTTPException, status
from datetime import timedelta
from fastapi import Body
from pydantic import BaseModel
from app.models import Item
from fastapi import Query

app = FastAPI(
  title="Journal Apis for the Shamiri Institute case study",
  description="Inspired by the yesterday.today.tomorrow event at the gathering at the trademark",
  version="1.0.0"
)

# Create tables
Base.metadata.create_all(bind=engine)

# Allow CORS for frontend
origins = [
  "http://localhost:3000",
  "http://localhost:8081",
  "http://localhost:8000"
]

app.add_middleware(
  CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
  return{"Hello":"World"}

# USERS
@app.post("/users",response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
  existing_email = crud.get_user_by_email(db, user.email)
  if existing_email:
    raise HTTPException(status_code=400, detail="Email already registered")
  return crud.create_user(db=db, user=user)   

@app.get("/users", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
  items = crud.get_users(db, skip=skip, limit=limit)
  return items

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.delete_user(db=db, user_id=user_id)

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/token", response_model=Token)
async def login_for_access_token(
    login_req: LoginRequest = Body(...),
    db: Session = Depends(database.get_db)
):
    user = auth.authenticate_user(db, login_req.email, login_req.password)
    if not user:
        raise HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
           detail="Incorrect email or password",
           headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user=Depends(auth.get_current_active_user)):
    return current_user

# ITEMS
@app.post("/items", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(database.get_db)):
    return crud.create_item(db=db, item=item)

@app.get("/items", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
  items = crud.get_items(db, skip=skip, limit=limit)
  return items

@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(database.get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.delete("/items/{item_id}", response_model=schemas.Item)
def delete_item(item_id: int, db: Session = Depends(database.get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return crud.delete_item(db=db, item_id=item_id)

@app.get("/items/search", response_model=list[schemas.ItemOut])
def search_items_by_title(title: str = Query(...), db: Session = Depends(database.get_db)):
    return db.query(Item).filter(Item.title.ilike(f"%{title}%")).all()

@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(database.get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    # Update fields
    db_item.title = item.title
    db_item.category = item.category
    db_item.mood = item.mood
    db_item.content = item.content
    db_item.owner_id = item.owner_id
    db.commit()
    db.refresh(db_item)
    return db_item

# ANALYTICS