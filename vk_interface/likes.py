from time import sleep
from vk_interface.account import Account
from vk_api.exceptions import VkApiError

class Message():
    def print_add_like_status(self, user, index):
        print (f"Пользователю {user['first_name']} {user['last_name']} - https://vk.com/id{user['id']} поставлен лайк на пост номер [{index}]")

    def print_error(self, error , id):
        print(f"[{error}] - ID-[https://vk.com/id{id}]")

class Likes(Account):
    def __init__(self) -> None:
        super().__init__()
        self.message = Message()

    def add(self, **kwarg):
        try:
            status = self.client.likes.add(owner_id=kwarg['user']['id'], 
                                           type=kwarg['post']['type'], 
                                           item_id=kwarg['post']['id'])
            sleep(0.3)
            self.message.print_add_like_status(kwarg['user'], 
                                               kwarg['post_index'])
            return status
        
        except VkApiError as error:
            self.message.print_error(error, kwarg['user']['id'])
            return error
    
    def is_can_liked(self, **kwarg):
        try:
            return kwarg['post']['likes']['can_like']
        
        except VkApiError as error:
            self.message.print_error(error, kwarg['user']['id'])
            return error