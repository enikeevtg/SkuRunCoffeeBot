from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config
import logging

from utils.orders_spreadsheet import OrdersSpreadsheet



logfile = open('skurun.log', 'w')
format = "%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s"
logging.basicConfig(stream=logfile, level=logging.INFO, format=format)
logger = logging.getLogger(__name__)

mode = config('MODE')
if mode == 'TEST':
    session = AiohttpSession()
elif mode == 'PROD':
    session = AiohttpSession(proxy="http://proxy.server:3128")
bot = Bot(token=config('TOKEN'),
          session=session,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
spreadsheet = OrdersSpreadsheet(config('SPREADSHEET_ID'),
                                config('CREDENTIALS_FILE'))
spreadsheet.spreadsheet_url
