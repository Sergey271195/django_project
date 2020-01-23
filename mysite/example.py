class Message():
    message_parent = "Hi Parent"

    def __init__(self):
        self.message = "Hi Son"

    def change_son(self):
        self.message = "Hi son?"

    def change_parent(self):
        Message.message_parent = "Hi Parnet?"

son1 = Message()
son1.change_parent()

son2 = Message()
print(son1.message_parent)
print(son2.message_parent)