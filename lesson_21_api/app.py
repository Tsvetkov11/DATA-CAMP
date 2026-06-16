import io
from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image
from transformers import pipeline

# Ініціалізація FastAPI додатку
app = FastAPI(
    title="Computer Vision API",
    description="API для класифікації зображень(ViT)",
    version="1.0.0"
)

# Глобальна змінна для пайплайну моделі
classifier = None

@app.on_event("startup")
async def load_model():
    """
    Завантаження моделі при запуску сервера.
    Модель Google ViT.
    """
    global classifier
    # Пайплайн автоматично завантажує архітектуру та ваги моделі
    classifier = pipeline("image-classification", model="google/vit-base-patch16-224")
    print("Модель завантажена і готова")

@app.get("/")
def read_root():
    """Ендпоінт для перевірки"""
    return {
        "status": "healthy",
        "message": "Computer Vision API працює. Перейдіть на /docs у Swagger UI."
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Приймає файл зображення, обробляє його за допомогою ViT моделі 
    та повертає топ-5 найбільш ймовірних класів.
    """
    # Перевіряємо, чи є завантажений файл зображенням
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Файл повинен бути зображенням (JPEG/PNG).")
    
    try:
        # Читання бінарного контенту файлу
        contents = await file.read()
        
        # Відкриття зображення через Pillow та приведення до RGB
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        
        # Отримання передбачень від моделі
        predictions = classifier(image)
        
        # Формування структурованої відповіді
        return {
            "filename": file.filename,
            "predictions": [
                {"label": pred["label"], "confidence": round(pred["score"], 4)}
                for pred in predictions
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Помилка при обробці зображення: {str(e)}")