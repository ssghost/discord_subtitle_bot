import discord
import time
import speech_recognition as sr

with open('./discord_token.txt') as f:
    token = f.readlines()[1]

client = discord.Client()
rec = sr.Recognizer()
time_limit = 5.0

class timer:
    def __init__(self):
        self.time = 0.0
    def start(self):
        self.time = time.time()
    def end(self):
        self.time = time.time() - self.time
    def reset(self):
        if self.time != 0.0:
            self.time = 0.0

timer = timer()

@client.event
async def on_ready():
    print('Bot Logged In As {0.user}.'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        channel = message.channel
        return

    if message.content.startswith('::start'):
        await timer.start()
        await channel.send('Ready For Listening.')

    if message.content.channel.startswith('::end'):
        await timer.reset()
        await channel.send('Listening Finished.')

    while timer.time != 0.0:
        with sr.Microphone() as source:
            audio = rec.listen(source, phrase_time_limit=time_limit)
            timer.end()
            if timer.time == time_limit:
                try:
                    text = rec.recognize_google(audio)
                    channel.send(text)
                except ValueError:
                    channel.send('No One Was Speaking.')
                timer.start()
            else:
                channel.send('Timer Error.') 
                timer.start() 

client.run(token)
