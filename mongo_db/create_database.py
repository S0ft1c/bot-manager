from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
from bson.objectid import ObjectId
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

    async def get_group_names(self):
        try:
            ans = [el for el in self.chat_groups.find()]
            return ans
        except Exception as e:
            logger.error(e)

    async def get_all_chats_from_group_by_id(self, group_id: ObjectId):
        try:
            ans = [el
                   for el in self.chats.find({'group_id': str(group_id)})]
            return ans
        except Exception as e:
            logger.error(e)

    async def get_group_info_by_id(self, group_id):
        try:
            ans = [el
                   for el in self.chat_groups.find({"_id": ObjectId(group_id)})
                   ][0]

            logger.debug(f'the element is {ans}')
            return ans
        except Exception as e:
            logger.error(e)

    async def create_group(self, group_name: str):
        try:
            self.chat_groups.insert_one({'title': group_name})
        except Exception as e:
            logger.error(e)

    async def get_all_nongroup_chats(self):
        try:
            ans = [el for el in self.chats.find() if not el.get('group_id')]
            return ans
        except Exception as e:
            logger.error(e)

    async def add_chat_to_group_action(self, chat_id, group_id):
        try:
            update_op = {'$set': {'group_id': group_id}}
            fil = {'_id': int(chat_id)}
            self.chats.update_one(fil, update_op)
        except Exception as e:
            logger.error(e)

    async def remove_chat_from_group(self, chat_id):
        try:
            update_op = {'$set': {'group_id': ''}}
            fil = {'_id': int(chat_id)}
            self.chats.update_one(fil, update_op)
        except Exception as e:
            logger.error(e)

    async def delete_group(self, group_id):
        try:
            self.chat_groups.delete_one({'_id': ObjectId(group_id)})

            # update all data
            fil = {'group_id': group_id}
            update_op = {'$set': {'group_id': ''}}
            self.chats.update_many(fil, update_op)
        except Exception as e:
            logger.error(e)
