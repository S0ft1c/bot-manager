from aiogram import Router
from .warn_user import router_warn_user
from .mute_user import router_mute_user
from .un_user import router_un_user
from .ban_user import router_ban_user
from .kick_user import router_kick_user

router_answer_handlers = Router()

# include all needed routers
router_answer_handlers.include_router(router_warn_user)
router_answer_handlers.include_router(router_mute_user)
router_answer_handlers.include_router(router_un_user)
router_answer_handlers.include_router(router_ban_user)
router_answer_handlers.include_router(router_kick_user)
