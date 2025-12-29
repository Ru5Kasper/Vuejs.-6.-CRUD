from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from slugify import slugify
import os

# Настройка базы данных (SQLite в памяти для простоты)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"  # Для тестирования в памяти

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Модели базы данных
class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    posts = relationship("Post", back_populates="category", cascade="all, delete-orphan")

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    content = Column(Text, nullable=False)
    image_url = Column(String, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    category = relationship("Category", back_populates="posts")

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Pydantic модели
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    posts_count: int = 0
    
    class Config:
        from_attributes = True

class PostBase(BaseModel):
    name: str
    content: str
    image_url: Optional[str] = None
    category_id: int

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    name: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = None

class PostResponse(PostBase):
    id: int
    slug: str
    created_at: datetime
    category: Optional[CategoryResponse] = None
    
    class Config:
        from_attributes = True

# FastAPI приложение
app = FastAPI(title="Blog API", version="1.0.0")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Vue dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Зависимость для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Вспомогательные функции
def generate_slug(name: str, db: Session) -> str:
    base_slug = slugify(name)
    slug = base_slug
    counter = 1
    
    # Проверяем уникальность slug
    while db.query(Post).filter(Post.slug == slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    return slug

# API endpoints
@app.get("/")
async def root():
    return {"message": "Blog API is running"}

# Категории
@app.get("/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    
    # Добавляем количество постов для каждой категории
    result = []
    for category in categories:
        category_dict = CategoryResponse.from_orm(category).dict()
        category_dict['posts_count'] = len(category.posts)
        result.append(category_dict)
    
    return result

@app.get("/categories/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    category_dict = CategoryResponse.from_orm(category).dict()
    category_dict['posts_count'] = len(category.posts)
    
    return category_dict

@app.post("/categories", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли категория с таким именем
    db_category = db.query(Category).filter(Category.name == category.name).first()
    if db_category:
        raise HTTPException(status_code=400, detail="Category with this name already exists")
    
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    category_dict = CategoryResponse.from_orm(db_category).dict()
    category_dict['posts_count'] = 0
    
    return category_dict

@app.put("/categories/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Проверяем, существует ли другая категория с таким именем
    existing_category = db.query(Category).filter(
        Category.name == category.name,
        Category.id != category_id
    ).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Category with this name already exists")
    
    db_category.name = category.name
    db.commit()
    db.refresh(db_category)
    
    category_dict = CategoryResponse.from_orm(db_category).dict()
    category_dict['posts_count'] = len(db_category.posts)
    
    return category_dict

@app.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Проверяем, есть ли связанные посты
    if len(db_category.posts) > 0:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot delete category with {len(db_category.posts)} posts. Delete posts first."
        )
    
    db.delete(db_category)
    db.commit()
    
    return {"message": "Category deleted successfully"}

# Посты
@app.get("/posts", response_model=List[PostResponse])
def get_posts(
    search: Optional[str] = Query(None, description="Search by post name"),
    db: Session = Depends(get_db)
):
    query = db.query(Post).join(Category, isouter=True)
    
    if search:
        query = query.filter(Post.name.ilike(f"%{search}%"))
    
    posts = query.order_by(Post.created_at.desc()).all()
    return posts

@app.get("/posts/{slug}", response_model=PostResponse)
def get_post(slug: str, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.slug == slug).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.post("/posts", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    # Проверяем существование категории
    category = db.query(Category).filter(Category.id == post.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Генерируем slug
    slug = generate_slug(post.name, db)
    
    db_post = Post(
        **post.dict(),
        slug=slug
    )
    
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.put("/posts/{slug}", response_model=PostResponse)
def update_post(slug: str, post: PostUpdate, db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.slug == slug).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Если изменяется категория, проверяем её существование
    if post.category_id is not None:
        category = db.query(Category).filter(Category.id == post.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    
    # Обновляем поля
    update_data = post.dict(exclude_unset=True)
    
    # Если изменяется имя, обновляем slug
    if 'name' in update_data and update_data['name'] != db_post.name:
        update_data['slug'] = generate_slug(update_data['name'], db)
    
    for field, value in update_data.items():
        setattr(db_post, field, value)
    
    db.commit()
    db.refresh(db_post)
    return db_post

@app.delete("/posts/{slug}")
def delete_post(slug: str, db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.slug == slug).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db.delete(db_post)
    db.commit()
    
    return {"message": "Post deleted successfully"}

# Добавим некоторые начальные данные
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    
    # Создаем тестовые категории, если их нет
    if db.query(Category).count() == 0:
        categories = [
            Category(name="Программирование"),
            Category(name="Дизайн"),
            Category(name="Маркетинг"),
            Category(name="Образование"),
            Category(name="Новости"),
        ]
        
        for category in categories:
            db.add(category)
        
        db.commit()
        
        # Создаем тестовые посты
        programming_category = db.query(Category).filter(Category.name == "Программирование").first()
        
        posts = [
            Post(
                name="Введение в Vue.js",
                slug="vvedenie-v-vue-js",
                content="Vue.js - это прогрессивный фреймворк для создания пользовательских интерфейсов.",
                image_url="https://vuejs.org/images/logo.png",
                category_id=programming_category.id
            ),
            Post(
                name="React vs Vue: что выбрать?",
                slug="react-vs-vue-chto-vybrat",
                content="Сравнение двух популярных фреймворков для фронтенд-разработки.",
                image_url="https://upload.wikimedia.org/wikipedia/commons/a/a7/React-icon.svg",
                category_id=programming_category.id
            ),
        ]
        
        for post in posts:
            db.add(post)
        
        db.commit()
    
    db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)