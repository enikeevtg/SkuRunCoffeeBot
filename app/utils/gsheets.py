# Устарело
import apiclient
from decouple import config
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.errors import HttpError
import logging


logger = logging.getLogger(__name__)


# Файл, полученный в Google Developer Console
# CREDENTIALS_FILE = './app/creds.json'
# ID Google Sheets документа (можно взять из его URL)
# spreadsheet_id = ''

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    config("CREDENTIALS_FILE"),
    [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ],
)
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build("sheets", "v4", http=httpAuth)
table_url = (
    f"https://docs.google.com/spreadsheets/d/{config("SPREADSHEET_ID")}/edit"
)


def init_google_sheet():
    try:
        response = (
            service.spreadsheets()
            .values()
            .clear(
                spreadsheetId=config("SPREADSHEET_ID"),
                range=config("SHEET_NAME"),
            )
            .execute()
        )

        response = (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId=config("SPREADSHEET_ID"),
                range=config("SHEET_NAME"),
                valueInputOption="USER_ENTERED",
                body={"values": [["Имя", "Напиток", "Статус"]]},
            )
            .execute()
        )
        logger.info(f"response: {response}")
        return response

    except HttpError as error:
        logger.error(f"An error occured: {error}")
        return error


def send_order(tg_id, username, nickname, drink):
    try:
        requests = []
        requests.append(
            {
                "appendCells": {
                    "sheetId": 0,
                    "rows": [
                        {
                            "values": [
                                {
                                    "userEnteredValue": {
                                        "stringValue": nickname
                                    }
                                },
                                {"userEnteredValue": {"stringValue": drink}},
                                {
                                    "dataValidation": {
                                        "condition": {
                                            "type": "BOOLEAN",
                                            "values": [
                                                {
                                                    "userEnteredValue": "OrderDone"
                                                }
                                            ],
                                        }
                                    }
                                },
                            ]
                        }
                    ],
                    "fields": "*",
                }
            }
        )

        body = {"requests": requests}
        response = (
            service.spreadsheets()
            .batchUpdate(spreadsheetId=config("SPREADSHEET_ID"), body=body)
            .execute()
        )
        logger.info(
            f"[{tg_id}, {username}: | {nickname} | {drink} | [ ] | "
            "cells appended.]"
        )
        return response

    except HttpError as error:
        logger.error(f"An error occured: {error}")
        return error
