from tqdm import tqdm
from database.user_data_manager import UserDataManager
from queries.ezo import EZO_KW
from queries.game_developers import GAMEDEV_KW
from statistic.statistical_methods import find_matches, filter_on_top

def find_relevance(info: dict, key_words, depth=2) -> dict:
    # Найти соотвествия из списка ключевых слов в данных 
    ids_matches = dict()
    for id, data in tqdm(info.items()):
        if data == None:
            continue
        for phrase in key_words:
            try:
                matches = find_matches(data, phrase)
                if matches > 1:
                    ids_matches[id] += matches
            except Exception:
                matches = find_matches(data, phrase)
                if matches == 0:
                    pass
                else:
                    ids_matches[id] = matches
    
    return filter_on_top(ids_matches, depth)

def main():
    info_manager = UserDataManager()
    info = info_manager.load_all_data()

    relevance_matches = dict(sorted(find_relevance(info, EZO_KW).items(), key=lambda x: x[1]))
    for id, matches in relevance_matches.items():
        print(f"https://vk.com/id{id} , эзотрик - {matches}")

if __name__ == "__main__":
    main()