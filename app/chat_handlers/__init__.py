from aiogram import Router
from .get_chat_info import router_get_chat_info
from .send_messages import router_send_messages
from .spam_setting_handlers import router_spam_settings_handler
from .admin_add_remove import router_admin_add_remove

router_chat_handlers = Router()

# all routers include
router_chat_handlers.include_router(router=router_get_chat_info)
router_chat_handlers.include_router(router=router_send_messages)
router_chat_handlers.include_router(router=router_spam_settings_handler)
router_chat_handlers.include_router(router=router_admin_add_remove)
