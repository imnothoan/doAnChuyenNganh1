from src.models.train_baseline import train_baseline_models


if __name__ == "__main__":
    metrics = train_baseline_models()
    print(metrics)
