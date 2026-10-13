import csv
import os
import json
from datetime import datetime

import requests
import urllib3

urllib3.disable_warnings()

# API Википедии: получаем список страниц из категории "Dinosaur genera"
API_URL = "https://en.wikipedia.org/w/api.php"

FILE_NAME = "data/dinosaurs.csv"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
}


def get_category_members(category="Category:Dinosaur genera", limit=500):
    """Получает список страниц из категории Википедии."""
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": category,
        "cmlimit": limit,
        "format": "json",
    }
    r = requests.get(API_URL, params=params, headers=headers, timeout=30, verify=False)
    data = r.json()
    members = data.get("query", {}).get("categorymembers", [])
    return members


def get_page_info(titles):
    """Получает краткую информацию о страницах (extract)."""
    params = {
        "action": "query",
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
        "titles": "|".join(titles),
        "format": "json",
    }
    r = requests.get(API_URL, params=params, headers=headers, timeout=60, verify=False)
    data = r.json()
    pages = data.get("query", {}).get("pages", {})
    return pages


def parse_members(members):
    """Преобразует список членов категории в нужный формат."""
    dinos = []
    for m in members:
        title = m.get("title", "")
        # пропускаем служебные страницы
        if title.startswith("Category:") or title.startswith("Template:"):
            continue
        dinos.append({
            "name": title,
            "page_id": m.get("pageid", ""),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        })
    return dinos


def save(dinos):
    if not os.path.exists("data"):
        os.mkdir("data")

    with open(FILE_NAME, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "page_id", "date"])
        writer.writeheader()
        for d in dinos:
            writer.writerow(d)

    print("Записали в файл:", len(dinos))


def main():
    print("Сбор динозавров с wiki")

    members = get_category_members("Category:Dinosaur genera", limit=500)
    print("Найдено записей:", len(members))

    if len(members) == 0:
        print("Категория пустая. Пробуем другую...")
        members = get_category_members("Category:Dinosaurs", limit=500)
        print("Найдено записей:", len(members))

    dinos = parse_members(members)
    if len(dinos) > 0:
        save(dinos)

    print("Готово")


main()