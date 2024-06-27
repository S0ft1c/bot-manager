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

            try:
                self.db.create_collection('users')
            except Exception as e:
                logger.warning('Collection users already exists')

            try:
                self.db.create_collection('messages')
            except Exception as e:
                logger.warning('Collection admins already exists')

            # adding all collections as self vars
            self.chats = self.db['chats']
            self.chat_groups = self.db['chat-groups']
            self.schedule = self.db['schedule']
            self.users = self.db['users']
            self.messages = self.db['messages']
        except Exception as e:
            logger.error(e)

    async def get_chats_info(self):
        return [el for el in self.chats.find()]

    async def delete_chat_by_id(self, chat_id):
        try:
            self.chats.delete_one({'_id': int(chat_id)})
        except Exception as e:
            logger.error(e)

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

    async def delete_schedule_message_by_group_id(self, group_id: int):
        try:
            self.schedule.delete_one({"group_id": group_id})
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

    async def get_group_by_chat_id(self, chat_id):
        try:
            chat = [el for el in self.chats.find({'_id': int(chat_id)})][0]
            group_id = chat['group_id']
            return group_id
        except Exception as e:
            logger.error(e)

    async def create_ad(self, data):
        try:
            data['all'] = True
            self.schedule.insert_one(data)
        except Exception as e:
            logger.error(e)

    async def get_chats(self):
        try:
            chats = [el for el in self.chats.find()]
            return chats
        except Exception as e:
            logger.error(e)

    async def delete_schedule_message_by_obj_id(self, obj_id):
        try:
            self.schedule.delete_one({'_id': obj_id})
        except Exception as e:
            logger.error(e)

    async def get_all_ads(self):
        try:
            ads = [el for el in self.schedule.find({'all': True})]
            return ads
        except Exception as e:
            logger.error(e)

    async def get_ad_by_id(self, ad_id):
        try:
            ad = [el for el in self.schedule.find({'_id': ObjectId(ad_id)})][0]
            return ad
        except Exception as e:
            logger.error(e)

    async def edit_ad(self, ad_info: dict):
        try:
            self.schedule.delete_one({'_id': ObjectId(ad_info['prev_id'])})
            ad_info.pop('prev_id')
            ad_info['all'] = True
            self.schedule.insert_one(ad_info)
        except Exception as e:
            logger.error(e)

    async def del_ad(self, ad_id):
        try:
            self.schedule.delete_one({'_id': ObjectId(ad_id)})
        except Exception as e:
            logger.error(e)

    async def add_spam_w_to_chat(self, chat_id, words: list):
        try:
            chat_data = [el
                         for el in self.chats.find({'_id': int(chat_id)})
                         ][0]
            spam_w: list = chat_data.get('spam_w', [])
            spam_w.extend(words)
            spam_w = list(set(spam_w))
            self.chats.update_one(
                filter={'_id': int(chat_id)},
                update={'$set': {'spam_w': spam_w}}
            )
        except Exception as e:
            logger.error(e)

    async def remove_spam_w_from_chat(self, chat_id, words: list):
        try:
            chat_data = [el
                         for el in self.chats.find({'_id': int(chat_id)})
                         ][0]
            spam_w = set(chat_data.get('spam_w', []))
            spam_w = list(spam_w - set(words))
            self.chats.update_one(
                filter={'_id': int(chat_id)},
                update={'$set': {'spam_w': spam_w}}
            )
        except Exception as e:
            logger.error(e)

    async def peresilka_change(self, chat_id):
        try:
            peresilka = [el
                         for el in self.chats.find({'_id': int(chat_id)})
                         ][0]
            peresilka = peresilka.get('peresilka', False)
            logger.debug(f'peresilka now -> {not peresilka}')
            self.chats.update_one(
                filter={'_id': int(chat_id)},
                update={'$set': {'peresilka': not peresilka}}
            )
        except Exception as e:
            logger.error(e)

    async def get_peresilka(self, chat_id):
        try:
            return [el for el in self.chats.find({'_id': int(chat_id)})][0].get('peresilka', False)
        except Exception as e:
            logger.error(e)

    async def ssilka_change(self, chat_id):
        try:
            ssilka = [el
                      for el in self.chats.find({'_id': int(chat_id)})
                      ][0]
            ssilka = ssilka.get('ssilka', True)
            logger.debug(f'ssilka now -> {not ssilka}')
            self.chats.update_one(
                filter={'_id': int(chat_id)},
                update={'$set': {'ssilka': not ssilka}}
            )
        except Exception as e:
            logger.error(e)

    async def get_ssilka(self, chat_id):
        try:
            return [el for el in self.chats.find({'_id': int(chat_id)})][0].get('ssilka', True)
        except Exception as e:
            logger.error(e)

    async def add_warn_to_user(self, user_id):
        try:
            user = [el for el in self.users.find({'_id': int(user_id)})]
            if not user:
                self.users.insert_one({'_id': int(user_id)})
                w = 0
            else:
                w = user[0]['warn']
            self.users.update_one(
                filter={'_id': int(user_id)},
                update={'$set': {'warn': w + 1}}
            )
        except Exception as e:
            logger.error(e)

    async def update_sanction_in_chat(self, chat_id, sanction):
        try:
            self.chats.update_one(
                filter={'_id': int(chat_id)},
                update={'$set': {'sanction': sanction}}
            )
        except Exception as e:
            logger.error(e)

    async def update_secs_in_chat(self, chat_id, secs):
        try:
            self.chats.update_one(
                filter={'_id': int(chat_id)},
                update={'$set': {'secs': secs}}
            )
        except Exception as e:
            logger.error(e)

    async def save_message(self, message: dict):
        try:
            self.messages.insert_one(message)
        except Exception as e:
            logger.error(e)

    async def get_users_messages_for_del(self, chat_id, user_id):
        try:
            msgs = [el for el in self.messages.find(
                {'chat_id': int(chat_id), 'user_id': int(user_id)}
            )]
            self.messages.delete_many(
                filter={'chat_id': int(chat_id), 'user_id': int(user_id)}
            )
            return msgs
        except Exception as e:
            logger.error(e)

    async def update_warn_message(self, chat_id, msg):
        try:
            self.chats.update_one(
                filter={'_id': int(chat_id)},
                update={'$set': {'warn_msg': msg}}
            )
        except Exception as e:
            logger.error(e)

    async def update_mute_message(self, chat_id, msg):
        try:
            self.chats.update_one(
                filter={'_id': int(chat_id)},
                update={'$set': {'mute_msg': msg}}
            )
        except Exception as e:
            logger.error(e)

    async def update_ban_message(self, chat_id, msg):
        try:
            self.chats.update_one(
                filter={'_id': int(chat_id)},
                update={'$set': {'ban_msg': msg}}
            )
        except Exception as e:
            logger.error(e)

    async def update_kick_message(self, chat_id, msg):
        try:
            self.chats.update_one(
                filter={'_id': int(chat_id)},
                update={'$set': {'kick_msg': msg}}
            )
        except Exception as e:
            logger.error(e)

    async def update_un_message(self, chat_id, msg):
        try:
            self.chats.update_one(
                filter={'_id': int(chat_id)},
                update={'$set': {'un_msg': msg}}
            )
        except Exception as e:
            logger.error(e)

    async def get_text_conf(self, chat_id, type):
        try:
            op = f'{type}_msg'
            ttt = [el for el in self.chats.find({'_id': int(chat_id)})][0]
            return ttt[op]
        except Exception as e:
            logger.error(e)

    async def get_secs(self, chat_id):
        try:
            return [el for el in self.chats.find({'_id': int(chat_id)})][0]['secs']
        except Exception as e:
            logger.error(e)

    async def get_spam_w(self, chat_id):
        try:
            return [el for el in self.chats.find({'_id': int(chat_id)})][0].get('spam_w', [])
        except Exception as e:
            logger.error(e)

    async def get_sanction(self, chat_id):
        try:
            return [el for el in self.chats.find({'_id': int(chat_id)})][0].get('sanction', 'warn')
        except Exception as e:
            logger.error(e)

    async def get_reputation_w(self, chat_id):
        try:
            return [el for el in self.chats.find({'_id': int(chat_id)})][0].get('reputation_w', [])
        except Exception as e:
            logger.error(e)

    async def get_rep_sys_workin(self, chat_id):
        try:
            return [el for el in self.chats.find({'_id': int(chat_id)})][0].get('rep_sys_workin', False)
        except Exception as e:
            logger.error(e)

    async def add_rep_to_user(self, chat_id, user_id):
        try:
            chat = [el for el in self.chats.find({'_id': int(chat_id)})][0]
            if not chat.get('user_rep', False):
                self.chats.update_one(
                    filter={'_id': int(chat_id)},
                    update={'$set': {'user_rep': {str(user_id): 1}}}
                )
            else:
                user_rep = chat.get('user_rep', {})
                user_rep[str(user_id)] = user_rep.get(str(user_id), 0) + 1
                self.chats.update_one(
                    filter={'_id': int(chat_id)},
                    update={'$set': {'user_rep': user_rep}}
                )
        except Exception as e:
            logger.error(e)

    async def get_all_messages_from_chat(self, chat_id):
        try:
            msgs = [el for el in self.messages.find({'chat_id': int(chat_id)})]
            return msgs
        except Exception as e:
            logger.error(e)

    async def get_user_rep(self, chat_id):
        try:
            user_rep = [el for el in self.chats.find(
                {'_id': int(chat_id)})][0].get('user_rep', [])
            return user_rep
        except Exception as e:
            logger.error(e)

    async def rep_sys_workin_change(self, chat_id):
        try:
            rep_sys_workin = [el
                              for el in self.chats.find({'_id': int(chat_id)})
                              ][0]
            rep_sys_workin = rep_sys_workin.get('rep_sys_workin', False)
            self.chats.update_one(
                filter={'_id': int(chat_id)},
                update={'$set': {'rep_sys_workin': not rep_sys_workin}}
            )
        except Exception as e:
            logger.error(e)

    async def add_rep_w_to_chat(self, chat_id, words: list):
        try:
            chat_data = [el
                         for el in self.chats.find({'_id': int(chat_id)})
                         ][0]
            spam_w: list = chat_data.get('reputation_w', [])
            spam_w.extend(words)
            spam_w = list(set(spam_w))
            self.chats.update_one(
                filter={'_id': int(chat_id)},
                update={'$set': {'reputation_w': spam_w}}
            )
        except Exception as e:
            logger.error(e)

    async def remove_rep_w_from_chat(self, chat_id, words: list):
        try:
            chat_data = [el
                         for el in self.chats.find({'_id': int(chat_id)})
                         ][0]
            reputation_w = set(chat_data.get('reputation_w', []))
            reputation_w = list(reputation_w - set(words))
            self.chats.update_one(
                filter={'_id': int(chat_id)},
                update={'$set': {'reputation_w': reputation_w}}
            )
        except Exception as e:
            logger.error(e)

    async def get_bye_config(self, chat_id):
        try:
            return [el for el in self.chats.find({'_id': int(chat_id)})][0].get('bye_config', {})
        except Exception as e:
            logger.error(e)

    async def update_bye_message(self, chat_id, message):
        try:
            bbb = [el for el in self.chats.find(
                {'_id': int(chat_id)})][0].get('bye_config', {})
            bbb['message'] = message

            self.chats.update_one(
                filter={'_id': int(chat_id)},
                update={'$set': {'bye_config': bbb}}
            )
        except Exception as e:
            logger.error(e)

    async def update_bye_sleep_time(self, chat_id, sleep_time):
        try:
            bbb = [el for el in self.chats.find(
                {'_id': int(chat_id)})][0].get('bye_config', {})
            bbb['sleep_time'] = sleep_time

            self.chats.update_one(
                filter={'_id': int(chat_id)},
                update={'$set': {'bye_config': bbb}}
            )
        except Exception as e:
            logger.error(e)

    async def get_came_users(self, chat_id, user_id):
        try:
            return [el for el in self.chats.find({'_id': int(chat_id)})][0].get(str(user_id), [])
        except Exception as e:
            logger.error(e)

    async def ref_user_came(self, chat_id, user_id, event_user_id):
        try:
            user_id = str(user_id)
            event_user_id = str(event_user_id)
            ch_info = [el for el in self.chats.find({'_id': int(chat_id)})][0]
            user_info = ch_info.get(user_id, [])
            user_info.append(event_user_id)
            user_info.append(user_id)
            self.chats.update_one(
                filter={'_id': int(chat_id)},
                update={'$set': {user_id: user_info}}
            )
        except Exception as e:
            logger.error()

    async def get_hi_config(self, chat_id):
        try:
            return [el for el in self.chats.find({'_id': int(chat_id)})][0].get('hi_config', {})
        except Exception as e:
            logger.error(e)

    async def create_new_hi_config(self, chat_id, typee: str):
        try:
            self.chats.update_one(
                filter={'_id': int(chat_id)},
                update={'$set': {'hi_config': {'type': typee}}}
            )
        except Exception as e:
            logger.error(e)

    async def erase_hi_config(self, chat_id):
        try:
            self.chats.update_one(
                filter={'_id': int(chat_id)},
                update={'$set': {'hi_config': {}}}
            )
        except Exception as e:
            logger.error(e)

    async def change_hi_message(self, chat_id, message):
        try:
            hhh = [el for el in self.chats.find(
                {'_id': int(chat_id)})][0].get('hi_config', {})
            hhh['message'] = message

            self.chats.update_one(
                filter={'_id': int(chat_id)},
                update={'$set': {'hi_config': hhh}}
            )
        except Exception as e:
            logger.error(e)

    async def update_hi_sleep_time(self, chat_id, sleep_time):
        try:
            hhh = [el for el in self.chats.find(
                {'_id': int(chat_id)})][0].get('hi_config', {})
            hhh['sleep_time'] = sleep_time

            self.chats.update_one(
                filter={'_id': int(chat_id)},
                update={'$set': {'hi_config': hhh}}
            )
        except Exception as e:
            logger.error(e)

    async def update_members_change(self, chat_id, cnt):
        try:
            hhh = [el for el in self.chats.find(
                {'_id': int(chat_id)})][0].get('hi_config', {})
            hhh['members_came'] = cnt

            self.chats.update_one(
                filter={'_id': int(chat_id)},
                update={'$set': {'hi_config': hhh}}
            )
        except Exception as e:
            logger.error(e)

    async def add_channel_to_hi(self, chat_id, link):
        try:

            hhh = [el for el in self.chats.find(
                {'_id': int(chat_id)})][0].get('hi_config', {})
            arr: list = hhh.get('channels', [])
            arr.append(link)
            hhh['channels'] = arr

            self.chats.update_one(
                filter={'_id': int(chat_id)},
                update={'$set': {'hi_config': hhh}}
            )
        except Exception as e:
            logger.error(e)

    async def rmv_channel_from_hi(self, chat_id, link):
        try:

            hhh = [el for el in self.chats.find(
                {'_id': int(chat_id)})][0].get('hi_config', {})
            arr: list = hhh.get('channels', [])
            arr.remove(link)
            hhh['channels'] = arr

            self.chats.update_one(
                filter={'_id': int(chat_id)},
                update={'$set': {'hi_config': hhh}}
            )
        except Exception as e:
            logger.error(e)
