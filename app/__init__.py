from aiogram import Router
from .admin_handlers import router_admin_handlers
from .chat_handlers import router_chat_handlers
from .group_handlers import router_group_handlers
from .ad_handlers import router_ad_handlers
from .answer_handlers import router_answer_handlers
from .top_rating import router_top_rating

router = Router()

# all routers include
router.include_router(router=router_admin_handlers)
router.include_router(router=router_chat_handlers)
router.include_router(router=router_group_handlers)
router.include_router(router=router_ad_handlers)
router.include_router(router=router_answer_handlers)
router.include_router(router=router_top_rating)
