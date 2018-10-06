import os
import sqlite3

# connect to the database file
conn = sqlite3.connect('example.db')

# create a cursor object to implement execute method
c = conn.cursor()


def create_table():
    c.execute(
        'CREATE TABLE IF NOT EXISTS JarvisCommand(keyword TEXT, FileName TEXT, Answer TEXT)')


def data_entry(keyword, behavior, answer):
    c.execute("INSERT INTO JarvisCommand VALUES('%s','%s','%s')" %
              (keyword, behavior, answer))

    # commit and close
    conn.commit()


def read_and_print_all_data():
    c.execute("SELECT * FROM JarvisCommand")
    data = c.fetchall()
    for i in data:
        print(i)


while True:
    input_string = raw_input(
        'keyword, behavior, answer (split using # instead of space / type n to leave):\n')

    # leave
    if input_string == "n":
        print('bye')
        break

    # split the input string
    input_data = input_string.split('#')

    # check if there are only three elements
    if len(input_data) != 3:
        print('please input three element!')
        break

    # insert to database
    data_entry(input_data[0], input_data[1], input_data[2])

    read_and_print_all_data()

c.close()
conn.close()
