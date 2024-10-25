import apiclient
from decouple import config
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
import logging


logger = logging.getLogger(__name__)


# Файл, полученный в Google Developer Console
# CREDENTIALS_FILE = './app/creds.json'
# ID Google Sheets документа (можно взять из его URL)
# spreadsheet_id = ''

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    config('CREDENTIALS_FILE'),
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)
table_url = 'https://docs.google.com/spreadsheets/d/' + \
            config('SPREADSHEET_ID') + '/edit'

def send_order_to_google_sheet(nickname, drink):
    result = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=config('SPREADSHEET_ID'),
            range=config('SHEET_NAME'),
            valueInputOption="USER_ENTERED",
            body={
                "majorDimension": "ROWS",
                "values": [[nickname, drink]]
            }
        )
        .execute()
    )
    logger.info(
        f"{(result.get('updates').get('updatedCells'))} cells appended.")


def clear_google_sheet():
    result = (
        service.spreadsheets()
        .values()
        .clear(
            spreadsheetId=config('SPREADSHEET_ID'),
            range=config('SHEET_NAME')
        )
        .execute()
    )

    result = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=config('SPREADSHEET_ID'),
            range=config('SHEET_NAME'),
            valueInputOption="USER_ENTERED",
            body={'values': [['имя', 'напиток']]}
        )
        .execute()
    )
    logger.info(
        f"{(result.get('updates').get('updatedCells'))} cells appended.")


# def send_order_to_google_sheet(row_id, name, drink):
    # service.spreadsheets().values().batchUpdate(
    #     spreadsheetId=config('SPREADSHEET_ID'),
    #     body={
    #         "valueInputOption": "USER_ENTERED",
    #         "data": [
    #             {"range": f'''A{row_id}:B{row_id}''',
    #             "majorDimension": "ROWS",
    #             "values": [[name, drink]]}
    #         ]
    #     } 
    # ).execute()
