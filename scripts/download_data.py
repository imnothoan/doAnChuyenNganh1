from src.data.download_manager import download_datasets


if __name__ == "__main__":
    statuses = download_datasets()
    for status in statuses:
        print(f"[{status.status}] {status.dataset}: {status.message}")
