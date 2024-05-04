from tqdm import tqdm
from vk_interface.groups import Groups


def get_unique(objects):
    unique = list()
    for object in objects:
        if object not in unique:
            unique.append(object)
    return unique

def collect_ids(group_ids):
    vk_groups = Groups()
    all_ids = list()
    for _, group_id in tqdm(group_ids.items()):
        all_ids += vk_groups.getMembers(group_id) 
    print(f"[ИНФО] Количество собранных ID: {len(all_ids)}")
    return all_ids