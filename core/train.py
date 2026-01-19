# core/py
import os
from pathlib import Path
import hydra
from omegaconf import DictConfig, OmegaConf
from ultralytics import YOLO
import mlflow
import torch


# Проверка данных
def validate_data_config(data_path: str):
    data_path = Path(data_path)
    if not data_path.exists():
        raise FileNotFoundError(f"❌ Файл конфигурации данных не найден: {data_path}")

    from ruamel.yaml import YAML
    yaml = YAML()
    try:
        cfg = yaml.load(data_path)
    except Exception as e:
        raise RuntimeError(f"❌ Ошибка чтения YAML: {e}")

    dataset_path = Path(cfg.get("path", "")).expanduser()

    if not dataset_path.is_absolute():
        dataset_path = (data_path.parent.parent / dataset_path).resolve()

    for split in ["train", "val"]:
        img_dir = dataset_path / cfg[split]
        if not img_dir.exists():
            raise NotADirectoryError(f"❌ Папка изображений не найдена: {img_dir}")

    print(f"✅ Данные проверены: {dataset_path}")
    # return dataset_path  # 🔁 Возвращаем, чтобы использовать



@hydra.main(config_path="configs", config_name="config", version_base=None)
def main(cfg: DictConfig) -> None:
    print("🔥 Используем конфиг:")
    print(OmegaConf.to_yaml(cfg))

    # Устанавливаем seed
    if cfg.get("seed"):
        from ultralytics.utils.torch_utils import init_seeds
        init_seeds(cfg.seed)
        print(f"🌱 Seed установлен: {cfg.seed}")

    # Путь к data.yaml
    data_yaml = Path(cfg.data_path).resolve()
    print(f"📂 Используем data.yaml: {data_yaml}")
    # dataset_path = validate_data_config(data_yaml)  # Получаем исправленный путь

    # Проверяем, что файл существует и корректен
    # validate_data_config(data_yaml)

    # Создаём папку для сохранения
    project_dir = Path(cfg.project)
    project_dir.mkdir(exist_ok=True, parents=True)
    print(f"📁 Проект: {project_dir} / {cfg.name}")

    # Создаём модель
    print(f"🚀 Загружаем модель: {cfg.weights}")
    model = YOLO(cfg.weights)

    if torch.cuda.is_available():
        device = 0
        print(f"🎮 Используем GPU: {torch.cuda.get_device_name(device)}")
    else:
        device = 'cpu'
        print(f"💻 CUDA недоступна, используем CPU")
    
    # Set to one of the supported schemes
    mlflow.set_tracking_uri(cfg.mlflow.tracking_uri)

    # Обучение
    print("🚀 Запускаем обучение...")
    try:
        results = model.train(
            data=str(data_yaml),
            epochs=cfg.epochs,
            batch=cfg.batch_size,
            imgsz=cfg.imgsz,
            optimizer=cfg.optimizer,
            lr0=cfg.lr,
            weight_decay=cfg.weight_decay,
            patience=cfg.patience,
            project=cfg.project,
            name=cfg.name,
            workers=cfg.workers,
            exist_ok=True,
            device=device,
        )
        print(f"✅ Обучение завершено. Результаты: {results.save_dir}")
    except Exception as e:
        print(f"\n❌ Ошибка при обучении: \n{e}")
        raise


if __name__ == "__main__":
    main()