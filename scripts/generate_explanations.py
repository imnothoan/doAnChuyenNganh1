import argparse

from src.explainability.explain import save_explanation_json


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True)
    args = parser.parse_args()
    output = save_explanation_json(args.text)
    print(f"Saved: {output}")
