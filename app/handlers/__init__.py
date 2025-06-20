__all__ = "router"

from aiogram import Router

from .bio import router as bio_router
from .drink_order import router as drink_order_router
from .group_messages_handler import router as group_messages_handler_router
from .not_text_handler import router as not_text_handler_router
from .start import router as start_router
from .redirection import router as redirection_router

# from . import router as _router


router = Router(name=__name__)
router.include_routers(
    group_messages_handler_router,
    redirection_router,
    drink_order_router,
    start_router,
    bio_router,
    not_text_handler_router,
)
