import PyPDF2

def manual(page: int = 0):
	file = open('manual.pdf','rb')
	pdfReader = PyPDF2.PdfFileReader(file)
	pageObj = pdfReader.getPage(page)
	text = pageObj.extractText()
	# this is the definition of shit code but whatever
	# .replace("\t","") \
	# .replace("  ","") \
	return text.replace("\n","") \
		.replace("VEX Robotics Competition In the Zone Œ Game Manual    vexrobotics.com Copyright 2016, VEX Robotics Inc. 2017-08-17","") \
		.replace("vexrobotics.com Copyright 2017, VEX Robotics Inc. 2017-08-17","")

def find(word):
	found = [];
	NUM_OF_PAGES = 36
	for i in range(NUM_OF_PAGES-1):
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


def getRule(section):
	sections = []

	section = section.upper()
	texts = ""
	if section.startswith("G") or section.startswith("<G"):
		for i in range(1,19+1):
			sections.append("<G"+str(i)+">")
		for page in range(12,16+1):
			text = manual(page)
			text = text.replace(text[text.find("A Cone Stacked on a Goal is worth two"):text.find("inadvertently cross the field border during normal game play.")+len("inadvertently cross the field border during normal game play.")],"")
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
		for i in range(1,21+1):
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

def definition(word):
	text = manual(21-1)
	return text

word = "VEX Robotics"
rule = "<r21>"
print(getRule(rule))
# print("Definition of "+word+": " + definition(word))
# print("Found instance of "+ word + " in sections: " + ', '.join(findInSection(word)))
# print("Found instance of " + word + " on pages: " + ', '.join([str(i) for i in find(word)]))