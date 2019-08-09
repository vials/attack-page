import requests, time

# These will be utilized for your GET request for monitoring the attacks
# and for your webhook POST request
FTHKey = "Your FTH API Key Here"
webHookLink = "Your Discord Webhook URL Here"

def sendMessage(message):
	r = requests.post(webHookLink, headers={"accept": "application/json"}, data={"content": message})
	print("Notification Sent: "+message)

def monitorAttack():
	attackLog = []
	attackIndex = []
	monitoring = True
	while monitoring:
		try:
			headers = {"accept": "application/json", "Authorization": FTHKey}
			getAttackCount = requests.get("https://api.fulltimehosting.net/firewall_log/unseen", headers=headers)
			if int(getAttackCount.json()['count']) > 0:
				r = requests.get("https://api.fulltimehosting.net/firewall_log", headers=headers)
				for attacks in range(len(r.json())):
					attackLog.append(r.json()[attacks])
				sendMessage("Attack on: ["+attackLog[-1:][0]['ip']+"] Started At: ["+attackLog[-1:][0]['start']+"]")
				attackIndex.append(int(len(attackLog)))

			for i in attackIndex:
				r = requests.get("https://api.fulltimehosting.net/firewall_log", headers=headers)
				if r.json()[i-1]['end'] != None:
					sendMessage("Attack on: ["+attackLog[-1:][0]['ip']+"] Ended At: ["+attackLog[-1:][0]['start']+"] With: ["+str(attackLog[-1:][0]['mbps'])+"] MBPS And ["+str(attackLog[-1:][0]['pps'])+"] PPS")
					attackIndex.remove(i)
				else:
					''' Do Nothing'''
				time.sleep(int(monitorEOACooldown)) #Cooldown for checking end of attack
		except Exception as e:
			print(str(e))
			pass
		time.sleep(int(monitorCooldown)) #Cooldown for monitoring attacks

if __name__ == "__main__":
	'''Set the cooldown to avoid hitting the rate limit.
	Just make sure that you are setting it to proper time lengths.
	Integers only!'''
	monitorCooldown = input("Enter Cooldown For Monitoring Attacks: ")
	monitorEOACooldown = input("Enter Cooldown For Monitoring End Of Attack: ")
	print("Monitoring Attack Logs\n"+"*"*32)
	monitorAttack()
