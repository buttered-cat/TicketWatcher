import urllib.request
import json
import time
import RPi.GPIO as GPIO

url = 'https://kyfw.12306.cn/otn/leftTicket/queryT?leftTicketDTO.train_date=2016-01-20&leftTicketDTO.from_station=CDW&leftTicketDTO.to_station=SYT&purpose_codes=ADULT'
#url = 'https://kyfw.12306.cn/otn/leftTicket/queryT?leftTicketDTO.train_date=2016-01-24&leftTicketDTO.from_station=SYT&leftTicketDTO.to_station=DUT&purpose_codes=ADULT'

blinkDelay = 0.1
queryDelay = 600
heartBeatDelay = 10
ctrlPin = 11
lightOn = False

GPIO.setmode(GPIO.BOARD)
GPIO.setup(ctrlPin, not lightOn)

while True:
	try:
		with urllib.request.urlopen(url) as rawRes:
			#print(rawRes.read().decode('utf-8'))
			dct = json.loads(rawRes.read().decode('utf-8'))
			#if len(dct['data']) != 0 :
			hasTicket = False
			for i in range(0, len(dct['data'])):
				if(dct['data'][i]['buttonTextInfo'] == '预订'):
					hasTicket = True
					break
			if(hasTicket):
				#print(dct['data'][i]['buttonTextInfo'])
				print('TICKETS!!!')
				GPIO.setup(ctrlPin, lightOn)
				break
			else:
				print('Still no tickets...maybe later :(')
				GPIO.setup(ctrlPin, lightOn)
				time.sleep(blinkDelay)
				GPIO.setup(ctrlPin, not lightOn)
				time.sleep(blinkDelay)
				GPIO.setup(ctrlPin, lightOn)
				time.sleep(blinkDelay)
				GPIO.setup(ctrlPin, not lightOn)

	except URLError as err:
		print('Status Red! Code #', err.code,':',err.reason)

	#time.sleep(queryDelay)

	for heartBeat in range(0, int(queryDelay/heartBeatDelay - 1)):
		time.sleep(heartBeatDelay)
		GPIO.setup(ctrlPin, lightOn)
		time.sleep(blinkDelay)
		GPIO.setup(ctrlPin, not lightOn)

	time.sleep(heartBeatDelay)
