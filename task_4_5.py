import requests
import datetime
from decimal import Decimal
import sys

def currency_rates(req_cur):
    response = requests.get("http://www.cbr.ru/scripts/XML_daily.asp")
    # print(response.status_code)  # 200 Ok
    # print(response.content.decode(encoding=response.encoding))
    content = response.text
    for el in content.split('ValCurs Date="')[1:]:
        e_date = el.split('"')[0]
        e_date_d = int(e_date.split('.')[0])
        e_date_m = int(e_date.split('.')[1])
        e_date_y = int(e_date.split('.')[2])
        # print(e_date_d, e_date_m, e_date_y)
        full_date = datetime.datetime(year=e_date_y, month=e_date_m, day=e_date_d)

    for el in content.split('<Valute ID="')[1:]:
        valute = el.split('</Valute>')[0]
        # print(rate)
        for el in valute.split('<CharCode>')[1:]:
            cur = el.split('</CharCode>')[0]
        for el in valute.split('<Nominal>')[1:]:
            nom = int(el.split('</Nominal>')[0])
        for el in valute.split('<Value>')[1:]:
            rate = el.split('</Value>')[0]
            rate = Decimal(rate.replace(',', '.'))  # <<class 'decimal.Decimal'>
            if nom > 1:
                rate = round(Decimal(float(rate) / (nom / 1)), 4)
                nom = int(nom / (nom / 1))
            # print(nom, cur, '=', rate, 'RUB')
            if cur == req_cur.upper():
                return f"{nom} {cur} = {rate} RUB, {full_date.strftime('%d.%m.%Y')}"



# if __name__ == '__main__':
#     print(currency_rates('eur'))
#     print(currency_rates('USD'))
#     print(currency_rates(input('Введите код валюты для конвертации (USD, GBP...): ')))
# print(sys.argv[1:])
val = "".join(sys.argv[1:])
print(currency_rates(val))
