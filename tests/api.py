import requests,json

url = 'https://api.vexdb.io/v1'

def getTeam(team):
	if team != None:	
		r = requests.get(url+'/get_teams?team='+team)
		teamRes = r.json()['result'][0]
		return teamRes
	else:
		return None

# type is robot skills, programming skills, combined skills
def getSkills(team,season=None,skillType=None):
	if team != None:
		path = url+'/get_skills?team='+team
		if season: path+='&season='+season
		if skillType: path+='&type='+str(skillType)
		r = requests.get(path)
		skills = r.json()
		return skills
	else:
		return None

def getAwards(team,name=None,season=None):
	if team != None:
		path = url+'/get_awards?team='+team
		if season: path+='&season='+season
		if name: path+='&name='+name
		r = requests.get(path)
		awards = r.json()
		return awards
	else:
		return None

def getRankings(team=None,division=None,rank=None,season=None):
	path = url+'/get_awards?'
	if division: path+='&division='+season
	if team: path+='&team='+team
	if rank: path+='&rank='+name
	r = requests.get(path)
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

def pretty(data):
	print json.dumps(data, indent=4, sort_keys=True)

team = '5327B'
print('TEAM')
print('\n****************\n')
pretty(getTeam(team))
print('\n****************\n')
print('SKILLS')
print('\n****************\n')
pretty(getSkills(team))
print('\n****************\n')
print('AWARDS')
print('\n****************\n')
pretty(getAwards(team))
print('\n****************\n')
print('RANKINGS')
print('\n****************\n')
pretty(getRankings(team))
print('\n****************\n')
print('EVENTS')
print('\n****************\n')
pretty(getEvents(team=team, season="Skyrise"))
print('\n****************\n')
print('MATCHES')
print('\n****************\n')
pretty(getMatches(team=team, season="Skyrise"))