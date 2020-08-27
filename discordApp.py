import os

import discord
from dotenv import load_dotenv
from googlesearch import search
import mysql.connector
from datetime import datetime

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="discord",
  auth_plugin='mysql_native_password'
)



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
mycursor = mydb.cursor()


client = discord.Client()

@client.event
async def on_ready():

    print(
        f'{client.user} is connected to the following guild:\n'
    )



def googleSearch(importantWords):
    result = ""
    count = 0
    sql = "INSERT INTO history (item, searchtime) VALUES (%s, %s)"
    val = (importantWords, datetime.now())
    mycursor.execute(sql, val)
    mydb.commit()
    for j in search(str(importantWords), tld="com", num=5, stop=5): 
        if(count != 0): 
            result = result + '\n' + j 
        else:    
            result = result + j
        count = count + 1
    return result


def recentSearch(importantWords):
    result = ""
    count = 0
    mycursor.execute("SELECT item FROM history where item like "+"'%"+importantWords+"%'"+" order by searchtime DESC")
    myresult = mycursor.fetchall()
    for data in myresult:
        if(count != 0): 
            result = result + '\n' + data[0] 
        else:    
            result = result + data[0]
        count = count + 1   
    return result

      
@client.event
async def on_message(message):
    words = message.content.split()
    if message.author == client.user:
        return
    if message.content == "hi":
        await message.channel.send("hey")
    if words[0].lower() == "!google":
       importantWords = ' '.join(words[1:])
       messageValue = googleSearch(importantWords)
       await message.channel.send(messageValue) 
    if words[0].lower() == "!recent":
       importantWords = ' '.join(words[1:])
       messageValue = recentSearch(importantWords)
       await message.channel.send(messageValue)        



client.run(TOKEN)