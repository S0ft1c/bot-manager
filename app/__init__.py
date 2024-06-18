from aiogram import Router
from .admin_handlers import router_admin_handlers
from .chat_handlers import router_chat_handlers

router = Router()

# all routers include
router.include_router(router=router_admin_handlers)
router.include_router(router=router_chat_handlers)
