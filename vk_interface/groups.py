from vk_interface.account import Account
from vk_api.exceptions import VkApiError

class Message():
    def print_error(self, error):
        print(error)
    
class Groups(Account):
    def __init__(self) -> None:
        super().__init__()
        self.message = Message()
    
    def getMembers(self, group_id):
        offset = 0
        all_members_ids = list()
        while True:
            next_members_ids = self.client.groups.getMembers(group_id=group_id, offset=offset)['items']

            if 0 == len(next_members_ids):
                break

            all_members_ids.extend(next_members_ids)

            offset += 1000
        
        return all_members_ids