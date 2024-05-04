from vk_interface.account import Account
from vk_api.exceptions import VkApiError

class Message():
    def print_status(self, status: int, user_id):
        if status == 1:
            print(f"Заявка на добавление {user_id} в друзья отправлена")
        elif status == 2:
            print(f"Заявка на добавление в друзья от {user_id} в друзья принята")
        elif status == 4:
            print(f"Повторная отправка заявки {user_id}")
        else:
            print(f"Пользователь {user_id} - [{status}]")
        
    def print_error(self, error , id):
        print(f"[{error}] - ID-[https://vk.com/id{id}]")

class Friends(Account):
    def __init__(self) -> None:
        super().__init__()
        self.message = Message()

    def get_requests(self):
        try:
            return self.client.friends.getRequests()
        except VkApiError as error:
            return error
    
    def get(self, user_id=None, count=5000):
        try:
            return self.client.friends.get(user_id=user_id, count=count)['items']
        except VkApiError as error:
            return error
    
    def get_mutual(self, target_uids):
        try:
            return self.client.friends.getMutual(target_uids=target_uids)
        
        except VkApiError as error:
            return error

    def add(self, user_id):
        try:
            status = self.client.friends.add(user_id=user_id)
            self.message.print_status(status, user_id)
            return status
        
        except VkApiError as error:
            self.message.print_error(error, user_id)
            return error
        
    def delete(self, user_id):
        try:
            status = self.client.friends.delete(user_id=user_id)
            self.message.print_status(status, user_id)
            return status
        
        except VkApiError as error:
            self.message.print_error(error, user_id)
            return error
