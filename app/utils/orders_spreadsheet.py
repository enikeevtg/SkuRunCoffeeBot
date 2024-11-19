import apiclient
from decouple import config
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.errors import HttpError
import logging


class OrdersSpreadsheet:
    """
    Orders google spreadsheet class
    """

    def __init__(self, spreadsheet_id, credentails_file):
        self.logger = logging.getLogger(__name__)
        self.spreadsheet_id = spreadsheet_id
        self.spreadsheet_url = ('https://docs.google.com/spreadsheets/d/' +
                                spreadsheet_id + '/edit')
        creds = ServiceAccountCredentials.from_json_keyfile_name(
                    credentails_file,
                    ['https://www.googleapis.com/auth/spreadsheets',
                    'https://www.googleapis.com/auth/drive'])
        httpAuth = creds.authorize(httplib2.Http())
        self.service = apiclient.discovery.build('sheets',
                                                 'v4',
                                                 http = httpAuth)
        self.__init_orders_spreadsheet()
        
    def __init_orders_spreadsheet(self) -> None:
        try:
            response = (
                self.service.spreadsheets()
                .values()
                .clear(
                    spreadsheetId=config('SPREADSHEET_ID'),
                    range=config('SHEET_NAME')
                )
                .execute()
            )

            response = (
                self.service.spreadsheets()
                .values()
                .append(
                    spreadsheetId=config('SPREADSHEET_ID'),
                    range=config('SHEET_NAME'),
                    valueInputOption="USER_ENTERED",
                    body={'values': [['Имя', 'Напиток', 'Статус']]}
                )
                .execute()
            )
            self.logger.info(f'response: {response}')

        except HttpError as error:
            self.logger.error(f'An error occured: {error}')

    def add_order(self,
                  tg_id: int,
                  username: str,
                  nickname: str,
                  drink: str):
        try:
            requests = []
            requests.append(
                {
                    "appendCells": {
                        "sheetId": 0,
                        "rows": [
                            {"values": [
                                {"userEnteredValue": {"stringValue": nickname}},
                                {"userEnteredValue": {"stringValue": drink}},
                                {"dataValidation": {
                                    "condition": {
                                        "type": "BOOLEAN",
                                        "values": [
                                            {"userEnteredValue": "OrderDone"}
                                        ]
                                    }
                                }}
                            ]}
                        ],
                        "fields": "*"
                    }
                }
            )

            body = {'requests': requests}
            response = (
                self.service.spreadsheets()
                .batchUpdate(spreadsheetId=config('SPREADSHEET_ID'), body=body)
                .execute()
            )
            self.logger.info(f'[{tg_id}, {username}: ' +
                             f'| {nickname} | {drink} | [ ] | ' +
                             'cells appended.]')
            return response

        except HttpError as error:
            self.logger.error(f'An error occured: {error}')
            return error
