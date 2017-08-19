import discord
from discord.ext import commands
# import time
from bs4 import BeautifulSoup
import requests
from html.parser import HTMLParser
import math as m
import PyPDF2
# Image Editing
from PIL import Image
from random import randint
import urllib.request
import urllib
# The below three are for replacing requests, didn't work
import aiohttp
vc_clients = {}


# Put at the beginning of command
prefix = '.'
# Description of bot
des = 'The Official 5327B Discord Bot.'
# Make the client
client = commands.Bot(description=des, command_prefix=prefix)


@client.event
async def on_ready():
	print("----------------------")
	print("Logged In As")
	print("Username: %s" % client.user.name)
	print("ID: %s" % client.user.id)
	print("----------------------")


# Nickname Command
@client.command(pass_context=True)
async def nick(ctx, user: discord.Member, nick: str):
	try:
		await client.change_nickname(user, nick)
	except:
		await client.say("Failed.")


# Spam Command
@client.command(pass_context=True)
async def spam(ctx, stuff: str, num: int = 5):
	for i in range(num):
		await client.say(stuff)


# Test Command
@client.command(pass_context=True)
async def test(ctx, num: int = 1):
	for i in range(num):
		await client.say("ping!")


class MLStripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.strict = False
		self.convert_charrefs = True
		self.fed = []

	def handle_data(self, d):
		self.fed.append(d)

	def get_data(self):
		return ''.join(self.fed)


def strip_tags(html):
	s = MLStripper()
	s.feed(html)
	return s.get_data()


# Define Command
@client.command(pass_context=True)
async def define(ctx, word):
	page = requests.get("https://www.merriam-webster.com/dictionary/" + word)
	thing = BeautifulSoup(page.text, 'html.parser')
	definition = thing.find_all('div', attrs={"class": "card-primary-content"})
	await client.say(strip_tags(str(definition[0])))


# Greet Command
@client.event
async def on_member_join(member):
	server = member.server
	fmt = 'Welcome {0.mention} to {1.name}!'
	await client.send_message(server, fmt.format(member, server))


# Look back at when joined command
@client.command()
async def joined(member: discord.Member):
	await client.say('{0.name} joined in {0.joined_at}'.format(member))


# Define Command
@client.command(pass_context=True)
async def random_cat(ctx, num: int = 1):
	# Using async
	for i in range(num):
		async with aiohttp.ClientSession() as cs:
			async with cs.get('http://random.cat/meow') as r:
				res = await r.json()
				await client.say(res['file'])


# Define Command
@client.command(pass_context=True)
async def manual(ctx, page: int = 0):
	text = manual(page)
	await client.say(text)

def manual(page: int = 0):
	# web_file = urllib.request.urlopen("https://content.vexrobotics.com/docs/vrc-inthezone/VRC-InTheZone-GameManual-20170817.pdf")
	# local_file = open('manual.pdf', 'wb')
	# local_file.write(web_file.read())
	file = open('manual.pdf','rb')
	pdfReader = PyPDF2.PdfFileReader(file)
	pageObj = pdfReader.getPage(page)
	text = pageObj.extractText()
	return text.replace("\n","") \
		.replace("VEX Robotics Competition In the Zone Œ Game Manual    vexrobotics.com Copyright 2016, VEX Robotics Inc. 2017-08-17","") \
		.replace("vexrobotics.com Copyright 2017, VEX Robotics Inc. 2017-08-17","")


@client.command(pass_context=True)
async def find(ctx, word):
	if(word is None):
		await client.say("You didn't pass in a word")
	else:
		await client.say("Found instance of "+ word + " in sections: " + ', '.join(findInSection(word)))

def find(word):
	found = [];
	NUM_OF_PAGES = 35
	for i in range(NUM_OF_PAGES):
		if word in manual(i):
			found.append(i)
	return found

def findInSection(word):
	RULE_PAGES = {
		"start": 13,
		"end": 20
	}

	sections = ["<S1>","<S2>"]
	# general
	for i in range(1,18):
		sections.append("<G"+str(i)+">")
	# specific
	for i in range(1,15):
		sections.append("<SG"+str(i)+">")

	texts = ""
	for page in range(RULE_PAGES["start"]-1,RULE_PAGES["end"]-1):
		text = manual(page)
		texts += text

	found = []

	for i in range(len(sections)-1):
		s = None
		if(i < len(sections)-1 -1):
			current = sections[i]
			nxt = sections[i+1]
			s = texts[texts.find(current):texts.find(nxt)-1]
		else:
			sections[i]
			s = texts[texts.find(current):len(texts)-1]
		if word in s:
			found.append(sections[i])

	return found

########################
# Mathemetical Commands#
########################


# Math Check Command
@client.command(pass_context=True)
async def math(ctx, oper: str = "", num1: int = 0, num2: int = 0):
	if oper == "":
		await client.say("Math commands:")
		await client.say("factorial [num] (takes a factorial of a number)")
		await client.say("^ Do not enter a number greater than 1000")
		await client.say("sum [num] [num2] (adds two numbers")
		await client.say("sqrt [num] (finds the square root)")
		await client.say("pow [num] [num2] (raise num to the num2 power)")
	elif oper == "factorial":
		await client.say(m.factorial(num1))
	elif oper == "sqrt":
		await client.say(m.sqrt(num1))
	elif oper == "pow":
		await client.say(m.pow(num1, num2))
	elif oper == "factorial":
		await client.say(m.factorial(num1))
	else:
		await client.say("Invalid operation.")


# Edit Command
@client.command(pass_context=True)
async def img(ctx, url="local.jpg", config=""):
	await client.delete_message(ctx.message)
	try:
		urllib.request.urlretrieve(url, "local.jpg")
		which = "local.jpg"
	except:
		which = url

	img = Image.open(which)
	width, height = img.size
	var1 = randint(-150, 150)
	var2 = randint(-150, 150)
	var3 = randint(-150, 150)

	choice = config
	try:
		if config == "":
			pass
		else:
			for x in range(width):
				for y in range(height):
					pixel_coordinate = (x, y)
					r, g, b = img.getpixel(pixel_coordinate)
					dimness = 50
					var4 = randint(-255, 255)
					var5 = randint(-255, 255)
					var6 = randint(-255, 255)
					choose = {'negative': (255 - r, 255 - g, 255 - b),
							  'hippie': (r, g, 255-b),
							  'dim': (r-dimness, g-dimness, b-dimness),
							  'haze': (r+var4, g+var5, b+var6),
							  'rand_tint': (r+var1, g+var2, b+var3),
							  'green': (r, g+125, b),
							  'red': (r+125, g, b),
							  'blue': (r, g, b+125),
							  'cyan': (r, g+125, b+125),
							  'pink': (r+125, g, b+125)
							  }
					img.putpixel(pixel_coordinate, choose[choice])
		img.save("local.jpg")
		await client.upload('local.jpg')
	except:
		await client.say("Incorrect format.")


client.run("MzQ3OTMyNDQ1NDI3MTA1ODAy.DHkfOA.T26ERyYvLVEmG3bNB-7eW8TJnxA")
