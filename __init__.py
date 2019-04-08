from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.log import getLogger
import pymongo

LOGGER = getLogger(__name__)

URI = 'mongodb://root:password1@ds049446.mlab.com:49446/hackathon'
CLIENT = pymongo.MongoClient(URI)
DB = CLIENT.get_database()
USER = 'user'
lists = DB['lists']

class GroceryList(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.grocery_list = lists.find_one({'name': USER})['items']

    # Add item to grocery list
    @intent_file_handler('add_item.intent')
    def handle_add_item_intent(self, message):
        item = message.data.get("item")

        if item not in self.grocery_list:
            self.grocery_list.append(item)
            update_db(self.grocery_list)
            message = item + (' have' if item[len(item) - 1] == 's' else ' has')
            self.speak_dialog('add_success', data={'message': message})
        else:
            self.speak_dialog('add_error', data={'item': item})

    # Remove item from grocery list
    @intent_file_handler('remove_item.intent')
    def handle_remove_item_intent(self, message):
        item = message.data.get('item')

        if item not in self.grocery_list:
            self.speak_dialog('remove_error', data={'item': item})
        else:
            self.grocery_list.remove(item)
            update_db(self.grocery_list)
            message = item + (' have' if item[len(item) - 1] == 's' else ' has')
            self.speak_dialog('remove_success', data={'message': message})
            # Detect if item is plural for has/have


    # How many items are on my grocery list?
    @intent_file_handler('count_items.intent')
    def handle_count_items(self, message):
        plural = len(self.grocery_list) > 1
        verb = 'are' if plural else 'is'
        s = 's' if plural else ''
        self.speak_dialog('count_items', data={'n': len(self.grocery_list), 'verb': verb, 's': s})

    @intent_file_handler('list_items.intent')
    def handle_list_grocery(self, message):
        if len(self.grocery_list) > 0:
            self.speak_dialog("list_items")
            for item in self.grocery_list:
                self.speak(item)
        else:
            self.speak_dialog("empty_list")
        # self.speak_dialog('list.grocery')

def create_skill():
    return GroceryList()

def update_db(grocery_list: list):
    lists.update_one({'name': USER}, {'$set': {'items': grocery_list}}, upsert=True)
