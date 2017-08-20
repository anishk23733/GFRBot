import discord
from discord.ext import commands
from discord import Embed
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
import json
import argparse
import shlex

vc_clients = {}


# Put at the beginning of command
prefix = '.'
# Description of bot
des = 'The Official 5327B Discord Bot.'
# Make the client
client = commands.Bot(description=des, command_prefix=prefix)
url = 'https://api.vexdb.io/v1'

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
	word = word.lower()
	print(word)
	RULE_PAGES = {
		"start": 13,
		"end": 20
	}

	sections = ["<S1>","<S2>"]
	# general
	for i in range(1,18+1):
		sections.append("<G"+str(i)+">")
	# specific
	for i in range(1,15+1):
		sections.append("<SG"+str(i)+">")
	# t
	for i in range(1,5+1):
		sections.append("<T0"+str(i)+">")
	# robot
	for i in range(1,20+1):
		sections.append("<R"+str(i)+">")

	texts = ""
	# normal
	for page in range(13-1,16+1):
		text = manual(page)
		text = text.replace("<SG3>","")\
			.replace(text[text.find("A Cone Stacked on a Goal is worth two"):text.find("the most points receives a ten (10) point bonus.")+len("the most points receives a ten (10) point bonus.")],"")
		texts += text
	# sg
	for page in range(17-1,19+1):
		text = manual(page)
		texts += text
	# t
	for page in range(24,26):
		text = manual(page)
		bs = text[text.find("Small Tournaments (Level 1 Tournaments)"):text.find("12 Alliances of 2 teams")+len("12 Alliances of 2 teams")]
		otherBs = text[text.find("This section provides rules and requirements"):text.find("Please ensure that you are familiar with each of these robot rules before proceeding with robot design.")+len("Please ensure that you are familiar with each of these robot rules before proceeding with robot design.")]
		text = text.replace(bs,"")\
			.replace(text[text.find("The Elimination Matches"):text.find("two wins, and advances.")+len("two wins, and advances.")],"")\
			.replace(otherBs,"")
		texts += text
	# r
	for page in range(28-1, 35):
		text = manual(page)
		texts += text

	texts = texts.lower()
	found = []

	for i in range(len(sections)-1):
		s = None
		current = sections[i].lower()
		if(i < len(sections)-1-1):
			nxt = sections[i+1].lower()
			s = texts[texts.find(current):texts.find(nxt)]
		else:
			s = texts[texts.find(current):len(texts)]

		if(sections[i] == "<SG2>"):
			print(s)
			nxt = sections[i+1]
			print(str(texts.find(current))+":"+str(texts.find(nxt)))
			print(nxt)

		texts = texts.replace(s,"")

		if word in s:
			found.append(sections[i])

	return found


@client.command(pass_context=True)
async def rule(ctx, rule):
	if(rule is None):
		await client.say("You didn't pass in a rule")
	else:
		if not rule.startswith("<"):
			rule = "<" + rule + ">"
		rule = rule.upper()
		embed = Embed(title=rule,type="rich",description=getRule(rule),color=discord.Colour.teal())

		await client.send_message(ctx.message.channel, embed=embed)

def getRule(section):
	sections = []

	section = section.upper()
	texts = ""
	if section.startswith("G") or section.startswith("<G"):
		for i in range(1,19+1):
			sections.append("<G"+str(i)+">")
		for page in range(12,16+1):
			text = manual(page)
			text = text.replace(text[text.find("A Cone Stacked on a Goal is worth two"):text.find("inadvertently cross the field border during normal game play.")+len("inadvertently cross the field border during normal game play.")],"")\
				.replace(text[text.find("<SG1> At the"):text.find("Figure 15 (right): A Legal Preload")+len("Figure 15 (right): A Legal Preload")],"")
			texts += text
	elif section.startswith("S") or section.startswith("<S"):
		sections = ["<S1>","<S2>"]
		for i in range(1,16+1):
			sections.append("<SG"+str(i)+">")
		for page in range(17-1,19+1):
			text = manual(page)
			texts += text
	elif section.startswith("T") or section.startswith("<T"):
		for i in range(1,6+1):
			sections.append("<T0"+str(i)+">")
		for page in range(24,26):
			text = manual(page)
			bs = text[text.find("Small Tournaments (Level 1 Tournaments)"):text.find("12 Alliances of 2 teams")+len("12 Alliances of 2 teams")]
			otherBs = text[text.find("This section provides rules and requirements"):text.find("Please ensure that you are familiar with each of these robot rules before proceeding with robot design.")+len("Please ensure that you are familiar with each of these robot rules before proceeding with robot design.")]
			text = text.replace(bs,"")\
				.replace(text[text.find("The Elimination Matches"):text.find("two wins, and advances.")+len("two wins, and advances.")],"")\
				.replace(otherBs,"")
			texts += text
	elif section.startswith("R") or section.startswith("<R"):
		for i in range(1,22+1):
			sections.append("<R"+str(i)+">")
		for page in range(28-1, 35):
			text = manual(page)
			texts += text

	for i in range(len(sections)-1):
		s = None
		current = sections[i]
		if(i < len(sections)-1-1):
			nxt = sections[i+1]
			s = texts[texts.find(current):texts.find(nxt)]
		else:
			s = texts[texts.find(current):len(texts)]

		if(sections[i] == section):
			return s

		texts = texts.replace(s,"")

	return "Not found"

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
async def img(ctx, loc="local.jpg", config=""):
	await client.delete_message(ctx.message)
	try:
		urllib.request.urlretrieve(loc, "local.jpg")
		which = "local.jpg"
	except:
		which = loc

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


########################
#       VEX API        #
########################
@client.group(pass_context=True)
async def vex(ctx):
	if ctx.invoked_subcommand is None:
		await client.say('Invalid vex command passed...')

@vex.command(pass_context=True)
async def help(ctx):
	text = ("teams [-t team number] (description of team)\n"
	"skills [-t team](get skills) \n"
	"awards [-t team number] (awards team has won)\n"
	"rankings [-t team number] (team rankings)\n"
	"events [-t team number] (team events)\n"
	"matches [-t team number] (team matches)\n")
	embed = Embed(title="VEX API commands",type="rich",description=text,color=discord.Colour.teal())
	await client.send_message(ctx.message.channel, embed=embed)

@vex.command(pass_context=True)
async def teams(ctx, *, message: str=""):
	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--team", help="team name")
	args = parser.parse_args(shlex.split(message))
	text = getTeams(team=args.team)
	par = ""
	for teams in text:
		par += str(teams)+"\n"
		pass
	embed = Embed(title="Team",type="rich",description=par,color=discord.Colour.teal())
	await client.send_message(ctx.message.channel, embed=embed)
	'''text = json.dumps(getTeams(team=args.team))
	for paragraph in discordTextSplit(text):
		embed = Embed(title="Teams",type="rich",description=paragraph,color=discord.Colour.teal())
		await client.send_message(ctx.message.channel, embed=embed)
		await client.say(type(text))'''

@vex.command(pass_context=True)
async def skills(ctx, *, message: str=""):
	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--team", help="team name")
	parser.add_argument("-s", "--season", help="season name")
	parser.add_argument("-ty", "--type", help="type name (0 robot, 1 programming, 2 combined)")

	args = parser.parse_args(shlex.split(message))
	text = getSkills(team=args.team,season=args.season,skillType=args.type)
	par = ""
	for skills in text:
		for i in range(1):
			for values in skills:
				par += (values.title() + ": " +str(skills[values]) +"\n")
		break
	#embed = Embed(title="Skills",type="rich",description=par,color=discord.Colour.teal())
	embed = Embed(title="Skills",type="rich",description=par,color=discord.Colour.teal())
	await client.send_message(ctx.message.channel, embed=embed)
	'''
	args = parser.parse_args(shlex.split(message))
	text = json.dumps(getSkills(team=args.team,season=args.season,skillType=args.type))
	for paragraph in discordTextSplit(text):
		embed = Embed(title="Skills",type="rich",description=paragraph,color=discord.Colour.teal())
		await client.send_message(ctx.message.channel, embed=embed)'''


@vex.command(pass_context=True)
async def rankings(ctx, *, message: str=""):
	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--team", help="team name")
	parser.add_argument("-d", "--division", help="division")
	parser.add_argument("-r", "--rank", help="rank")
	args = parser.parse_args(shlex.split(message))

	text = json.dumps(getRankings(team=args.team,division=args.division,rank=args.rank))
	for paragraph in discordTextSplit(text):
		embed = Embed(title="Rankings",type="rich",description=paragraph,color=discord.Colour.teal())
		await client.send_message(ctx.message.channel, embed=embed)

@vex.command(pass_context=True)
async def matches(ctx, *, message: str=""):
	# division=None,round=None,instance=None,field=None,team=None,scored=None,season=None
	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--team", help="team name")
	parser.add_argument("-d", "--division", help="division")
	parser.add_argument("-r", "--round", help="round")
	parser.add_argument("-f", "--field", help="field")
	parser.add_argument("-sc", "--scored", help="scored")
	parser.add_argument("-s", "--season", help="season")
	args = parser.parse_args(shlex.split(message))

	text = json.dumps(getMatches(team=args.team,division=args.division,round=args.round,field=args.field,scored=args.scored,season=args.season))
	for paragraph in discordTextSplit(text):
		embed = Embed(title="Matches",type="rich",description=paragraph,color=discord.Colour.teal())
		await client.send_message(ctx.message.channel, embed=embed)

@vex.command(pass_context=True)
async def events(ctx, *, message: str=""):
	# team=None,city=None,region=None,country=None,season=None,program="VRC",status="All"
	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--team", help="team name")
	parser.add_argument("-r", "--region", help="region")
	parser.add_argument("-c", "--country", help="country")
	parser.add_argument("-p", "--program", help="VEXU/VRC")
	parser.add_argument("-s", "--season", help="season")
	parser.add_argument("-st", "--status", help="status: All/Past/Future")
	args = parser.parse_args(shlex.split(message))

	text = json.dumps(getEvents(team=args.team,region=args.region,country=args.country,program=args.program,season=args.season,status=args.status))
	for paragraph in discordTextSplit(text):
		embed = Embed(title="Events",type="rich",description=paragraph,color=discord.Colour.teal())
		await client.send_message(ctx.message.channel, embed=embed)

@vex.command(pass_context=True)
async def awards(ctx, *, message: str=""):
	# team=None,name=None,season=None
	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--team", help="team name")
	parser.add_argument("-n", "--name", help="award name")
	parser.add_argument("-s", "--season", help="season name")
	args = parser.parse_args(shlex.split(message))

	text = json.dumps(getAwards(team=args.team,name=args.name,season=args.season))

	for paragraph in discordTextSplit(text):
		embed = Embed(title="Awards",type="rich",description=paragraph,color=discord.Colour.teal())
		await client.send_message(ctx.message.channel, embed=embed)

def discordTextSplit(paragraph):
	x = 2048
	return [paragraph[i: i + x] for i in range(0, len(paragraph), x)]

def getTeams(team=None):
	payload = {
		"team": team
	}
	r = requests.get(url+'/get_teams',params=payload)
	teamRes = r.json()
	values = teamRes["result"]
	values = values[0]
	teamList = []
	for team in values:
		if str(values[team]) != "":
			teamList.append(str(team).replace("_", " ").title()+": "+str(values[team]))
		else:
			teamList.append(str(team).replace("_", " ").title()+": "+"None")
	return teamList

# type is robot skills, programming skills, combined skills
def getSkills(team=None,season=None,skillType=None):
	path = url+'/get_skills'
	payload = {
		"team": team,
		"season": season,
		"type": skillType
	}
	r = requests.get(path,params=payload)
	skills = r.json()
	values = skills["result"]
	return values

def getAwards(team=None,name=None,season=None):
	path = url+'/get_awards'
	payload = {
		"team": team,
		"name": name,
		"season": season
	}
	r = requests.get(path,params=payload)
	awards = r.json()
	return awards

def getRankings(team=None,division=None,rank=None,season=None):
	path = url+'/get_awards'
	payload = {
		"division": division,
		"team": team,
		"rank": rank
	}
	r = requests.get(path,params=payload)
	rankings = r.json()
	return rankings

def getEvents(team=None,city=None,region=None,country=None,season=None,program="VRC",status="All"):
	path = url+'/get_events'
	payload = {
		"city": city,
		"team": team,
		"region": region,
		"country": country,
		"season": season,
		"program": program,
		"status": status
	}
	r = requests.get(path,params=payload)
	rankings = r.json()
	return rankings

def getMatches(division=None,round=None,instance=None,field=None,team=None,scored=None,season=None):
	path = url+'/get_matches'
	payload = {
		"division": division,
		"round": round,
		"instance": instance,
		"field": field,
		"team": team,
		"scored": scored,
		"season": season
	}
	r = requests.get(path,params=payload)
	matches = r.json()
	return matches


client.run("MzQ3OTMyNDQ1NDI3MTA1ODAy.DHkfOA.T26ERyYvLVEmG3bNB-7eW8TJnxA")
