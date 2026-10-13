import os
import pandas as pd
import matplotlib.pyplot as plt

FILE_NAME = "data/dinosaurs.csv"


def main():
    if not os.path.exists(FILE_NAME):
        print("Сначала запусти scraper.py!")
        return

    df = pd.read_csv(FILE_NAME)

    print("Всего динозавров:", len(df))
    print("Колонки:", list(df.columns))
    print("\nПервые 10 строк:")
    print(df.head(10))

    if not os.path.exists("reports"):
        os.mkdir("reports")

    # график: количество динозавров на каждую первую букву названия
    df["first_letter"] = df["name"].astype(str).str[0].str.upper()
    counts = df["first_letter"].value_counts().sort_index()

    plt.figure(figsize=(14, 6))
    counts.plot(kind="bar", color="seagreen")
    plt.title("Количество динозавров по первой букве названия")
    plt.xlabel("Буква")
    plt.ylabel("Количество")
    plt.tight_layout()
    plt.savefig("reports/chart.png")
    print("\nГрафик сохранён в reports/chart.png")


main()