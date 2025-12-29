from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from slugify import slugify
from contextlib import asynccontextmanager

# Настройка базы данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

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

# Pydantic модели
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    posts_count: int = 0
    
    model_config = ConfigDict(from_attributes=True)

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

# Важная модель для ответа
class PostResponse(BaseModel):
    id: int
    name: str
    content: str
    image_url: Optional[str] = None
    category_id: int
    slug: str
    created_at: datetime
    category: Optional[CategoryBase] = None
    
    model_config = ConfigDict(from_attributes=True)

# Функции для жизненного цикла
@asynccontextmanager
async def lifespan(app: FastAPI):
    # При запуске
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
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
            
            if programming_category:
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
            else:
                print("Категория 'Программирование' не найдена для создания тестовых постов")
    finally:
        db.close()
    
    yield
    
    # При завершении
    # Можно добавить логику очистки при необходимости

# FastAPI приложение
app = FastAPI(title="Blog API", version="1.0.0", lifespan=lifespan)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все источники для разработки
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
    
    result = []
    for category in categories:
        category_dict = {
            "id": category.id,
            "name": category.name,
            "created_at": category.created_at,
            "posts_count": len(category.posts)
        }
        result.append(category_dict)
    
    return result

@app.get("/categories/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return {
        "id": category.id,
        "name": category.name,
        "created_at": category.created_at,
        "posts_count": len(category.posts)
    }

@app.post("/categories", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    # Проверяем, существует ли категория с таким именем
    db_category = db.query(Category).filter(Category.name == category.name).first()
    if db_category:
        raise HTTPException(status_code=400, detail="Category with this name already exists")
    
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return {
        "id": db_category.id,
        "name": db_category.name,
        "created_at": db_category.created_at,
        "posts_count": 0
    }

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
    
    db_category.name = category.name # pyright: ignore[reportAttributeAccessIssue]
    db.commit()
    db.refresh(db_category)
    
    return {
        "id": db_category.id,
        "name": db_category.name,
        "created_at": db_category.created_at,
        "posts_count": len(db_category.posts)
    }

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
    
    # Создаем response
    result = []
    for post in posts:
        post_dict = {
            "id": post.id,
            "name": post.name,
            "content": post.content,
            "image_url": post.image_url,
            "category_id": post.category_id,
            "slug": post.slug,
            "created_at": post.created_at,
            "category": None
        }
        
        if post.category:
            post_dict["category"] = {
                "name": post.category.name
            }
        
        result.append(post_dict)
    
    return result

@app.get("/posts/{slug}", response_model=PostResponse)
def get_post(slug: str, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.slug == slug).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    post_dict = {
        "id": post.id,
        "name": post.name,
        "content": post.content,
        "image_url": post.image_url,
        "category_id": post.category_id,
        "slug": post.slug,
        "created_at": post.created_at,
        "category": None
    }
    
    if post.category:
        post_dict["category"] = {
            "name": post.category.name
        }
    
    return post_dict

@app.post("/posts", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    # Проверяем существование категории
    category = db.query(Category).filter(Category.id == post.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Генерируем slug
    slug = generate_slug(post.name, db)
    
    db_post = Post(
        name=post.name,
        content=post.content,
        image_url=post.image_url,
        category_id=post.category_id,
        slug=slug
    )
    
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    post_dict = {
        "id": db_post.id,
        "name": db_post.name,
        "content": db_post.content,
        "image_url": db_post.image_url,
        "category_id": db_post.category_id,
        "slug": db_post.slug,
        "created_at": db_post.created_at,
        "category": {
            "name": category.name
        }
    }
    
    return post_dict

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
    if post.name is not None and post.name != db_post.name:
        db_post.name = post.name # pyright: ignore[reportAttributeAccessIssue]
        db_post.slug = generate_slug(post.name, db) # pyright: ignore[reportAttributeAccessIssue]
    
    if post.content is not None:
        db_post.content = post.content # pyright: ignore[reportAttributeAccessIssue]
    
    if post.image_url is not None:
        db_post.image_url = post.image_url # pyright: ignore[reportAttributeAccessIssue]
    
    if post.category_id is not None:
        db_post.category_id = post.category_id # pyright: ignore[reportAttributeAccessIssue]
    
    db.commit()
    db.refresh(db_post)
    
    # Получаем актуальную категорию
    category = db.query(Category).filter(Category.id == db_post.category_id).first()
    
    post_dict = {
        "id": db_post.id,
        "name": db_post.name,
        "content": db_post.content,
        "image_url": db_post.image_url,
        "category_id": db_post.category_id,
        "slug": db_post.slug,
        "created_at": db_post.created_at,
        "category": None
    }
    
    if category:
        post_dict["category"] = {
            "name": category.name
        }
    
    return post_dict

@app.delete("/posts/{slug}")
def delete_post(slug: str, db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.slug == slug).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db.delete(db_post)
    db.commit()
    
    return {"message": "Post deleted successfully"}

# Endpoint для проверки CORS
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)