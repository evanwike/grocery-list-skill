from mycroft import MycroftSkill, intent_file_handler

__author__ = 'evanwike'
LOGGER = getLogger(__name__)

class GroceryList(MycroftSkill):
    def __init__(self):
        # MycroftSkill.__init__(self)
        super("GroceryList", self).__init__(name="GroceryList")
        self.grocery_list = []

    @intent_file_handler('add_item.intent')
    def handle_add_item_intent(self, message):
        try:
            item = message.data.get("item")
            self.grocery_list.append(item)
            self.speak_dialog("add_success", data=item)
        except:
            self.speak_dialog("add_error")

    @intent_file_handler('list.grocery.intent')
    def handle_list_grocery(self, message):
        self.speak_dialog('list.grocery')


def create_skill():
    return GroceryList()
