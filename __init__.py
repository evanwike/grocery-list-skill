from mycroft import MycroftSkill, intent_file_handler


class GroceryList(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('list.grocery.intent')
    def handle_list_grocery(self, message):
        self.speak_dialog('list.grocery')


def create_skill():
    return GroceryList()

