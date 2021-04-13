from bs4 import BeautifulSoup
import requests
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def toSheet():
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(credentials)
        # sheet = client.open('MAE').sheet1

        spreadsheet = client.open("MAE")
        today = datetime.today().strftime('%d-%m-%Y')
        sheet = spreadsheet.add_worksheet(title=today, rows="300", cols="11")

        url = 'https://servicios.mae.com.ar/mercados/rentafija/resumen_final.aspx'

        r = requests.get(url)
        s = BeautifulSoup(r.text, "html.parser")

        container = s.find("div", {"id": "ContentPlaceHolder1_UPPreciosExtracto"})
        table = container.find("table")

        rows = table.findAll("tr")
        values_row = rows[0]
        rows = rows[1:]

        values = []
        for th in values_row.findAll("th"):
            values.append(th.text)
        sheet.insert_row(values, 1)

        final_rows = []
        for tr in rows:
            row = []
            for td in tr.findAll("td"):
                row.append(td.text.strip())
            final_rows.append(row)

        sheet.insert_rows(final_rows, 2)
        return True
    except Exception as e:
        print(e)
        return False


# if __name__ == "__main__":
#     toSheet()
