import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardButton

##VARIABLES
bot_name = "EII_bot"
bot = telebot.TeleBot("1370488161:AAE4JEvyoz1hVS7KznyU2W-M2UaSpilEOUs")
init_message = f"""Bienvenido a {bot_name}
Este bot ha sido desarrollado por estudiantes
para estudiantes, esperamos que te sea de utilidad.
No dudes en contactar con nostros.
Si necesitas ayuda para empezar escribe /help"""
##FUNCTIONS
# Abre el archivo en modo lectura
agenda = open("agenda.org", "r")
content = agenda.readlines()
agenda.close()

print(content[1])

def save_data(chat_id):
    ids = open('ids.txt', 'a')
    ids.write(str(chat_id)+'\n')
    ids.close()

def send_message(text):
    ids = open('ids.txt', 'r')
    for line in ids:
        bot.send_message(int(line), "Funciona?\n" + text)
    ids.close()
    # markup = types.ReplyKeyboardMarkup(row_width=2)
    # itembtn1 = types.KeyboardButton('a')
    # itembtn2 = types.KeyboardButton('v')
    # itembtn3 = types.KeyboardButton('d')
    # markup.add(itembtn1, itembtn2, itembtn3)
    # chat_id = message.chat.id
    # bot.send_message(chat_id, 'памагити пж')
    # bot.send_message(chat_id, "Choose one letter:", reply_markup=markup)
    # return(chat_id)


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            "Contact with us", url='https://t.me/rhyloo'
        )
    )
    save_data(chat_id)
    bot.send_message(chat_id,init_message , reply_markup = keyboard)
    return(chat_id)
@bot.message_handler(commands=['grados'])
def exchange_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('GIERM', callback_data='get-GIERM'),
        telebot.types.InlineKeyboardButton('GIEN', callback_data='get-GIEN')
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton('GIOI', callback_data='get-GIOI'),
        telebot.types.InlineKeyboardButton('GITI', callback_data='get-GITI')
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton('--', callback_data='get-EUR'),
        telebot.types.InlineKeyboardButton('--', callback_data='get-RUR')
    )
    bot.send_message(message.chat.id, "Selcciona tu grado", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
   data = query.data
   if data.startswith('get-'):
           bot.answer_callback_query(query.id,{"works!"})
           bot.send_chat_action(query.message.chat.id, 'typing')


@bot.message_handler(commands=['secret_command'])
def help_command(message):
    print(message.text)
    mensaje = message.text
    mensaje_splited = mensaje.split()
    mensaje_splited.remove('/secret_command')
    mensaje = " ".join(mensaje_splited)
    send_message(mensaje)

@bot.message_handler(commands=['help'])
def help_command(message):
    print(message.chat.id)
    print(message.message_id)
    bot.send_message(message.chat.id,"Has seleccionado la ayuda")
    bot.forward_message(message.chat.id,message.chat.id,message.message_id)




@bot.message_handler(commands=['prueba_primer_dia_de_clases'])
def saludo_comando(message):
   bot.send_message(message.chat.id,"Grabaré todo? Sí xddd")

@bot.message_handler(commands=['maria'])
def saludo_comando(message):
   bot.send_message(message.chat.id,"Soy Maria,estoy en ingenieria de la Energía <3")

@bot.message_handler(commands=['mama'])
def saludo_comando(message):
   bot.send_message(message.chat.id,"Buenas noches, te quiero <3")

@bot.message_handler(commands=['test'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Hi there, I am Humobot.
What do you want to verify?
""")

@bot.inline_handler(lambda query: query.query == 'hola')
def query_text(inline_query):
    try:
        r = types.InlineQueryResultArticle('1', 'Result', types.InputTextMessageContent('Result message.'))
        r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('Result message2.'))
        bot.answer_inline_query(inline_query.id, [r, r2])
    except Exception as e:
        print(e)

bot.polling(none_stop=True)
