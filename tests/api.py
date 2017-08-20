import requests,json

url = 'https://api.vexdb.io/v1'

def getTeam(team=None):
	payload = {
		"team": team
	}
	r = requests.get(url+'/get_teams',params=payload)
	teamRes = r.json()
	return teamRes

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
	return skills

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