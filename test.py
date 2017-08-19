import PyPDF2

def manual(page: int = 0):
	file = open('manual.pdf','rb')
	pdfReader = PyPDF2.PdfFileReader(file)
	pageObj = pdfReader.getPage(page)
	text = pageObj.extractText()
	# this is the definition of shit code but whatever
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



# <G#>, <SG#>, <R#>, <T#>
# print(manual(7))

word = "VEX Robotics"
print("Found instance of "+ word + " in sections: " + ', '.join(findInSection(word)))
# print("Found instance of " + word + " on pages: " + ', '.join([str(i) for i in find(word)]))