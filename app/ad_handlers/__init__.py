from aiogram import Router
from .create_ad import router_create_ad

router_ad_handlers = Router()

# include all needed routers
router_ad_handlers.include_router(router_create_ad)
