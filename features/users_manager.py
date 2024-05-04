import json
from database.database import load, save
from vk_interface.users import Users

from vk_api.exceptions import VkApiError


class UsersManager():
    def __init__(self, user_ids) -> None:
        self.users = Users()
        self.deactivated_ids = set(load('deactivated_ids'))
        self.user_ids = self.__filter_out_deactivated_ids(user_ids)
        self.users_info = dict()
        self.old_online_ids = list()
        self.new_online_ids = set()
    
    def get_online(self):
        self.users_info = self.users.get(self.user_ids)
        activated_users = self.__filter_out_deactivated_users(self.users_info)
        available_users = self.__filter_out_private_users(activated_users)
        self.new_online_ids = self.__get_online_ids(available_users)
        actual_online_ids = self.__get_actual_online_ids(self.old_online_ids, self.new_online_ids)
        self.old_online_ids = self.new_online_ids
        return actual_online_ids
    
    def __filter_out_deactivated_users(self, users):
        deactivated_ids = {user['id'] for user in users if 'deactivated' in user}
        self.deactivated_ids.update(deactivated_ids)
        save('deactivated_ids', list(self.deactivated_ids))
        self.user_ids = self.__filter_out_deactivated_ids(self.user_ids)
        return [user for user in users if 'deactivated' not in user]

    def __filter_out_private_users(self, users):
        return [user for user in users if user['is_closed'] == False]

    def __filter_out_deactivated_ids(self, user_ids):
        return [id for id in user_ids if id not in self.deactivated_ids]

    def __get_online_ids(self, users_info: list):
        """Возвращает список ID пользователей онлайн"""
        try:
            return [user for user in users_info if 'online' in user and user['online']] 
        except VkApiError as error:
            print(error)
    
    def __get_actual_online_ids(self, old_online_users: list, new_online_users: list):
        """Возвращает ID новых пользователей, которые появились в онлайн после последнего обновления"""
        try:
            def convert_users_to_id(users: list) -> set:
                """Получить ID пользователей из списка словарей с информацией о пользователях"""
                return {user['id'] for user in users}
            
            new_online_ids = convert_users_to_id(new_online_users)
            old_online_ids = convert_users_to_id(old_online_users)
            
            actual_ids = new_online_ids.difference(old_online_ids)
            union_users = new_online_users + old_online_users

            return [user for user in union_users if user['id'] in actual_ids]
        except VkApiError as error:
            print(error)