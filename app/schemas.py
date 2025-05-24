from pydantic import BaseModel
import datetime as _dt

class UserBase(BaseModel):
  email: str
  name: str | None = None

class UserCreate(BaseModel):
  email: str
  hashed_password: str
  name: str | None = None

  class Config:
    from_attributes = True

class User(BaseModel):
  email:str
  hashed_password: str
  id: int
  name: str | None = None

  class Config:
    from_attributes = True

class ItemBase(BaseModel):
    title: str
    category: str = ""
    mood: str = ""
    content: str = ""

class ItemCreate(ItemBase):
    owner_id: int
    pass

class Item(ItemBase):
    id: int
    owner_id: int
    date_created: _dt.datetime
    date_updated: _dt.datetime

    class Config:
        from_attributes = True