import shutil
from pathlib import Path
import pyautogui
import time
import psutil
import requests
import json

# Checks if process exists, alt + f4's whatever window is open

countdowinTimeInterval = 5
idleTimeInterval = 5
minecraftProcess = "javaw.exe"
processToDelete = minecraftProcess
secondsLeftToPlay = 10
leetcodeUsername = "user"
url = "https://leetcode.com/graphql/"
query = f"{{matchedUser(username: \"{leetcodeUsername}\") {{ submitStats {{ acSubmissionNum {{ difficulty count submissions }}}}}}}}"
configFile = "config.json"
secondsPerEasy = 60*15
secondsPerMedium = 60*30
secondsPerHard = 60*60

def processExists(processToDelete):
	return processToDelete in (p.name() for p in psutil.process_iter())


# Get leetcode stats
# Start session on website to fetch csrf token
session = requests.Session()
response = session.get(url)
csrfToken = session.cookies.get_dict()["csrftoken"]
headers = {"referer": f"https://leetcode.com/{leetcodeUsername}/", 'content-type': 'application/graphql', 'X-CSRFToken': csrfToken}


response = session.post(url,query,headers=headers)
leetcodeResponse = json.loads(response.text)
leetcodeData = leetcodeResponse["data"]
actualSubmissions = leetcodeData['matchedUser']['submitStats']['acSubmissionNum']
print(actualSubmissions)
solvedTotal = actualSubmissions[0]['count']
solvedEasy = actualSubmissions[1]['count']
solvedMedium = actualSubmissions[2]['count']
solvedHard = actualSubmissions[3]['count']


# compare to previous stats
f = open(configFile)
configData = json.load(f)
secondsLeftToPlay = configData['secondsLeft']
savedNumberOfSolved = configData['solved']
deltaSolvedEasy = deltaSolvedMedium = deltaSolvedHard = 0
if(solvedEasy>savedNumberOfSolved['Easy']):
	deltaSolvedEasy = solvedEasy-savedNumberOfSolved['Easy']
	configData['solved']['Easy'] = solvedEasy
if(solvedMedium>savedNumberOfSolved['Medium']):
	deltaSolvedMedium = solvedMedium-savedNumberOfSolved['Medium']
	configData['solved']['Medium'] = solvedMedium
if(solvedHard>savedNumberOfSolved['Hard']):
	deltaSolvedHard = solvedHard-savedNumberOfSolved['Hard']
	configData['solved']['Hard'] = solvedHard


# calculate new secondsLeftToPlay	
addedSecondsLeftToPlay = (deltaSolvedEasy*secondsPerEasy) + (deltaSolvedMedium*secondsPerMedium) + (deltaSolvedHard*secondsPerHard)
secondsLeftToPlay+=addedSecondsLeftToPlay
print(secondsLeftToPlay/60)
configData['secondsLeft'] = secondsLeftToPlay

# save to JSON
with open(configFile, 'w', encoding='utf-8') as f:
	json.dump(configData,f, ensure_ascii=False, indent=4)



# Monitor Playtime

# Always run program
while True:
	time.sleep(idleTimeInterval)
	if processExists(processToDelete):
		# Count down the time Left To Play
		while(processExists(processToDelete) and secondsLeftToPlay>0):
			time.sleep(1)
			secondsLeftToPlay-=1
			configData['secondsLeft'] = secondsLeftToPlay
			# save to JSON
			with open(configFile, 'w', encoding='utf-8') as f:
				json.dump(configData,f, ensure_ascii=False, indent=4)
			if(secondsLeftToPlay%60==0):
				print(f"Minutes left: {secondsLeftToPlay/60}")
		if(secondsLeftToPlay<=0):
			secondsLeftToPlay = 0
			# Exit the process
			print(f"Deleting process: {processToDelete}")
			# Countdown to deletion
			for i in range(coundtdownTimeInterval):
				print(countdownTimeInterval-i)
				time.sleep(1)
			# Alt + f4 to delete process as this saves the world in Minecraft
			pyautogui.hotkey('alt','f4')