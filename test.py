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
	for i in range(35):
		if word in manual(i):
			found.append(i)
	return found

print(manual(7))

word = "VEX Robotics"
print("Found instance of " + word + " on pages: " + ', '.join([str(i) for i in find(word)]))