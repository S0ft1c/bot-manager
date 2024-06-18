from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
from dotenv import load_dotenv
import os
from loguru import logger
load_dotenv()


class DB:
    def __init__(self):
        try:
            connection_string = os.environ.get('CONNECTION_STRING')
            # db_name = os.environ.get('DB_NAME')
            CONNECTION_STRING = connection_string
            self.client = MongoClient(CONNECTION_STRING)
            # create a database
            self.db = self.client.get_database('bot-manager-db')

            # create all nedded collections
            try:
                self.db.create_collection('chat-groups')
            except Exception as e:
                logger.warning('Collection chat-groups already exists')

            try:
                self.db.create_collection('chats')
            except Exception as e:
                logger.warning('Collection chats already exists')

            try:
                self.db.create_collection('schedule')
            except Exception as e:
                logger.warning('Collection schedule already exists')

            # adding all collections as self vars
            self.chats = self.db['chats']
            self.chat_groups = self.db['chat-groups']
            self.schedule = self.db['schedule']
        except Exception as e:
            logger.error(e)

    async def get_chats_info(self):
        return [el for el in self.chats.find()]

    async def insert_chat(self, data: dict) -> bool:
        try:
            candidates = [el for el in self.chats.find({'_id': data['_id']})]
            if candidates:
                return False

            self.chats.insert_one(data)
            return True
        except Exception as e:
            logger.error(e)

    async def get_chat_info_by_id(self, chatid: str):
        try:
            chat = [el for el in self.chats.find({'_id': int(chatid)})][0]
            logger.debug(chat)
            return chat
        except Exception as e:
            logger.error(e)

    async def schedule_message(self, data: dict):
        try:
            self.schedule.insert_one(data)
        except Exception as e:
            logger.error(e)

    async def get_scheduled_messages(self):
        try:
            msgs = [el for el in self.schedule.find()]
            return msgs
        except Exception as e:
            logger.error(e)

    async def delete_schedule_message_by_id(self, chatid: int):
        try:
            self.schedule.delete_one({"chatid": chatid})
        except Exception as e:
            logger.error(e)
