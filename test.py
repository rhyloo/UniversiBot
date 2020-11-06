import threading

def printit():
  threading.Timer(5.0, printit).start()
  print("Hello, World!")

printit()



agenda = open("notes.org", "r")
content = agenda.readlines()
agenda.close()

#is the file?
def itfile():
    if (content[1] == "* Tasks"):
        pass
    else:
        print("Error no existe ese archivo")
#read the tags
def readtgs():
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


        

#Main
itfile()
print(range(len(content)))
print(len(content))
todo_tasks, done_tasks = readtgs()
print(todo_tasks)
print(done_tasks)


