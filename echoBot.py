# -*- coding: UTF-8 -*-
from fbchat import log, Client
import fbchat
from fbchat.models import *
import os
import sqlite3
import subprocess

# connect to the database file
conn = sqlite3.connect('bot.db')
# create a cursor object to implement execute method
c = conn.cursor()

conn1 = sqlite3.connect('example.db')
c1 = conn1.cursor()


def create_table():
    c.execute(
        'CREATE TABLE IF NOT EXISTS EchoBot(date TEXT,time TEXT, thing TEXT)')


def data_entry(date, time, thing):
    c.execute("INSERT INTO EchoBot VALUES('%s','%s','%s')" %
              (date, time, thing))

    # commit and close
    conn.commit()


def read_from_db(command):
    # 因為python使用上
    # 也是透過 execute("...") 在 sqlite 自己的terminal 上輸入指令
    # 所以 "..." 的內容是 SELECT * FROM JarvisCommand WHERE INSTR('turn on the light', keyword)
    # 而 字串代換的過程中 如果沒有在 %s 旁加上 '' 會變成 SELECT * FROM JarvisCommand WHERE INSTR(turn on the light, keyword)
    # 不符合規則！
    c1.execute("SELECT * FROM JarvisCommand WHERE INSTR('%s', keyword)" % command)
    # data is an array
    data = c1.fetchall()
    # print data
    return data


def read_and_print_all_data():
    c.execute("SELECT * FROM EchoBot")
    data = c.fetchall()

    return_text = []

    for i in range(len(data)):
        return_text.append(" ".join(data[i]))

    # print("\n".join(return_text))
    return "\n".join(return_text)


def behavior(text):

    create_table()

    # Schedule
    if text[0] == '#':  # add to schedule
        input_data = text.replace('#', '').split('~')

        # check if there are only three elements
        if len(input_data) != 3:
            return "please input three element! # date ~ time ~ thing"

        # input, 0 : date, 1 : schedule

        # insert to database
        data_entry(input_data[0], input_data[1], input_data[2])

        return "add to schedule"

    elif text == "All" or text == "all":
        return read_and_print_all_data()

    elif len(read_from_db(text)) != 0:

        if read_from_db(text)[0][2] != None:

            if read_from_db(text)[0][1] != ' ':  # command .py
                pid = subprocess.Popen(
                    ["python", "./behavior/"+read_from_db(text)[0][1]])

            return read_from_db(text)[0][2]

    else:
        return "what?"


class CustomClient(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)
        log.info("{} from {} in {}".format(
            message_object, thread_id, thread_type.name))

        # If you're not the author, echo
        if author_id != self.uid:
            # do something
            request = message_object.text

            message_object.text = behavior(request)
            self.send(message_object, thread_id=thread_id,
                      thread_type=thread_type)


# Do something with message_object here


client = CustomClient("arthurtwks@gmail.com", "124511382")
client.listen()
