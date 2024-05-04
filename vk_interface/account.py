from vk_api import VkApi
from config.token import TOKEN

class Account():
    def __init__(self) -> None:
        self.client = VkApi(token=TOKEN).get_api()