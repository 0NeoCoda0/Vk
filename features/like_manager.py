from pprint import pprint
from time import sleep

from tqdm import tqdm
from config.settings import WAITING_TIME
from vk_interface.users import Users
from vk_interface.likes import Likes



class LikeManager():
    def __init__(self) -> None:
        self.users = Users()
        self.likes = Likes()
        self.like_calls = 0           
            
    def add_likes_to_users(self, users):
        walls = self.users.get_walls(users)
        for id, user_wall in walls.items():
            try:
                posts = user_wall['wall']
                for post in posts:
                        likes_parameters = dict(post=post, user=user_wall['user'], post_index=posts.index(post))
                        if self.likes.is_can_liked(**likes_parameters):
                            #Поставить лайк на следующий доступный пост
                            self.likes.add(**likes_parameters)
                            self.like_calls += 1
                            # sleep(WAITING_TIME)
                            break
                
                
            except Exception as error:
                try:
                    print(f"---- Пользователь: https://vk.com/id{user_wall['user']['id']} [{user_wall['user'][0]['first_name']} {user_wall['user']['last_name']}] - #{error}#")
                except Exception:
                    pass
        
        
    
    