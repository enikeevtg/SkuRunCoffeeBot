from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config
import logging


admins_list = [int(admin_id) for admin_id in config('ADMINS').split(',')]

logfile = open('skurun.log', 'w')
format = "%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s"
logging.basicConfig(stream=logfile, level=logging.INFO, format=format)
logger = logging.getLogger(__name__)

session = AiohttpSession()
# session = AiohttpSession(proxy="http://proxy.server:3128")
bot = Bot(token=config('TOKEN'),
          session=session,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
