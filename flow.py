from prefect import flow, task
from scraper import get_html, parse, save, URL


@task
def collect():
    html = get_html(URL)
    return parse(html)


@task
def store(dinos):
    save(dinos)


@flow
def my_flow():
    dinos = collect()
    store(dinos)
    print("Собрали:", len(dinos))


my_flow()