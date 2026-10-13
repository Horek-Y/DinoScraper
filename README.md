# Динозавры
Проект собирает данные о динозаврах с Википедии.

## Файлы
- `scraper.py` — собирает данные
- `analysis.py` — строит график
- `flow.py` — запускает через prefect
- `data/dinosaurs.csv` — данные
- `reports/chart.png` — график

## Как запустить
библиотеки:
pip install -r requirements.txt

python scraper.py
python analysis.py

## Результат
- CSV-файл с динозаврами в `data/`
- Картинка с графиком в `reports/`