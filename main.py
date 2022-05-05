import telebot
import datetime as DT
import kb
from db import SQLighter


admin = '576688754'
db = SQLighter('db.sqlite')
print("Зашёл в БД")
bot = telebot.TeleBot('TOKEN')


@bot.message_handler(commands=['start'])
def start_message(message): 
    db = SQLighter('db.sqlite')

    name = message.from_user.first_name
    username = message.from_user.username
    user_id = message.from_user.id

    referrer_candidate = None
    if " " in message.text:
        referrer_candidate = message.text.split()[1]
        try:
            referrer_candidate = int(referrer_candidate)

        except ValueError:
            pass


    if(not db.user_exists_tg(user_id)):
        if username:
            db.add_user_tg(user_id, username, name)
            bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEEohZic7yYpKX0cmFu0vpyIOjCHfdb2gACAQEAAladvQoivp8OuMLmNCQE')
            bot.send_message(message.chat.id, 'Привет, '+ name + ', рад познакомиться! 💜\n\n*Немного расскажу про себя*\n\nЯ - это аналог телеграм каналам, имея свои *фишки*\n\nУ меня ты сможешь рассылать свои истории и новости\nИ при этом, указывать того, кто сможет их увидеть\n\nЧто-то на подобии *Лучших друзей* в Instagram\n\nЕсли остались вопросы, узнавай в *Инфо*❓', parse_mode="MARKDOWN", reply_markup=kb.keyboard1) 
            bot.send_message(admin, '🚫 Запуск бота\n\n💎 Имя:  ' + name + '\n⭐ Тег:  @' + str(username) + '\n📝 ID:  ' + str(user_id)) 

            if referrer_candidate != None:
                if(not db.reader_exists(user_id, referrer_candidate)):
                    db.add_publisher_and_user(referrer_candidate, user_id, name)
                    bot.send_message(user_id, f'Ты подписался на новости от [Него/Неё](tg://user?id={referrer_candidate})', parse_mode="MARKDOWN")
                    bot.send_message(referrer_candidate, f'📗 У вас *новый читатель* [{name}](tg://user?id={user_id})!\n\n*Выберите 1-3*\n\n1 - Лучший друг\n2 - Утка\n3 - Обычный друг', parse_mode="MARKDOWN", reply_markup=kb.keyboard4)
                else:
                    bot.send_message(user_id, 'Ты уже подписан на *того*, по чьей ссылке перешёл', parse_mode="MARKDOWN")

        else:
            PATH = 'settings.jpg'
            bot.send_photo(message.chat.id, photo=open(PATH, 'rb'), caption='❗ Для пользования ботом установите *Имя пользователя* в *Настройках*', reply_markup=kb.keyboard0, parse_mode="MARKDOWN")
          
    else:
        bot.send_message(message.chat.id, 'Привет, '+ name + ', рад снова тебя видеть!', reply_markup=kb.keyboard1) 

        if referrer_candidate != None:
            if(not db.reader_exists(user_id, referrer_candidate)):
                db.add_publisher_and_user(referrer_candidate, user_id, name)
                bot.send_message(user_id, f'Ты подписался на новости от [Него/Неё](tg://user?id={referrer_candidate})', parse_mode="MARKDOWN")
                bot.send_message(referrer_candidate, f'📗 У вас *новый читатель* [{name}](tg://user?id={user_id})!\n\n*Выберите 1-3*\n\n1 - Лучший друг\n2 - Утка\n3 - Обычный друг', parse_mode="MARKDOWN", reply_markup=kb.keyboard4)
            else:
                bot.send_message(user_id, 'Ты уже подписан на *того*, по чьей ссылке перешёл', parse_mode="MARKDOWN")

        else:
            pass

@bot.message_handler(commands=['donate'])
def send_donate_sys(message): 
    chat_id = message.from_user.id
    bot.send_message(chat_id, text='💜 Тута можно поддержать разрабочика\n💜 Ссылки вы видите снизу ', reply_markup=kb.keyboard7)


@bot.message_handler(content_types=['text'])
def send_text(message):
    db = SQLighter('db.sqlite')
    user_id = message.from_user.id
    name = message.from_user.first_name
    username = message.from_user.username

    if message.text.lower() == 'установил':
        bot.send_message(message.chat.id, 'Теперь заного перейди по той ссылке, с помощью который, ты попал сюда.\nЕсли же зашёл сам, то жми - /start') 

    if message.text.lower() == '❓ инфо':
        list_Readers = db.take_readers_list(user_id)
        list_Publishers = db.take_publisher_list(user_id)
        bot.send_message(message.chat.id, f'*Информация* 📌\n\nВы подписаны на *{len(list_Publishers)} людей*\nНа вас подписаны *{len(list_Readers)} людей*\n\n*Как использовать бота* ❔\n\nПолучаете ссылку - [Ссылка 🔗]\nРазсылаете её друзьям, знакомым\n\nПубликуете новость - [Публиковать 📑]\n\nВыбираете кто будет видеть\n*Пример:* 2 - увидят все кроме обычных друзей!\n\n*Вспомогательные команды 🛠*\n\nПерезапустить бота - /start\nПоддержать проект - /donate\n\n*Остались вопросы* - @ullneverknow 🔧', parse_mode="MARKDOWN") 
        

    if message.text.lower() == '📑 публиковать новость':
        msg = bot.send_message(message.from_user.id, text=f'Всё, что ты напишешь мне тут, я доставлю твоим друзьям\nЭто может быть *видео, голосовое или фото и текст*\n\nДумай и отправляй, *я жду*',parse_mode="MARKDOWN", reply_markup=kb.keyboard8)
        bot.register_next_step_handler(msg, new_publication)

    if message.text.lower() == '🔗 ссылка':
        bot.send_message(message.from_user.id, text='По ней, на тебя могут подписываться друзья\nИ в дальнейшем читать твои новости\n\n🔗 t.me/pubduck_bot?start=' + str(user_id))


@bot.callback_query_handler(func=lambda call: True) 
def callback_worker(call): 

    db = SQLighter('db.sqlite')
    user_id = call.from_user.id
    msg=call.message.id
    reader_id = call.message.json.get('entities')[1].get('user').get('id')
    reader_name = call.message.json.get('entities')[1].get('user').get('first_name')


    if call.data == "1": 
        trust = 1
        db.select_trust_for_reader(user_id, reader_id, trust)
        bot.edit_message_text(text=f'Вы выбрали *Лучший друг* для [{reader_name}](tg://user?id={reader_id})', message_id=msg, chat_id=user_id, parse_mode="MARKDOWN")

    if call.data == "2": 
        trust = 2
        db.select_trust_for_reader(user_id, reader_id, trust)
        bot.edit_message_text(text=f'Вы выбрали *Утка* для [{reader_name}](tg://user?id={reader_id})', message_id=msg, chat_id=user_id, parse_mode="MARKDOWN")

    if call.data == "3":  
        trust = 3
        db.select_trust_for_reader(user_id, reader_id, trust)
        bot.edit_message_text(text=f'Вы выбрали *Обычный друг* для [{reader_name}](tg://user?id={reader_id})', message_id=msg, chat_id=user_id, parse_mode="MARKDOWN")



def new_publication(msg):
    db = SQLighter('db.sqlite')
    user_id = msg.from_user.id

    if msg.text == '⬅ Назад':
        bot.send_message(msg.from_user.id, text=f'❗ Вы возвращены в Меню', reply_markup=kb.keyboard1)
        
    else:
        msgid = msg.id
        db.new_publicationID(user_id, msgid)
        msg = bot.send_message(msg.from_user.id, text='Выбери кто сможет увидить эту публикацию 👀\n\n*Напоминание* ❗\n1 - Лучшие друзья\n2 - Утки\n3 - Обычные друзья', parse_mode="MARKDOWN", reply_markup=kb.keyboard6)
        bot.register_next_step_handler(msg, select_ppl)

      
def select_ppl(msg):
    db = SQLighter('db.sqlite')
    user_id = msg.from_user.id
    needTrust = 0
    if msg.text == '1':
        needTrust = 1
        whowillsee = '*Лучшие друзья*'
        
    elif msg.text == '2':
        needTrust = 2
        whowillsee = '*Лучшие друзья и утки*'
    
    elif msg.text == '3':
        needTrust = 3
        whowillsee = '*Все твои читатели*'

    else: 
        pass
    
    db.setTrust(user_id, needTrust)
    msgid = db.user_info_tg(user_id)[3]
    bot.forward_message(msg.from_user.id, msg.from_user.id, msgid)
    msg = bot.send_message(msg.from_user.id, text=f'Выше ты видишь своё сообщение\n\nКто увидит это сообщение:\n{whowillsee}\n\nОсталось *подтвердить* отправку',parse_mode="MARKDOWN", reply_markup=kb.keyboard5)
    bot.register_next_step_handler(msg, apply_publication)


def apply_publication(msg):
    db = SQLighter('db.sqlite')
    user_id = msg.from_user.id
    if msg.text == '✔ Отправить':
        user_info = db.user_info_tg(user_id)
        msgid = user_info[3]
        needTrust = user_info[4]
        n=0
        listofReaders = db.readers_for_publication(user_id, needTrust)

        for i in range(len(listofReaders)):
            bot.forward_message(listofReaders[n][1], listofReaders[n][0], msgid)
            n+=1

        bot.send_message(msg.from_user.id, text=f'✅ Публикация отправлена', reply_markup=kb.keyboard1)

    elif msg.text == '❌ Заного':
        msg = bot.send_message(msg.from_user.id, text=f'Создайте публикацию заного 🔄', reply_markup=kb.keyboard5)
        bot.register_next_step_handler(msg, new_publication)
    
    elif msg.text == '⬅ Меню':
        bot.send_message(msg.from_user.id, text=f'❗ Вы возвращены в Меню', reply_markup=kb.keyboard1)
        
    else:
        pass

bot.polling(none_stop = True)

