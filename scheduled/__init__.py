from .send_scheduled_messages import send_scheduled_messages
from asyncio import run


def schedule_worker(bot):
    run(send_scheduled_messages(bot))
