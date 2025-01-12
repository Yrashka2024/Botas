from botas.bot import Bot, InlineMenu, InlineButton  # Импортируем класс бота и необходимые классы

TOKEN = '7853209724:AAG8mTrUnjl1lcYPWDyAc4knu9Aqcu35JXY'  # Укажите ваш токен бота

bot = Bot(TOKEN)

@bot.command("/start")
def start_command(chat_id):
    bot.send_message(chat_id, "Добро пожаловать! Это ваш бот администрирования.")

@bot.command("/menu")
def menu_command(chat_id):
    inline_menu = InlineMenu()
    inline_menu.add(InlineButton("Добавить администратора", "menu_add_admin"))
    inline_menu.add(InlineButton("Заблокировать пользователя", "menu_ban_user"))
    inline_menu.add(InlineButton("Разблокировать пользователя", "menu_unban_user"))
    bot.send_inline_menu(chat_id, "Выберите действие:", inline_menu)

@bot.callback("menu_add_admin")
def add_admin_callback(chat_id):
    # Замените на ID пользователя, которого хотите сделать администратором
    user_id = 1234567890  
    if bot.is_admin(user_id):
        bot.send_message(chat_id, f"Пользователь {user_id} уже администратор.")
    else:
        bot.admins.add(user_id)
        bot.send_message(chat_id, f"Пользователь {user_id} добавлен как администратор.")

@bot.callback("menu_ban_user")
def ban_user_callback(chat_id):
    # Ваш код получения ID пользователя
    user_id = 1234567890  
    bot.ban_user(user_id)
    bot.send_message(chat_id, f"Пользователь с ID {user_id} заблокирован.")

@bot.callback("menu_unban_user")
def unban_user_callback(chat_id):
    # Ваш код получения ID пользователя
    user_id = 1234567890  
    bot.unban_user(user_id)
    bot.send_message(chat_id, f"Пользователь с ID {user_id} разблокирован.")

# Запускаем бота
if __name__ == "__main__":
    bot.run()

