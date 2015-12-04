import urllib.request
import json
import time
import RPi.GPIO as GPIO

url = 'https://kyfw.12306.cn/otn/leftTicket/queryT?leftTicketDTO.train_date=2016-01-24&leftTicketDTO.from_station=CDW&leftTicketDTO.to_station=SYT&purpose_codes=ADULT'
blinkDelay = 0.1
queryDelay = 600
heartBeatDelay = 10

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,True)

while True:
	try:
		with urllib.request.urlopen(url) as rawRes:
			dct = json.loads(rawRes.read().decode('utf-8'))
			if len(dct['data']) != 0 :
				print('TICKETS!!!')
				GPIO.setup(11,False)
			else:
				print('Still no tickets...maybe later :(')
				GPIO.setup(11,False)
				time.sleep(blinkDelay)
				GPIO.setup(11,True)
				time.sleep(blinkDelay)
				GPIO.setup(11,False)
				time.sleep(blinkDelay)
				GPIO.setup(11,True)

	except URLError as err:
		print('Status Red! Code #',err.code,':',err.reason)

	#time.sleep(queryDelay)

	for heartBeat in range(0, int(queryDelay/heartBeatDelay - 1)):
		time.sleep(heartBeatDelay)
		GPIO.setup(11,False)
		time.sleep(blinkDelay)
		GPIO.setup(11,True)

	time.sleep(queryDelay)
