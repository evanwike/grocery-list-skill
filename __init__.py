from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.log import getLogger
import pymongo

LOGGER = getLogger(__name__)

URI = 'mongodb://root:password1@ds049446.mlab.com:49446/hackathon'
CLIENT = pymongo.MongoClient(URI)
DB = CLIENT.get_default_database()

evan = DB['evan']
tondi = DB['tondi']

class GroceryList(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.grocery_list = []

    # Add item to grocery list
    @intent_file_handler('add_item.intent')
    def handle_add_item_intent(self, message):
        item = message.data.get("item")

        if item not in self.grocery_list:
            self.grocery_list.append(item)
        else:
            self.speak_dialog('add_error', data={'item': item})

        evan.insert_many(self.grocery_list)

        # Detect if item is plural for has/
        message = item + (' have' if item[len(item) - 1] == 's' else ' has')
        self.speak_dialog('add_success', data={'message': message})

    # Remove item from grocery list
    @intent_file_handler('remove_item.intent')
    def handle_remove_item_intent(self, message):
        item = message.data.get('item')

        if item not in self.grocery_list:
            self.speak_dialog('remove_error', data={'item': item})
        else:
            self.grocery_list.remove(item)

            # Detect if item is plural for has/have
            message = item + (' have' if item[len(item) - 1] == 's' else ' has')
            self.speak_dialog('remove_success', data={'message': message})

    # How many items are on my grocery list?
    @intent_file_handler('count_items.intent')
    def handle_count_items(self, message):
        self.speak_dialog('count_items', data={'n': len(self.grocery_list)})

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
