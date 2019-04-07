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

        # Detect if item is plural for has/
        message = item + (' have' if item[len(item) - 1] == 's' else ' has')
        self.speak_dialog('add_success', data={'message': message})

    # Remove item from grocery list
    @intent_file_handler('remove_item.intent')
    def handle_remove_item_intent(self, message):
        item = message.data.get('item')

        if item not in self.grocery_list:
            self.speak_dialog('remove_error')
        else:
            self.grocery_list.remove(item)

            # Detect if item is plural for has/have
            message = item + (' have' if item[len(item) - 1] == 's' else ' has')
            self.speak_dialog('remove_success', data={'message': message})

    # How many items are on my grocery list?
    @intent_file_handler('count_items.intent')
    def handle_count_items(self, message):
        self.speak_dialog('count_items', data={'n': len(self.grocery_list)})

    @intent_file_handler('list_items')
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
