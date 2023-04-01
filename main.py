from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections
import argparse
from pprint import pprint


def get_catalog_from_excel():
    parser = argparse.ArgumentParser(
        description='Запуск сайта'
    )
    parser.add_argument('--filepath', help='Укажите путь к файлу', default='wine3.xlsx')
    args = parser.parse_args()
    filepath = args.filepath

    excel_data_df = pandas.read_excel(
        filepath,
        sheet_name='Лист1',
        usecols=['Категория', 'Название', 'Сорт', 'Цена', 'Картинка', 'Акция'],
        na_values=['N/A', 'NA'],
        keep_default_na=False
    )

    price = collections.defaultdict(list)
    for unit_of_goods in excel_data_df.to_dict(orient='record'):
        price[unit_of_goods['Категория']].append(unit_of_goods)
    return price


def get_age():
    foundation_year = 1920
    age = datetime.datetime.now().year - foundation_year
    if age % 10 == 1 and age % 100 != 11:
        return f'{age} год'
    if age % 10 in [2, 3, 4] and not (age % 100 in [12, 13, 14]):
        return f'{age} года'
    return f'{age} лет'


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')
    rendered_page = template.render(
        drinks_catalog=get_catalog_from_excel(),
        age_text=get_age()
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()