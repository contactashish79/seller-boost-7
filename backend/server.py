from fastapi import FastAPI, APIRouter, HTTPException, Depends, UploadFile, File, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timezone, timedelta
import jwt
from passlib.context import CryptContext
import base64
from io import BytesIO
from PIL import Image
import asyncio
from emergentintegrations.llm.chat import LlmChat, UserMessage, ImageContent

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()
api_router = APIRouter(prefix="/api")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

JWT_SECRET = os.environ.get('JWT_SECRET', 'your-secret-key')
JWT_ALGORITHM = "HS256"
EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY')

class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

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
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    name: str
    original_image: Optional[str] = None
    processed_image: Optional[str] = None
    ai_title: Optional[str] = None
    ai_description: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ProjectCreate(BaseModel):
    name: str

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    original_image: Optional[str] = None
    processed_image: Optional[str] = None
    ai_title: Optional[str] = None
    ai_description: Optional[str] = None

class ContentGenerateRequest(BaseModel):
    product_type: str
    key_features: Optional[str] = None

class ImageGenerateRequest(BaseModel):
    prompt: str
    reference_image: Optional[str] = None

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

@api_router.get("/")
async def root():
    return {"message": "Amazon A+ Content Generator API"}

@api_router.post("/auth/signup", response_model=Token)
async def signup(user_data: UserCreate):
    existing_user = await db.users.find_one({"email": user_data.email}, {"_id": 0})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = User(email=user_data.email)
    user_dict = user.model_dump()
    user_dict['created_at'] = user_dict['created_at'].isoformat()
    user_dict['password_hash'] = pwd_context.hash(user_data.password)
    
    await db.users.insert_one(user_dict)
    
    token = create_access_token({"user_id": user.id, "email": user.email})
    return Token(access_token=token, token_type="bearer", user=user)

@api_router.post("/auth/login", response_model=Token)
async def login(user_data: UserLogin):
    user_doc = await db.users.find_one({"email": user_data.email}, {"_id": 0})
    if not user_doc:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not pwd_context.verify(user_data.password, user_doc['password_hash']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if isinstance(user_doc['created_at'], str):
        user_doc['created_at'] = datetime.fromisoformat(user_doc['created_at'])
    
    user = User(**{k: v for k, v in user_doc.items() if k != 'password_hash'})
    token = create_access_token({"user_id": user.id, "email": user.email})
    return Token(access_token=token, token_type="bearer", user=user)

@api_router.post("/projects", response_model=Project)
async def create_project(project_data: ProjectCreate, user_id: str = Depends(verify_token)):
    project = Project(user_id=user_id, name=project_data.name)
    project_dict = project.model_dump()
    project_dict['created_at'] = project_dict['created_at'].isoformat()
    project_dict['updated_at'] = project_dict['updated_at'].isoformat()
    
    await db.projects.insert_one(project_dict)
    return project

@api_router.get("/projects", response_model=List[Project])
async def get_projects(user_id: str = Depends(verify_token)):
    projects = await db.projects.find({"user_id": user_id}, {"_id": 0}).sort("created_at", -1).to_list(100)
    
    for project in projects:
        if isinstance(project.get('created_at'), str):
            project['created_at'] = datetime.fromisoformat(project['created_at'])
        if isinstance(project.get('updated_at'), str):
            project['updated_at'] = datetime.fromisoformat(project['updated_at'])
    
    return projects

@api_router.get("/projects/{project_id}", response_model=Project)
async def get_project(project_id: str, user_id: str = Depends(verify_token)):
    project = await db.projects.find_one({"id": project_id, "user_id": user_id}, {"_id": 0})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if isinstance(project.get('created_at'), str):
        project['created_at'] = datetime.fromisoformat(project['created_at'])
    if isinstance(project.get('updated_at'), str):
        project['updated_at'] = datetime.fromisoformat(project['updated_at'])
    
    return Project(**project)

@api_router.put("/projects/{project_id}", response_model=Project)
async def update_project(project_id: str, updates: ProjectUpdate, user_id: str = Depends(verify_token)):
    project = await db.projects.find_one({"id": project_id, "user_id": user_id}, {"_id": 0})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    update_data = {k: v for k, v in updates.model_dump().items() if v is not None}
    if update_data:
        update_data['updated_at'] = datetime.now(timezone.utc).isoformat()
        await db.projects.update_one({"id": project_id}, {"$set": update_data})
    
    updated_project = await db.projects.find_one({"id": project_id}, {"_id": 0})
    if isinstance(updated_project.get('created_at'), str):
        updated_project['created_at'] = datetime.fromisoformat(updated_project['created_at'])
    if isinstance(updated_project.get('updated_at'), str):
        updated_project['updated_at'] = datetime.fromisoformat(updated_project['updated_at'])
    
    return Project(**updated_project)

@api_router.delete("/projects/{project_id}")
async def delete_project(project_id: str, user_id: str = Depends(verify_token)):
    result = await db.projects.delete_one({"id": project_id, "user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"success": True}

@api_router.post("/image/upload")
async def upload_image(file: UploadFile = File(...), user_id: str = Depends(verify_token)):
    contents = await file.read()
    base64_image = base64.b64encode(contents).decode('utf-8')
    mime_type = file.content_type or 'image/jpeg'
    return {"image": f"data:{mime_type};base64,{base64_image}"}

@api_router.post("/image/remove-background")
async def remove_background(image_data: dict, user_id: str = Depends(verify_token)):
    try:
        image_base64 = image_data.get('image', '').split(',')[1] if ',' in image_data.get('image', '') else image_data.get('image', '')
        image_bytes = base64.b64decode(image_base64)
        
        img = Image.open(BytesIO(image_bytes)).convert("RGBA")
        datas = img.getdata()
        
        newData = []
        threshold = 240
        for item in datas:
            if item[0] > threshold and item[1] > threshold and item[2] > threshold:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        
        img.putdata(newData)
        
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        result_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        return {"image": f"data:image/png;base64,{result_base64}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Background removal failed: {str(e)}")

@api_router.post("/image/generate-background")
async def generate_background(request: ImageGenerateRequest, user_id: str = Depends(verify_token)):
    try:
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=f"image_gen_{user_id}_{uuid.uuid4()}",
            system_message="You are an expert at creating professional product photography backgrounds."
        )
        chat.with_model("gemini", "gemini-3-pro-image-preview").with_params(modalities=["image", "text"])
        
        file_contents = []
        if request.reference_image:
            ref_base64 = request.reference_image.split(',')[1] if ',' in request.reference_image else request.reference_image
            file_contents.append(ImageContent(ref_base64))
        
        msg = UserMessage(
            text=f"Create a professional product photography background: {request.prompt}. Make it suitable for e-commerce, high quality, and professional.",
            file_contents=file_contents if file_contents else None
        )
        
        text, images = await chat.send_message_multimodal_response(msg)
        
        if images and len(images) > 0:
            img_data = images[0]['data']
            mime_type = images[0].get('mime_type', 'image/png')
            return {"image": f"data:{mime_type};base64,{img_data}"}
        else:
            raise HTTPException(status_code=500, detail="No image generated")
    except Exception as e:
        logging.error(f"Image generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")

@api_router.post("/image/enhance")
async def enhance_image(image_data: dict, user_id: str = Depends(verify_token)):
    try:
        image_base64 = image_data.get('image', '').split(',')[1] if ',' in image_data.get('image', '') else image_data.get('image', '')
        image_bytes = base64.b64decode(image_base64)
        
        img = Image.open(BytesIO(image_bytes))
        width, height = img.size
        enhanced = img.resize((width * 2, height * 2), Image.Resampling.LANCZOS)
        
        buffered = BytesIO()
        enhanced.save(buffered, format="PNG", quality=95)
        result_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        return {"image": f"data:image/png;base64,{result_base64}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enhancement failed: {str(e)}")

@api_router.post("/content/generate")
async def generate_content(request: ContentGenerateRequest, user_id: str = Depends(verify_token)):
    try:
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=f"content_gen_{user_id}_{uuid.uuid4()}",
            system_message="You are an expert at creating Amazon A+ content that converts. Create compelling, benefit-focused copy that follows Amazon's guidelines."
        )
        chat.with_model("openai", "gpt-5.2")
        
        prompt = f"""Create Amazon A+ content for a {request.product_type}.
{f'Key features: {request.key_features}' if request.key_features else ''}

Provide:
1. A compelling product title (max 200 characters, benefit-focused)
2. A detailed product description (3-4 paragraphs, highlighting benefits, use cases, and quality)

Format:
TITLE: [your title]
DESCRIPTION: [your description]"""
        
        msg = UserMessage(text=prompt)
        response = await chat.send_message(msg)
        
        parts = response.split('DESCRIPTION:')
        title = parts[0].replace('TITLE:', '').strip()
        description = parts[1].strip() if len(parts) > 1 else ''
        
        return {
            "title": title,
            "description": description
        }
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
async def shutdown_db_client():
    client.close()