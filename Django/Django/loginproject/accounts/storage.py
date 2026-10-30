import csv
from pathlib import Path

from django.contrib.auth.hashers import make_password, check_password

CSV_FILE = Path(__file__).resolve().parent.parent / "users.csv"


def read_users():
    if not CSV_FILE.exists():
        return []

    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def find_user(username):
    for user in read_users():
        if user["username"].lower() == username.lower():
            return user

    return None


def add_user(username, password):
    file_exists = CSV_FILE.exists()

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["username", "password"])

        writer.writerow([username, make_password(password)])


def check_user(username, password):
    user = find_user(username)

    if user is None:
        return None

    if check_password(password, user["password"]):
        return user["username"]

    return None