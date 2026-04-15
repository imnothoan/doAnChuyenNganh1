try:
    from scripts._bootstrap import ensure_repo_root_on_path
except ModuleNotFoundError:
    from _bootstrap import ensure_repo_root_on_path

ensure_repo_root_on_path(__file__)

from src.models.train_baseline import train_baseline_models


if __name__ == "__main__":
    metrics = train_baseline_models()
    print(metrics)
