import datetime


def log_info(message: str):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[INFO {now}]: {message}")
