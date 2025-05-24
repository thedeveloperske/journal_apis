from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, orm
import passlib.hash as _hash
import datetime as dt

from app.database import Base

class User(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True, index=True)
  email = Column(String(255), index=True, unique=True) 
  hashed_password = Column(String(255)) 
  name = Column(String(255), nullable=True)  

  items = orm.relationship("Item", back_populates="owner")

  def verify_password(self, password: str):
    return _hash.bcrypt.verify(password, self.hashed_password)

class Item(Base):
  __tablename__ = "items"
  id = Column(Integer, primary_key=True, index=True)
  title = Column(String(255), index=True)
  category = Column(String(255), default="")
  mood = Column(String(255), default="")
  content = Column(String(255), default="")
  owner_id = Column(Integer, ForeignKey("users.id"))
  date_created = Column(DateTime, default=dt.datetime.utcnow)
  date_updated = Column(DateTime, default=dt.datetime.utcnow)

  owner = orm.relationship("User", back_populates="items")