##token import 
from data import token

##To use the easy api of telegram
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardButton

#Get the current time
import time

##"Multitasks"
import threading

#To manage data
import csv

#To delete files
import os

import requests


##VARIABLES
bot_name = "J.A.R.V.I.S"
bot = telebot.TeleBot(token)
init_message =f"""¡Bienvenido extraño!\nEsta es una agenda privada si
crees que te lo mereces ingresa la contraseña y observa las tareas de
Rhyloo."""
name_agenda = 'agenda.csv'

##FUNCTIONS
def read_csv(column):
  data = []
  try:
    agenda_file = open(name_agenda, 'r')
  except:
    print("Something didnt work!")
    #Enviar mensaje fallo telegram
  else:
    with agenda_file:
      csv_reader = csv.reader(agenda_file, delimiter=',')
      for row in csv_reader:
        data.append(row[column])
    agenda_file.close()
    return data

def write_csv (state,day,month,year,hour,mins,message,first_time):
  agenda_file = open(name_agenda,'a',newline='')
  with agenda_file:
    agenda_data = ['state','day', 'month', 'year', 'hour', 'min', 'message']
    agenda_writer = csv.DictWriter(agenda_file, fieldnames=agenda_data)    
    if (first_time == True):
      agenda_writer.writeheader()
    agenda_writer.writerow({'state': state,'day': day, 'month': month,
                              'year': year, 'hour':hour, 'min': mins,'message':message})
  agenda_file.close()

#Distribution filters  
def filtertask(task,task_state):
  filtered_task = task.replace('**','')
  filtered_task = filtered_task.replace(task_state,'')
  filtered_task = filtered_task.strip()
  filtered_task = " ".join(filtered_task.split())
  filtered_task = filtered_task.strip()
  return filtered_task;

def filtertime(time):
  time_splited = time.split(":")
  return time_splited;

def filterdate(date):
  date_splited = date.split("-")
  return date_splited;
    
#distribution
def readorg(content):
  try:
    os.remove("agenda.csv")
  except:
    print("File didn't exist")
  #tasks distribution
  for i in range(len(content)):
    content_splited =  content[i].split()
    if (i == 2):
      first_time = True
    else:
      first_time = False
    #Message todo,done,in progress,etc...
    if (content_splited[0] == "**"):
      if (content_splited[1] == "TODO" or content_splited[1] == "DONE" ):
        task_message = filtertask(content[i],content_splited[1])
        task_state = content_splited[1]
             
    #:label: time date         
    if (content_splited[0] == ":ALARM:" ):
      content_splited[3] = content_splited[3].replace(']','')
      content_splited[1] = content_splited[1].replace('[','')
      #return date year moth and day as array
      date = filterdate(content_splited[1])
      #return hour minute as array
      time = filtertime(content_splited[3])
      write_csv(task_state,date[2],date[1],date[0],time[0],time[1],task_message,first_time)

def filterlocaltime (localtime):
  if (localtime.tm_hour < 10 ):
        localtime_useful_hour = "0"+str(localtime.tm_hour)
  else:
       localtime_useful_hour = str(localtime.tm_hour)

  if (localtime.tm_min < 10 ):
        localtime_useful_min = "0"+str(localtime.tm_min)
  else:
       localtime_useful_min = str(localtime.tm_min)
  return localtime_useful_hour,localtime_useful_min;

#FUNCTIONS FOR THE BOT      
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

def checkit():
  try:
    agenda = open("notes.org", "r")
    content = agenda.readlines()
    agenda.close()
    readorg(content)
  except:
    print("Notes.org doesn't exist please create one!")

def actualization_file():
  url = 'https://raw.githubusercontent.com/rhyloo/agenda_bot/develop/notes.org'
  r = requests.get(url, allow_redirects=True)
  open('notes.org', 'wb').write(r.content)
### Hilo 1
def notifications():
  #Time default 60.0
  threading.Timer(60.0, notifications).start()
  actualization_file()
  checkit()
  print("Revisado...")
  localtime = time.localtime(time.time())
  localtime_useful_hour,localtime_useful_min = filterlocaltime(localtime)

  
  state = read_csv(0)
  day = read_csv(1)
  month = read_csv(2)
  year = read_csv(3)
  hour = read_csv(4)
  minute = read_csv(5)
  message = read_csv(6)

  try:
    for i in range(len(state)):
      if(state[i] == "TODO" and day[i] == str(localtime.tm_mday) and month[i] == str(localtime.tm_mon) and year[i] == str(localtime.tm_year) and hour[i] == localtime_useful_hour and minute[i] == localtime_useful_min):
      send_message(message[i])
  except:
    print("Error! Check!")
    
notifications()

### Hilo 2
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
    
#    return(chat_id)

@bot.message_handler(commands=['menu'])
def tareas(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('Tasks', callback_data='ask_tasks'),
#        telebot.types.InlineKeyboardButton('GIEN', callback_data='get-GIEN')
#    )
#    keyboard.row(
#       telebot.types.InlineKeyboardButton('GIOI', callback_data='get-GIOI'),
#       telebot.types.InlineKeyboardButton('GITI', callback_data='get-GITI')
#    )
#    keyboard.row(
#        telebot.types.InlineKeyboardButton('--', callback_data='get-EUR'),
#        telebot.types.InlineKeyboardButton('--', callback_data='get-RUR')
    )
    bot.send_message(message.chat.id, "MENU",
                     reply_markup=keyboard)

def tasks_ask():
  message = read_csv(6)
  state = read_csv(0)
  block_message = []
  for i in range(len(message)):
    if (state[i] == "TODO"):
      block_message.append(message[i])

  block = '\n'.join(block_message)    
  send_message(block)
   
@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
   data = query.data
   if data.startswith('ask_tasks'):
     bot.answer_callback_query(query.id,{"reading..."})
     tasks_ask()      
           

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
