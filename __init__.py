from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.log import getLogger

LOGGER = getLogger(__name__)

class GroceryList(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.grocery_list = []

    # Add item to grocery list
    @intent_file_handler('add_item.intent')
    def handle_add_item_intent(self, message):
        item = message.data.get("item")
        self.grocery_list.append(item)
        self.speak_dialog("add_success", data={'item': item})

    # Remove item from grocery list
    @intent_file_handler('remove_item.intent')
    def handle_remove_item_intent(self, message):
        item = message.data.get('item')

        if item not in self.grocery_list:
            self.speak_dialog('remove_error')
        else:
            self.grocery_list.remove(item)
            self.speak_dialog('remove_success', data={'item': item})

    @intent_file_handler('list.grocery.intent')
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
