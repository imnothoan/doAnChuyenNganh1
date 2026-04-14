from src.models.train_transformer import train_transformer_or_report_fallback


if __name__ == "__main__":
    result = train_transformer_or_report_fallback()
    print(result)
