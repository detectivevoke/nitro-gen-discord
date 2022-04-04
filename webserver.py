from flask import Flask
 
from threading import Thread
from http import client
 

import asyncio
import os
import platform
import random
import sys
import json
import discord
import aiohttp
import requests
 
from discord.ext import commands, tasks
from discord.ext.commands import Bot
from discord import Game
from requests.exceptions import RequestException
 
 
app = Flask('')
 
 
 
@app.route('/')
 
def home():
 
    return f"Discord.py API version: {discord.__version__} \nPython version: {platform.python_version()} \nRunning on: {platform.system()} {platform.release()} ({os.name})  Made by Veritify <3"
 
 
 
def run():
 
  app.run(host='0.0.0.0',port=8080)
 
 
 
def keep_alive():  
 
    t = Thread(target=run)
 
    t.start()

