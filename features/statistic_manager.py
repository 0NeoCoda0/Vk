from vk_interface.friends import Friends
from vk_interface.users import Users

class StatisticManager():
    def __init__(self) -> None:
        self.friends = Friends()
        self.users = Users()

    def show_followers_quantity(self):
        followers = self.users.get_followers()
        print(f"Количество подписчиков: {followers['count']}")

    def show_friends_quantity(self):
        friends_info = self.friends.get()
        print(f"Количество друзей: {friends_info['count']}")