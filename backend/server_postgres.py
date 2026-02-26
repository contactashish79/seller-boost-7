from fastapi import FastAPI, APIRouter, HTTPException, Depends, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
import logging
from pathlib import Path
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timezone, timedelta
import jwt
from passlib.context import CryptContext
from PIL import Image
from io import BytesIO
import shutil
from emergentintegrations.llm.chat import LlmChat, UserMessage, ImageContent
import base64

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create uploads directory
UPLOAD_DIR = ROOT_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# PostgreSQL connection
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://localhost/amazon_aplus')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class UserDB(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

class ProjectDB(Base):
    __tablename__ = "projects"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)
    original_image_path = Column(String, nullable=True)
    processed_image_path = Column(String, nullable=True)
    ai_title = Column(Text, nullable=True)
    ai_description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
api_router = APIRouter(prefix="/api")

# Mount uploads directory for serving files
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

JWT_SECRET = os.environ.get('JWT_SECRET', 'your-secret-key')
JWT_ALGORITHM = "HS256"
EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY')
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:8000')

# Pydantic models
class User(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

class Project(BaseModel):
    id: str
    user_id: str
    name: str
    original_image_url: Optional[str] = None
    processed_image_url: Optional[str] = None
    ai_title: Optional[str] = None
    ai_description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class ProjectCreate(BaseModel):
    name: str

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    ai_title: Optional[str] = None
    ai_description: Optional[str] = None

class ContentGenerateRequest(BaseModel):
    product_type: str
    key_features: Optional[str] = None

class ImageGenerateRequest(BaseModel):
    prompt: str
    project_id: str

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload.get("user_id")
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

def save_uploaded_file(file: UploadFile, user_id: str, file_type: str = "original") -> str:
    """Save uploaded file and return URL path"""
    file_ext = Path(file.filename).suffix or '.jpg'
    filename = f"{user_id}_{file_type}_{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / filename
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return f"/uploads/{filename}"

def save_processed_image(image: Image.Image, user_id: str, prefix: str = "processed") -> str:
    """Save PIL Image and return URL path"""
    filename = f"{user_id}_{prefix}_{uuid.uuid4()}.png"
    file_path = UPLOAD_DIR / filename
    image.save(file_path, "PNG")
    return f"/uploads/{filename}"

def path_to_url(path: str) -> str:
    """Convert file path to full URL"""
    if path and not path.startswith('http'):
        return f"{BASE_URL}{path}"
    return path

@api_router.get("/")
async def root():
    return {"message": "Amazon A+ Content Generator API"}

@api_router.post("/auth/signup", response_model=Token)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(UserDB).filter(UserDB.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_id = str(uuid.uuid4())
    user_db = UserDB(
        id=user_id,
        email=user_data.email,
        password_hash=pwd_context.hash(user_data.password)
    )
    db.add(user_db)
    db.commit()
    
    user = User(id=user_id, email=user_data.email, created_at=user_db.created_at)
    token = create_access_token({"user_id": user_id, "email": user_data.email})
    return Token(access_token=token, token_type="bearer", user=user)

@api_router.post("/auth/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user_db = db.query(UserDB).filter(UserDB.email == user_data.email).first()
    if not user_db or not pwd_context.verify(user_data.password, user_db.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user = User(id=user_db.id, email=user_db.email, created_at=user_db.created_at)
    token = create_access_token({"user_id": user_db.id, "email": user_db.email})
    return Token(access_token=token, token_type="bearer", user=user)

@api_router.post("/projects", response_model=Project)
async def create_project(project_data: ProjectCreate, user_id: str = Depends(verify_token), db: Session = Depends(get_db)):
    project_id = str(uuid.uuid4())
    project_db = ProjectDB(
        id=project_id,
        user_id=user_id,
        name=project_data.name
    )
    db.add(project_db)
    db.commit()
    
    return Project(
        id=project_id,
        user_id=user_id,
        name=project_data.name,
        created_at=project_db.created_at,
        updated_at=project_db.updated_at
    )

@api_router.get("/projects", response_model=List[Project])
async def get_projects(user_id: str = Depends(verify_token), db: Session = Depends(get_db)):
    projects = db.query(ProjectDB).filter(ProjectDB.user_id == user_id).order_by(ProjectDB.created_at.desc()).all()
    
    return [
        Project(
            id=p.id,
            user_id=p.user_id,
            name=p.name,
            original_image_url=path_to_url(p.original_image_path),
            processed_image_url=path_to_url(p.processed_image_path),
            ai_title=p.ai_title,
            ai_description=p.ai_description,
            created_at=p.created_at,
            updated_at=p.updated_at
        )
        for p in projects
    ]

@api_router.get("/projects/{project_id}", response_model=Project)
async def get_project(project_id: str, user_id: str = Depends(verify_token), db: Session = Depends(get_db)):
    project = db.query(ProjectDB).filter(ProjectDB.id == project_id, ProjectDB.user_id == user_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return Project(
        id=project.id,
        user_id=project.user_id,
        name=project.name,
        original_image_url=path_to_url(project.original_image_path),
        processed_image_url=path_to_url(project.processed_image_path),
        ai_title=project.ai_title,
        ai_description=project.ai_description,
        created_at=project.created_at,
        updated_at=project.updated_at
    )

@api_router.put("/projects/{project_id}", response_model=Project)
async def update_project(project_id: str, updates: ProjectUpdate, user_id: str = Depends(verify_token), db: Session = Depends(get_db)):
    project = db.query(ProjectDB).filter(ProjectDB.id == project_id, ProjectDB.user_id == user_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if updates.name:
        project.name = updates.name
    if updates.ai_title is not None:
        project.ai_title = updates.ai_title
    if updates.ai_description is not None:
        project.ai_description = updates.ai_description
    
    project.updated_at = datetime.now(timezone.utc)
    db.commit()
    
    return Project(
        id=project.id,
        user_id=project.user_id,
        name=project.name,
        original_image_url=path_to_url(project.original_image_path),
        processed_image_url=path_to_url(project.processed_image_path),
        ai_title=project.ai_title,
        ai_description=project.ai_description,
        created_at=project.created_at,
        updated_at=project.updated_at
    )

@api_router.delete("/projects/{project_id}")
async def delete_project(project_id: str, user_id: str = Depends(verify_token), db: Session = Depends(get_db)):
    project = db.query(ProjectDB).filter(ProjectDB.id == project_id, ProjectDB.user_id == user_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Delete associated files
    if project.original_image_path:
        try:
            (UPLOAD_DIR / Path(project.original_image_path).name).unlink(missing_ok=True)
        except:
            pass
    if project.processed_image_path:
        try:
            (UPLOAD_DIR / Path(project.processed_image_path).name).unlink(missing_ok=True)
        except:
            pass
    
    db.delete(project)
    db.commit()
    return {"success": True}

@api_router.post("/image/upload/{project_id}")
async def upload_image(project_id: str, file: UploadFile = File(...), user_id: str = Depends(verify_token), db: Session = Depends(get_db)):
    project = db.query(ProjectDB).filter(ProjectDB.id == project_id, ProjectDB.user_id == user_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    file_path = save_uploaded_file(file, user_id, "original")
    project.original_image_path = file_path
    project.processed_image_path = file_path
    project.updated_at = datetime.now(timezone.utc)
    db.commit()
    
    return {
        "original_image_url": path_to_url(file_path),
        "processed_image_url": path_to_url(file_path)
    }

@api_router.post("/image/remove-background/{project_id}")
async def remove_background(project_id: str, user_id: str = Depends(verify_token), db: Session = Depends(get_db)):
    project = db.query(ProjectDB).filter(ProjectDB.id == project_id, ProjectDB.user_id == user_id).first()
    if not project or not project.processed_image_path:
        raise HTTPException(status_code=404, detail="Project or image not found")
    
    try:
        img_path = UPLOAD_DIR / Path(project.processed_image_path).name
        img = Image.open(img_path).convert("RGBA")
        
        datas = img.getdata()
        newData = []
        threshold = 240
        for item in datas:
            if item[0] > threshold and item[1] > threshold and item[2] > threshold:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        
        img.putdata(newData)
        result_path = save_processed_image(img, user_id, "nobg")
        project.processed_image_path = result_path
        project.updated_at = datetime.now(timezone.utc)
        db.commit()
        
        return {"processed_image_url": path_to_url(result_path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Background removal failed: {str(e)}")

@api_router.post("/image/generate-background")
async def generate_background(request: ImageGenerateRequest, user_id: str = Depends(verify_token), db: Session = Depends(get_db)):
    project = db.query(ProjectDB).filter(ProjectDB.id == request.project_id, ProjectDB.user_id == user_id).first()
    if not project or not project.processed_image_path:
        raise HTTPException(status_code=404, detail="Project or image not found")
    
    try:
        # Load reference image
        img_path = UPLOAD_DIR / Path(project.processed_image_path).name
        with open(img_path, "rb") as f:
            ref_image_b64 = base64.b64encode(f.read()).decode('utf-8')
        
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=f"image_gen_{user_id}_{uuid.uuid4()}",
            system_message="You are an expert at creating professional product photography backgrounds."
        )
        chat.with_model("gemini", "gemini-3-pro-image-preview").with_params(modalities=["image", "text"])
        
        msg = UserMessage(
            text=f"Create a professional product photography background: {request.prompt}. Make it suitable for e-commerce.",
            file_contents=[ImageContent(ref_image_b64)]
        )
        
        text, images = await chat.send_message_multimodal_response(msg)
        
        if images and len(images) > 0:
            img_data = base64.b64decode(images[0]['data'])
            img = Image.open(BytesIO(img_data))
            result_path = save_processed_image(img, user_id, "aibg")
            
            project.processed_image_path = result_path
            project.updated_at = datetime.now(timezone.utc)
            db.commit()
            
            return {"processed_image_url": path_to_url(result_path)}
        else:
            raise HTTPException(status_code=500, detail="No image generated")
    except Exception as e:
        logging.error(f"Image generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")

@api_router.post("/image/enhance/{project_id}")
async def enhance_image(project_id: str, user_id: str = Depends(verify_token), db: Session = Depends(get_db)):
    project = db.query(ProjectDB).filter(ProjectDB.id == project_id, ProjectDB.user_id == user_id).first()
    if not project or not project.processed_image_path:
        raise HTTPException(status_code=404, detail="Project or image not found")
    
    try:
        img_path = UPLOAD_DIR / Path(project.processed_image_path).name
        img = Image.open(img_path)
        width, height = img.size
        enhanced = img.resize((width * 2, height * 2), Image.Resampling.LANCZOS)
        
        result_path = save_processed_image(enhanced, user_id, "enhanced")
        project.processed_image_path = result_path
        project.updated_at = datetime.now(timezone.utc)
        db.commit()
        
        return {"processed_image_url": path_to_url(result_path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enhancement failed: {str(e)}")

@api_router.post("/content/generate")
async def generate_content(request: ContentGenerateRequest, user_id: str = Depends(verify_token)):
    try:
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=f"content_gen_{user_id}_{uuid.uuid4()}",
            system_message="You are an expert at creating Amazon A+ content."
        )
        chat.with_model("openai", "gpt-5.2")
        
        prompt = f"""Create Amazon A+ content for a {request.product_type}.
{f'Key features: {request.key_features}' if request.key_features else ''}

Provide:
1. A compelling product title (max 200 characters)
2. A detailed product description (3-4 paragraphs)

Format:
TITLE: [your title]
DESCRIPTION: [your description]"""
        
        msg = UserMessage(text=prompt)
        response = await chat.send_message(msg)
        
        parts = response.split('DESCRIPTION:')
        title = parts[0].replace('TITLE:', '').strip()
        description = parts[1].strip() if len(parts) > 1 else ''
        
        return {"title": title, "description": description}
    except Exception as e:
        logging.error(f"Content generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Content generation failed: {str(e)}")

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown():
    pass
