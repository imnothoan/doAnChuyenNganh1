try:
    from scripts._bootstrap import ensure_repo_root_on_path
except ModuleNotFoundError:
    from _bootstrap import ensure_repo_root_on_path

ensure_repo_root_on_path(__file__)

from src.models.train_transformer import train_transformer_or_report_fallback


if __name__ == "__main__":
    result = train_transformer_or_report_fallback()
    print(result)
