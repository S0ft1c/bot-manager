from aiogram import Router
from .create_ad import router_create_ad
from .get_ads import router_get_ads
from .edit_ad import router_edit_ad
from .del_ad import router_del_ad

router_ad_handlers = Router()

# include all needed routers
router_ad_handlers.include_router(router_create_ad)
router_ad_handlers.include_router(router_get_ads)
router_ad_handlers.include_router(router_edit_ad)
router_ad_handlers.include_router(router_del_ad)
