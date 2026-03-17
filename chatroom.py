from datetime import datetime

class Message:
    message_counter = 1

    def __init__(self, sender, content):
        self.sender = sender
        self.content = content
        self.id = Message.message_counter
        self.timestamp = datetime.now().strftime("%H:%M:%S")
        Message.message_counter += 1

    def __str__(self):
        return f"[{self.timestamp}] ({self.id}) {self.sender.username}: {self.content}"

class User:
    def __init__(self, username, role="user"):
        self.username = username
        self.role = role
        self.chatroom = None

    def join_chatroom(self, chatroom):
        if self.chatroom:
            print(f"{self.username} is already in a chatroom.")
        else:
            chatroom.add_user(self)
            self.chatroom = chatroom
            print(f"{self.username} joined {chatroom.name}")

    def leave_chatroom(self):
        if not self.chatroom:
            print(f"{self.username} is not in any chatroom.")
        else:
            self.chatroom.remove_user(self)
            print(f"{self.username} left {self.chatroom.name}")
            self.chatroom = None

    def send_message(self, content):
        if not self.chatroom:
            print(f"{self.username} cannot send a message (not in a chatroom).")
        else:
            self.chatroom.broadcast(self, content)

    def send_private(self, receiver_name, content):
        if self.chatroom:
            self.chatroom.private_message(self, receiver_name, content)
        else:
            print("Join a chatroom first!")


class ChatRoom:
    def __init__(self, name):
        self.name = name
        self.users = []
        self.messages = []

    def add_user(self, user):
        if user not in self.users:
            self.users.append(user)
        else:
            print(f"{user.username} is already in the chatroom.")

    def remove_user(self, user):
        if user in self.users:
            self.users.remove(user)

    def broadcast(self, sender, content):
        if len(content) > 100:
            print("Message too long!")
            return
        message = Message(sender, content)
        self.messages.append(message)
        print(message)

    def private_message(self, sender, receiver_name, content):
        for user in self.users:
            if user.username == receiver_name:
                print(f"[PRIVATE] {sender.username} → {receiver_name}: {content}")
                return
        print("User not found!")

    def show_chat_history(self):
        print(f"\n--- Chat History ({self.name}) ---")
        for msg in self.messages:
            print(msg)
        print()

    def search_messages(self, keyword):
        print(f"\nSearching for '{keyword}':")
        for msg in self.messages:
            if keyword.lower() in msg.content.lower():
                print(msg)

    def save_chat(self):
        with open("chat_history.txt", "w") as f:
            for msg in self.messages:
                f.write(str(msg) + "\n")
        print("Chat saved to file!")

if __name__ == "__main__":
    room = ChatRoom("Python Lounge")
    admin = User("Admin", role="admin")
    u1 = User("Alice")
    u2 = User("Bob")
    u3 = User("Charlie")
    
    admin.join_chatroom(room)
    u1.join_chatroom(room)
    u2.join_chatroom(room)
    
    u1.send_message("Hello everyone!")
    u2.send_message("Hi Alice!")
    
    u3.join_chatroom(room)
    u3.send_message("Hey guys!")
    u1.send_private("Bob", "How are you?")
    
    room.search_messages("hello")
    room.show_chat_history()
    room.save_chat()
    
    u1.leave_chatroom()
    u2.leave_chatroom()
    u3.leave_chatroom()
