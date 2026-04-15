import argparse

try:
    from scripts._bootstrap import ensure_repo_root_on_path
except ModuleNotFoundError:
    from _bootstrap import ensure_repo_root_on_path

ensure_repo_root_on_path(__file__)

from src.data.make_dataset import make_dataset


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--time-aware", action="store_true", help="Use chronological split when published_at is available")
    args = parser.parse_args()
    make_dataset(time_aware_split=args.time_aware)
