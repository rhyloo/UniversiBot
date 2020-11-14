##token import 
from data import token

##To use the easy api of telegram
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardButton

#Get the current time
import time

##"Multitasks"
import threading


##VARIABLES
bot_name = "J.A.R.V.I.S"
bot = telebot.TeleBot(token)
init_message = f"""¡Bienvenido extraño!\nEsta es una agenda privada si
crees que te lo mereces ingresa la contraseña y observa las tareas de Rhyloo."""

##FUNCTIONS
### Hilo 1
def checkit():
  #Time default 60.0
  threading.Timer(60.0, checkit).start()
  print("Revisado...")
  localtime = time.localtime(time.time())

  if (localtime.tm_hour < 10 ):
        localtime_useful_hour = "0"+str(localtime.tm_hour)
  else:
       localtime_useful_hour = str(localtime.tm_hour)

  if (localtime.tm_min < 10 ):
        localtime_useful_min = "0"+str(localtime.tm_min)
  else:
       localtime_useful_min = str(localtime.tm_min)

  localtime_useful = localtime_useful_hour + ":" + localtime_useful_min

  agenda = open("notes.org", "r")
  content = agenda.readlines()
  agenda.close()

  for i in range(len(content)):
      content_splited =  content[i].split()
#      print("El número es:",i)
 #     print("El contenido de content_splited[0] es:", content_splited)
      if (content_splited[0] == ":ALARM:" ):
          content_splited[3] = content_splited[3].replace(']','')
  #        print("El contenido de content_splited[3] es:",content_splited[3])
          if (content_splited[3] == localtime_useful):
            send_message(content[i-1])
checkit()
### Hilo 2

def send_message(text):
    ids = open('ids.txt', 'r')
    for line in ids:
        bot.send_message(int(line),text)
    ids.close()
    
def save_data(chat_id):
    text = str(chat_id)+'\n'
    write = 0
    ids = open('ids.txt', 'r')
    for line in ids:
      if (line == text):
        write = write + 1
    ids.close()
    if (write == 0):
      ids = open('ids.txt', 'a')
      ids.write(str(chat_id)+'\n')
      ids.close()

#read the tags
def readtgs(content):
    #tags here
    todo_tasks = []
    done_tasks = []
    
    #tasks separation
    for i in range(len(content)):
       content_splited =  content[i].split()
       if (content_splited[0] == "**"):
           if (content_splited[1] == "TODO"):
               todo_tasks.append(i)               
           elif (content_splited[1] == "DONE"):
               done_tasks.append(i)
    return todo_tasks, done_tasks;           

#saving tasks to print
def print_todo (todo_tasks,content):
    task_message = ""
    for i in todo_tasks:
        task_message = task_message + content[i] 
    return task_message

def print_done (done_tasks,content):
    done_message = ""
    for i in done_tasks:
        task_message = task_message + content[i] 
    return task_message



#Solución temporal repetir códigon no es bueno
def main_todo():
    agenda = open("notes.org", "r")
    content = agenda.readlines()
    agenda.close()
    itfile(content)
    todo_tasks, done_tasks = readtgs(content)
    task_message = print_todo(todo_tasks,content)
    return task_message

def main_done():
    agenda = open("notes.org", "r")
    content = agenda.readlines()
    agenda.close()
    itfile(content)
    todo_tasks, done_tasks = readtgs(content)
    task_message = print_todo(done_tasks,content)
    return task_message


#Bots commands
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    #Make a box with the message/link contact with us
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            "Contact with me", url='https://t.me/rhyloo'
        )
    )
    #Save the chat_id (Idk if its necessary)
    save_data(chat_id)
    #Send init message befor box "contact me"
    bot.send_message(chat_id,init_message , reply_markup = keyboard)
    return(chat_id)

@bot.message_handler(commands=['tareas'])
def tareas(message):
   task_message = main_todo()
   bot.send_message(message.chat.id, task_message)

@bot.message_handler(commands=['tareas_hechas'])
def tareas(message):
   task_message = main_done()
   bot.send_message(message.chat.id, task_message)

@bot.message_handler(commands=['tareas_hechas'])
def tareas(message):
   task_message = main_done()
   bot.send_message(message.chat.id, task_message)

#@bot.message_handler(commands=['mama'])
def alarm_message(message):
   bot.send_message(message.chat.id,"FUNCIONA!")
   
bot.polling(none_stop=True)
