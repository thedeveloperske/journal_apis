from sqlalchemy.orm import Session
from passlib.context import CryptContext
import logging

from app import schemas
from . import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configure logging for development
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# http://127.0.0.1:8000/auth/register
# http://127.0.0.1:8000/auth/login

# USER
def create_user(db: Session, user: schemas.UserCreate):
    logger.debug(f"Creating user with email: {user.email}")
    hashed_pass = pwd_context.hash(user.hashed_password)
    db_user = models.User(email=user.email, hashed_password=hashed_pass, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"User created with id: {db_user.id}")
    return db_user

def get_user(db: Session, user_id: int):
    logger.debug(f"Fetching user with id: {user_id}")
    return db.query(models.User).filter(models.User.id == user_id).first()

def delete_user(db: Session, user_id: int):
    logger.debug(f"Deleting user with id: {user_id}")
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    logger.info(f"User deleted with id: {user_id}")
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 10):
    logger.debug(f"Fetching users, skip={skip}, limit={limit}")
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user_by_email(db: Session, email: str):
    logger.debug(f"Fetching user by email: {email}")
    return db.query(models.User).filter(models.User.email == email).first()

# ITEMS
def get_item(db: Session, item_id: int):
    logger.debug(f"Fetching item with id: {item_id}")
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 10):
    logger.debug(f"Fetching items, skip={skip}, limit={limit}")
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_item(db: Session, item: schemas.ItemCreate):
    logger.debug(f"Creating item with title: {item.title} for owner_id: {item.owner_id}")
    db_item = models.Item(
        title=item.title,
        category=item.category,
        mood=item.mood,
        content=item.content,
        owner_id=item.owner_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    logger.info(f"Item created with id: {db_item.id}")
    return db_item

def delete_item(db: Session, item_id: int):
    logger.debug(f"Deleting item with id: {item_id}")
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    db.delete(db_item)
    db.commit()
    logger.info(f"Item deleted with id: {item_id}")
    return db_item