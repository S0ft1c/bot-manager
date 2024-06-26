from aiogram import Router
from .spam_settings_menu import router_spam_settings_menu
from .spam_add_w import router_spam_add_w
from .remove_spam_w import router_remove_spam_w
from .peresilka_change import router_peresilka_change
from .ssilka_change import router_ssilka_change
from .spam_sactions import router_spam_sanctions
from .lifetime_change import router_lifetime_change

router_spam_settings_handler = Router()

# include for all routers
router_spam_settings_handler.include_router(router_spam_settings_menu)
router_spam_settings_handler.include_router(router_spam_add_w)
router_spam_settings_handler.include_router(router_remove_spam_w)
router_spam_settings_handler.include_router(router_peresilka_change)
router_spam_settings_handler.include_router(router_ssilka_change)
router_spam_settings_handler.include_router(router_spam_sanctions)
router_spam_settings_handler.include_router(router_lifetime_change)
