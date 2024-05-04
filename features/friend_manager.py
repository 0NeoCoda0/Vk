from time import sleep
from config.settings import WAITING_TIME
from vk_interface.friends import Friends
from vk_interface.users import Users

class FriendsManager():
    def __init__(self) -> None:
        self.friends = Friends()
        self.users = Users()
    
    def add_all_follower_to_friends(self):
        followers_list = self.users.get_followers()['items']
        
        for id in followers_list:        
            self.friends.add(id)
            sleep(WAITING_TIME)