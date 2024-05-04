from tqdm import tqdm
from database.database import load, save
from vk_interface.friends import Friends
from vk_interface.users import Users


class UserDataManager():
    def __init__(self) -> None:
        self.users = Users()
        self.info = str()
        self.friends = Friends()
    
    def __collect_info(self, id):
        try:
            info_list = list()
            info = self.users.get(id)[0]
            if info['is_closed'] == True:
                return None
            
            for _, value in info.items():
                if not isinstance(value, dict) and not isinstance(value, list):
                    info_list.append(str(value))
            
            wall_info = ' '.join([post['text'] for post in self.users.get_wall(id, count=100)['items']])
            self.info = ' '.join(info_list) + wall_info


            return ' '.join(self.info.split())
        except Exception:
            return None

    def load_all_data(self):
        # Загрузить всю имеющуюся информацию на пользователей
        infos = load('users_info')
        return infos
    
    def collect_and_save_userdata(self, user_ids):
        all_data = self.load_all_data()
        exists_ids = list()
        for id, value in all_data.items():
            exists_ids.append(int(id))

        # Собрать и сохранить данные о тех пользователях, которых еще нет в базе.
        ids_infos = dict()
        for id in tqdm(user_ids):
            if id not in exists_ids:
                info = self.__collect_info(id)
                if info == None:
                    continue
                
                ids_infos[id] = info
            
                index = user_ids.index(id)
                if index % 10 == 0 and index != 0:
                    save('users_info', ids_infos)
                    ids_infos = dict()



