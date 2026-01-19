# core/app.py

import base64
import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from ultralytics import YOLO
import uvicorn
from pathlib import Path
import sys

# Добавляем корень проекта в путь, если нужно
sys.path.append(str(Path(__file__).parent.parent))

from omegaconf import DictConfig
import hydra


app = FastAPI(title="Bubble Detection API")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Глобальная модель — загружаем один раз при старте
print("Загружаю модель YOLO...")
model_path = Path("weights/model.pt").resolve()
if not model_path.exists():
    raise RuntimeError(f"Модель не найдена: {model_path}")
model = YOLO(str(model_path))
print(f"Модель загружена: {model_path}")


@app.post("/use_model")
async def use_model(file: UploadFile = File(...)):
    """
    Обработка изображения: predict + plot → base64
    """
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if image is None:
            raise HTTPException(status_code=400, detail="Не удалось декодировать изображение")

        results = model.predict(image, verbose=False, conf=0.25)
        res_img = results[0].plot()

        _, buffer = cv2.imencode(".jpg", res_img)
        img_base64 = base64.b64encode(buffer).decode("utf-8")

        return JSONResponse(content={"image": img_base64})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Ошибка: {str(e)}"})


@hydra.main(config_path="configs", config_name="api", version_base=None)
def main(cfg: DictConfig) -> None:
    """
    Точка входа с конфигурацией Hydra
    """
    print(f"🚀 Запуск API: {cfg.host}:{cfg.port}")
    print(f"🔧 Reload: {cfg.reload}, Log level: {cfg.log_level}")

    uvicorn.run(
        app="core.app:app",
        host=cfg.host,
        port=cfg.port,
        reload=cfg.reload,
        log_level=cfg.log_level,
        workers=1,
    )


if __name__ == "__main__":
    main()
