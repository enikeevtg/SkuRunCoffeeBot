__all__ = "router"

from aiogram import Router

from .add_order_manually import router as add_order_router
from .admins_main import router as admins_main_router
from .cancel import router as cancel_router
from .dice import router as dice_router


router = Router(name=__name__)
router.include_routers(
    cancel_router,
    add_order_router,
    admins_main_router,
    dice_router,
)
