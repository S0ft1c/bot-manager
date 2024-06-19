from aiogram import Router
from .warn_user import router_warn_user

router_answer_handlers = Router()

# include all needed routers
router_answer_handlers.include_router(router_warn_user)
