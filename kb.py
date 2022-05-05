import telebot

# Клава Меню 1

keyboard0 = telebot.types.ReplyKeyboardMarkup(True, one_time_keyboard=True)
keyboard0.row('Установил')


# Клава Меню 1

keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('📑 Публиковать новость')
keyboard1.row('🔗 Ссылка', '❓ Инфо')



keyboard4 = telebot.types.InlineKeyboardMarkup()
key_1 = telebot.types.InlineKeyboardButton(text='1⃣', callback_data='1') 
key_2 = telebot.types.InlineKeyboardButton(text='2⃣', callback_data='2') 
key_3 = telebot.types.InlineKeyboardButton(text='3⃣', callback_data='3') 
keyboard4.add(key_1, key_2, key_3, row_width=3)



keyboard5 = telebot.types.ReplyKeyboardMarkup(True, one_time_keyboard=True)
keyboard5.row('✔ Отправить', '❌ Заного')
keyboard5.row('⬅ Меню')



keyboard6 = telebot.types.ReplyKeyboardMarkup(True)
keyboard6.row('1', '2', '3')

keyboard7 = telebot.types.InlineKeyboardMarkup()
key_donate1 = telebot.types.InlineKeyboardButton(text='Monobank', url='https://send.monobank.ua/3ctb86HEXd') 
key_donate2 = telebot.types.InlineKeyboardButton(text='PrivatBank', url='https://www.privat24.ua/rd/transfer_to_card?hash=rd/transfer_to_card/%7B%22from%22:%22%22,%22to%22:%224149%204991%203127%202146%22,%22ccy%22:%22UAH%22,%22amt%22:%22100%22%7D') 
keyboard7.add(key_donate1, key_donate2)


keyboard8 = telebot.types.ReplyKeyboardMarkup(True)
keyboard8.row('⬅ Назад')


