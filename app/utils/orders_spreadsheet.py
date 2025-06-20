import asyncio
import aiohttp
from decouple import config
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.errors import HttpError
import logging


class GoogleSpreadsheetsRequests:
    """
    order google-spreadsheet requests class
    """

    def __init__(self, credentails_file, spreadsheet_id):
        self.logger = logging.getLogger(__name__)
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            filename=credentails_file,
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive",
            ],
        )
        self.url = (
            f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"
        )
        self.endpoint_url = (
            f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}"
        )
        asyncio.run(self.__init_orders_spreadsheet())

    async def __init_orders_spreadsheet(self) -> None:
        try:
            sheet_name = config("SHEET_NAME")
            await self.clear_request(sheet_name)
            values = {"values": [["Имя", "Напиток", "Статус"]]}
            await self.append_request(sheet_name, values)
        except HttpError as error:
            self.logger.error(f"An error occured: {error}")

    async def send_order(
        self, tg_id: int, username: str, nickname: str, drink: str
    ):
        try:
            body = {
                "requests": [
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
                                        {
                                            "userEnteredValue": {
                                                "stringValue": drink
                                            }
                                        },
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
                ]
            }
            response = await self.batchUpdate_request(body)
            self.logger.info(
                f"[{tg_id}, {username}: "
                + f"| {nickname} | {drink} | [ ] | "
                + "cells appended.]"
            )
            return response

        except HttpError as error:
            self.logger.error(f"An error occured: {error}")
            return error

    async def clear_request(self, sheet_name):
        endpoint = f"{self.endpoint_url}/values/{sheet_name}:clear?alt=json"
        response = await self.async_request("POST", endpoint)
        self.logger.info(f"response: {response}")

    async def append_request(self, sheet_name, body):
        endpoint = f"{self.endpoint_url}/values/{sheet_name}:append?valueInputOption=USER_ENTERED&alt=json"
        response = await self.async_request("POST", endpoint, body)
        self.logger.info(f"response: {response}")

    async def batchUpdate_request(self, body):
        endpoint = f"{self.endpoint_url}:batchUpdate?alt=json"
        response = await self.async_request("POST", endpoint, body)
        self.logger.info(f"response: {response}")

    async def async_request(self, method: str, url: str, body: dict = None):
        """
        async request method
        """
        token_info = self.credentials.get_access_token()
        headers = {
            "Authorization": f"Bearer {token_info.access_token}",
            "Content-Type": "application/json",
        }
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method, url=url, headers=headers, json=body
            ) as response:
                result = await response.json()
        return result
