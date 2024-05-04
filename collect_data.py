from config.group_ids import groups_ids
from database.user_data_manager import UserDataManager
from utils import collect_ids




def main():
    ids = collect_ids(groups_ids)
    data_manager = UserDataManager()
    data_manager.collect_and_save_userdata(ids)
        

if __name__ == "__main__":
    main()