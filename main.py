import os
from time import sleep
from config.group_ids import groups_ids
from features.like_manager import  LikeManager
from utils import collect_ids
from features.users_manager import UsersManager
from vk_interface.friends import Friends


def main():
    like_manager = LikeManager()
    friends = Friends()
    # not_friends_ids = collect_ids(groups_ids)
    friends_ids = friends.get()
    
    users_manager = UsersManager(friends_ids)

    while True:
        os.system('cls')
        print(f"Всего лайков поставлено: {like_manager.like_calls}")
        online_users = users_manager.get_online()
        like_manager.add_likes_to_users(online_users)
        print('---end---')
        sleep(2)

if __name__ == "__main__":
    main()