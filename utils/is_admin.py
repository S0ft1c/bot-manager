from dotenv import load_dotenv
import os
from aiogram.types import Message


class IsAdmin:
    def __init__(self):
        load_dotenv()
        self.admins = [int(el)
                       for el in os.environ.get('ADMIN_LIST').split(';')
                       ]
        print(self.admins)

    def __call__(self, message: Message):
        return message.from_user.id in self.admins
