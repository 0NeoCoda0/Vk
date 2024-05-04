import asyncio
from tqdm import tqdm
from utils import get_unique
from vk_interface.account import Account
from vk_api.exceptions import VkApiError
from config.settings import DEPTH_OF_IMMERSION, USER_FIELDS

class Message():
    def delete_success(self, user_id):
        print(f"[ИНФО] Пользователь {user_id} удален из списка подписчиков")

    def collect_user_data(self):
        print(f"[ИНФО] Собираю информацию о пользователях")

    def error(self, error):
        print(f"[ОШИБКА] {error}")


class Users(Account):
    def __init__(self) -> None:
        super().__init__()
        self.message = Message()

    def get_followers(self):
        try:
            return self.client.users.getFollowers()
        except VkApiError as error:
            # self.message.error(error)
            return error
    
    def get(self, user_ids):
        if isinstance(user_ids, int) or isinstance(user_ids, str):
            return self.client.users.get(user_ids=user_ids, fields=USER_FIELDS)

        try:
            self.message.collect_user_data()
            offset = 0
            step = 1000
            iteration_length = len(user_ids) // step + 1
            users_list = list()
            for _ in tqdm(range(iteration_length)):  
                users_list.extend(self.client.users.get(user_ids=user_ids[offset:offset+step], fields=USER_FIELDS))
                offset += step
            
            unique = self.__get_unique_users(users_list)
            print(f"[ИНФО]Уникальных пользователей всего {len(unique)}")
            return unique
        
        except VkApiError as error:
            # self.message.error(error)
            return error

    def get_wall(self, owner_id, offset=0, count=DEPTH_OF_IMMERSION):
        try:
            result = self.client.wall.get(owner_id=owner_id, offset=offset, count=count)
            return result
        except VkApiError as error:
            # self.message.error(error)
            return error.error['error_code']
        
    def __get_unique_users(self, users):
        unique_ids = list()
        unique_users = list()
        for user in users:
            if user['id'] not in unique_ids:
                unique_users.append(user)
                unique_ids.append(user['id'])
        
        return unique_users
    
    def get_walls(self, users, offset=0, count=DEPTH_OF_IMMERSION):
        def deconstruct_on(items, lenght):
            result = list()
            for i in range(len(items)):
                if i % 25 == 0 or i == 0:
                    result.append(items[i:i+lenght])
            return result

        walls_list = list()
        walls_dict = dict()
        result = dict()
        user_ids = [user['id'] for user in users]
        try:
            for ids in tqdm(deconstruct_on(user_ids, 25)):
                code = """
                    var walls = {};
                    var offset = %d;
                    var count = %d;
                    
                    // Цикл для получения стен от разных пользователей
                    %s
                    
                    return walls;
                """ % (offset, count, self._generate_wall_get_code(ids))
                
                walls_list += self.client.execute(code=code)

            for wall in tqdm(walls_list):
                for user in users:
                    if user['id'] == wall['owner_id']:
                        walls_dict[user['id']] = {'user': user, 'wall': wall['items']}
            
            return walls_dict
        except VkApiError as error:
            # self.message.error(error)
            return error.error['error_code']
    
    def _generate_wall_get_code(self, owner_ids):
        code = ""
        for owner_id in owner_ids:
            code += """
                var wall = API.wall.get({"owner_id": %s, "offset": offset, "count": count});
                walls.push({"owner_id": %s, "items": wall.items});
            """ % (owner_id, owner_id)
        return code