from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from PIL import Image
import numpy as np
import torch
from loguru import logger
from matchvibe.ml.model import load_model, load_transform

model = None
transform = None
app = FastAPI()

# Подключаем папку static для статических файлов
app.mount("/frontend/static", StaticFiles(directory="frontend/static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://0.0.0.0:8080", "http://127.0.0.1:8080"],  # Укажите домены вашего фронтенда
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)


class SimilarityResponse(BaseModel):
    similarity_score: float


@app.get("/")
def serve_homepage():
    """Возвращает HTML-файл при переходе на корневой URL."""
    return FileResponse("frontend/static/index.html")


@app.on_event("startup")
def startup_event():
    global model
    global transform
    model = load_model()
    transform = load_transform()


@app.post("/compare-images", response_model=SimilarityResponse)
async def compare_images(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    try:
        logger.info("Received request to compare images.")
        
        # Load and preprocess images
        image1 = Image.open(file1.file).convert("RGB")
        image2 = Image.open(file2.file).convert("RGB")
        logger.info("Images successfully loaded.")

        tensor1 = transform(image1).unsqueeze(0)  # Add batch dimension
        tensor2 = transform(image2).unsqueeze(0)  # Add batch dimension
        logger.info("Images successfully transformed.")

        # Get embeddings
        embedding1 = model(tensor1).embedding
        embedding2 = model(tensor2).embedding
        logger.info("Embeddings successfully computed.")

        # Calculate similarity
        similarity_score = calculate_similarity(embedding1, embedding2)
        logger.info(f"Similarity score computed: {similarity_score}")

        return SimilarityResponse(similarity_score=similarity_score)
    except Exception as e:
        logger.error(f"Error during image comparison: {e}")
        raise HTTPException(status_code=500, detail="Error processing images")


def calculate_similarity(embedding1, embedding2):
    """Calculate cosine similarity between two embeddings."""
    embedding1 = torch.tensor(embedding1).float()
    embedding2 = torch.tensor(embedding2).float()
    
    cos = torch.nn.functional.cosine_similarity(embedding1, embedding2)
    return cos.item()
