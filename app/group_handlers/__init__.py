from aiogram import Router
from .group_info import router_group_info
from .create_group import router_create_group
from .add_chat_to_group import router_add_chat_to_group

router_group_handlers = Router()

# include all other routers
router_group_handlers.include_router(router=router_group_info)
router_group_handlers.include_router(router=router_create_group)
router_group_handlers.include_router(router=router_add_chat_to_group)
