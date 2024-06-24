from aiogram import Router
from .hi_and_bye_menu import router_hi_and_bye_menu
from .bye_config import router_bye_config
from .bye_message_change import router_bye_message_change
from .bye_time_change import router_bye_time_change

router_hi_and_bye = Router()

# here all routers connection
router_hi_and_bye.include_routers(
    router_hi_and_bye_menu,
    router_bye_config,
    router_bye_message_change,
    router_bye_time_change
)
