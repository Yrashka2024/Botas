import requests

class InlineButton:
    def __init__(self, text, callback_data):  
        self.text = text
        self.callback_data = callback_data

    def to_dict(self):
        return {
            'text': self.text,
            'callback_data': self.callback_data
        }

class InlineMenu:
    def __init__(self):  
        self.buttons = []

    def add(self, button):
        self.buttons.append(button)

    def to_dict(self):
        return [[button.to_dict() for button in self.buttons]]

class Bot:
    def __init__(self, token):  
        self.token = token
        self.base_url = f'https://api.telegram.org/bot{self.token}/'
        self.commands = {}
        self.callbacks = {}
        self.admins = {6953580337}  # ID администратора
        self.banned_users = set()    # Множество для хранения заблокированных пользователей

    def command(self, command_name):
        def decorator(func):
            self.commands[command_name] = func
            return func
        return decorator

    def callback(self, callback_data):
        def decorator(func):
            self.callbacks[callback_data] = func
            return func
        return decorator

    def get_updates(self, offset=None):
        url = self.base_url + 'getUpdates'
        params = {'offset': offset}
        response = requests.get(url, params=params)
        return response.json()

    def send_message(self, chat_id, text, reply_markup=None):
        url = self.base_url + 'sendMessage'
        payload = {'chat_id': chat_id, 'text': text}
        if reply_markup:
            payload['reply_markup'] = reply_markup
        response = requests.post(url, json=payload)
        return response.json()

    def send_inline_menu(self, chat_id, text, inline_menu):
        reply_markup = {'inline_keyboard': inline_menu.to_dict()}
        self.send_message(chat_id, text, reply_markup)

    def run(self):
        offset = None
        while True:
            updates = self.get_updates(offset)

            for update in updates.get('result', []):
                if 'message' in update:
                    chat_id = update['message']['chat']['id']
                    user_id = update['message']['from']['id']
                    command = update['message']['text']

                    if user_id in self.banned_users:
                        self.send_message(chat_id, "Вы заблокированы от использования этого бота.")
                        continue
                    
                    if command in self.commands:
                        self.commands[command](chat_id)

                elif 'callback_query' in update:
                    callback_query = update['callback_query']
                    callback_data = callback_query['data']
                    chat_id = callback_query['message']['chat']['id']

                    if callback_data in self.callbacks:
                        self.callbacks[callback_data](chat_id)

                offset = update['update_id'] + 1
                
    def is_admin(self, user_id):
        return user_id in self.admins
        
    def ban_user(self, user_id):
        self.banned_users.add(user_id)
        
    def unban_user(self, user_id):
        self.banned_users.discard(user_id)
