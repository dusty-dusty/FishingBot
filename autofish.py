import threading
from humanize_zucc import *

'''
Testing
meta = {'foo': 'bar', 'nest1': 'nested text'}

opts = {'level': 'info', 'meta': meta}

for i in range(10):
	log.error('Log Line Sample: {}'.format(i), opts)

humanClick("left")
# Cam zoom = -180'''
forceStop = False
paused = True
totalTime = 0
timerLimit = 999999999


def timeInputer():
	global timerLimit
	limit = input('Enter amount of afk 10-15min min!\n1 = 1min: ')

	try:
		limit = int(limit)
		limit *= 60
		log.info('Time till shutdown: {}'.format(limit))
		print('Time till shutdown: {}'.format(limit))
		timerLimit = limit
	except Exception as e:
		appendFile = open('logs/logfile_errors.txt', 'a')
		appendFile.write('ERROR(timeInputer) @{}  Info {}\n'.format(strftime("%c"), e))
		appendFile.close()
		timeInputer()


def runTime():
	global forceStop, totalTime, timerLimit
	timeInputer()
	appendFile = open('logs/logfile_time.txt', 'a')
	appendFile.write('Total Minutes = {}min @{}\n'.format(round((timerLimit / 60)), strftime("%c")))
	appendFile.close()
	start = time()

	while not forceStop:
		totalTime = int(time() - start)

		if totalTime > timerLimit:
			print('Total Minutes = {0}{2}\nTotal Minutes Limit = {1}{2}\n'.format(round((totalTime / 60)),
			                                                                      round((timerLimit / 60)),
			                                                                      strftime("%c")))
			appendFile = open('logs/logfile_time.txt', 'a')
			appendFile.write('Total Minutes Completed = {}min @{}\n'.format(round((totalTime / 60)), strftime("%c")))
			appendFile.close()
			forceStop = True
			if forceStop:
				break
		sleep(1)


def stopAll():
	global forceStop, paused

	while True:

		try:
			if is_pressed('['):
				forceStop = True
				print("Force Stopped!")

				while is_pressed('q'):
					sleep(0.05)
			if is_pressed(']'):
				print("Seconds passed: {}".format(totalTime))
				print("Time left: {}".format(timerLimit - totalTime))
				print("paused")
				paused = True
				sleep(0.1)

				while is_pressed(']'):
					sleep(0.05)
					print("unpaused")
					paused = False
		except Exception as e:
			appendFile = open('logs/logfile_errors.txt', 'a')
			appendFile.write('ERROR(stopAll) @{}  Info {}\n'.format(strftime("%c"), e))
			appendFile.close()
			print("ERROR3 Info {}\n".format(e))
		else:
			sleep(0.05)
			if forceStop:
				break


def logout():
	img = imageLocation(824, 286, 974, 333)
	[x, y] = imageFind("images/loginscreen1.png", img, 824, 286, tolerance=0.8)
	if x > 0:
		humanMove(x, y)
		humanClick("left")
	img2 = imageLocation(669, 321, 813, 361)
	enterPass = imageFind("images/loginscreen2.png", img2, 669, 321, tolerance=0.8, boolValue=True)
	if enterPass:
		value = randint(20, 40)
		for backAmount in range(value):
			humanKeyp("backspace")
		humanType('cool')
		humanKeyp("enter")
	img3 = imageLocation(709, 314, 934, 404)
	[x2, y2, xMax2, yMax2] = imageFind("images/loginscreen3.png", img3, 709, 314, tolerance=0.8, imageShape=1)
	if x2 > 0:
		xMaxMove = randomValue(4, xMax2, -4)
		yMaxMove = randomValue(4, yMax2, -4)
		humanMove((x2 + xMaxMove), (y2 + yMaxMove), 2, 4, -10, 10)
		humanClick("left")
	img4 = imageLocation(738, 290, 900, 349)
	x4, y4 = imageFind("images/loginscreen4.png", img4, 738, 290, tolerance=0.8)
	if x4 > 0:
		humanMove(x4, y4)
		humanClick("left")
		appendFile = open('logs/logfile_data.txt', 'a')
		appendFile.write('Relogged@{}\n'.format(strftime("%c")))
		appendFile.close()


def fishFind():
	blackout = 0
	chance = randint(0, 100)
	if chance > 60:
		blackout = 1
	picList = ["images/f1.png", "images/f2.png", "images/f3.png", "images/f4.png", "images/f5.png", "images/f6.png",
	           "images/f7.png", "images/f8.png", "images/f9.png", "images/f10.png", "images/f11.png", "images/f12.png",
	           "images/f13.png", "images/f14.png", "images/f15.png", "images/f16.png", "images/f17.png",
	           "images/f18.png", "images/f19.png", "images/f20.png", "images/f21.png", "images/f22.png",
	           "images/f23.png", "images/f24.png", "images/f25.png", "images/f26.png"]
	img = imageLocation(250, 85, 1220, 1100)
	if blackout == 1:
		for i in range(len(picList)):
			[x, y, xMax, yMax] = imageFind("{}".format(picList[i]), img, 250, 85, imageShape=1)
			img = np.array(img)

			xCover, yCover = x - 250, y - 85
			xMaxCover, yMaxCover = xCover + xMax, yCover + yMax
			rectangle(img, (xCover, yCover), (xMaxCover, yMaxCover), (0, 0, 0), -1)
			print("Blackouted!")
			break
	for i in range(len(picList)):
		[x, y, xMax, yMax] = imageFind("{}".format(picList[i]), img, 250, 85, imageShape=1)
		if x > 0:
			misschance = randint(0, 100)
			print(picList[i])

			if misschance > 85:
				print(misschance)
				print("missclick fishing")
				xMaxMove = randomValue(-5, xMax, 8)
				yMaxMove = randomValue(-5, yMax, 8)
				humanMove((x + xMaxMove), (y + yMaxMove), 2, 4, -20, 20)
			else:
				xMaxMove = randomValue(4, xMax, -4)
				yMaxMove = randomValue(4, yMax, -4)
				humanMove((x + xMaxMove), (y + yMaxMove), 2, 8, -20, 20)

			humanClick('left')

			if chance < 80:
				humanMove(randint(-820, -212), randint(862, 897), 4, 6, -7, 7)
				humanClick("left")

			appendFile = open('logs/logfile_imagedata.txt', 'a')
			appendFile.write('Image@{}  Info {}\n'.format(strftime("%c"), picList[i]))
			appendFile.close()
			sleep(0.4)
			break


def itemDrop():
	no_find = 0
	holdShift = 0
	img = imageLocation(1424, 736, 1619, 1007)
	chanceClick = randint(0, 100)
	if chanceClick <= 70:
		humanMove(randint(1649, 1874), randint(76, 1022), 1, 4, -7, 7)
		humanClick('left')
	while no_find < 2 and not forceStop and not paused:
		[x, y, xMax, yMax] = imageFind("images/dropicon.png", img, 1424, 736, tolerance=0.6, imageShape=1)
		if x > 0:
			no_find = 0
			chance = randint(0, 100)
			img = np.array(img)

			xCover, yCover = x - 1424, y - 736
			xMaxCover, yMaxCover = xCover + xMax, yCover + yMax
			rectangle(img, (xCover, yCover), (xMaxCover, yMaxCover), (0, 0, 0), -1)
			if chance > 95:
				print(chance)
				print("miss clicking dropping")
				xMaxMove = randomValue(-4, xMax, 4)
				yMaxMove = randomValue(0, yMax, 4)
			else:
				xMaxMove = randomValue(4, xMax, -4)
				yMaxMove = randomValue(4, yMax, -4)
			humanMove((x + xMaxMove), (y + yMaxMove), 2, 3, -7, 7)
			limitSleep = uniform(0.047, 0.2)
			if chanceClick >= 70:
				holdShift += 1
				if holdShift == 2:
					kpress("shift")
					sleep(limitSleep)
			else:
				if holdShift == 0:
					kpress("shift")
					holdShift = 1
					sleep(limitSleep)
			humanClick('left')
		else:
			no_find += 1
			print("sleep")
			sleep(1)
			img = imageLocation(1424, 736, 1619, 1007)
	krelease("shift")


def fill():
	sleep(4)
	checkPrompt = 0
	fDropCheck = 0
	startTimerP = time()
	startTimerF = time()
	startTimeL = time()
	superTime = time()
	promptStop = 5
	forcedropStop = 10
	logoutStop = 60

	if pixelFindColour((129, 86, 47), 1473, 144, 1487, 158, 5):
		x2 = randint(1473, 1487)
		y2 = randint(144, 158)
		humanMove(x2, y2, 1, 4, -7, 7)
		humanClick("left")
	while not forceStop:
		if not paused:
			ransleep = uniform(0, 10)
			checkPrompt += 1
			fDropCheck += 1
			promptTimer = time() - startTimerP
			dropTimer = time() - startTimerF
			logoutTimer = time() - startTimeL

			img = imageLocation(1561, 965, 1617, 1003)
			foundImage = imageFind("images/dropicon.png", img, 1561, 965, boolValue=True)
			if foundImage:  # itemdrop
				beforechance = randint(0, 100)

				if beforechance < 40:
					print("sleep before item drop")
					sleep(ransleep)

				itemDrop()

			if pixelFindColour((255, 0, 0), 36, 48, 601, 66, boolValue=True):  # fishing
				sleepchance = randint(0, 100)
				if sleepchance < 70:
					print("ransleep")
					sleep(ransleep)

				if sleepchance > 95:
					longerSleep = uniform(1, 120)
					print("sleeping longer:{}".format(longerSleep))
					appendFile = open('logs/logfile_data.txt', 'a')
					appendFile.write('LongSleep@{} info:{}\n'.format(strftime("%c"), longerSleep))
					appendFile.close()
				fishFind()
				sleep(1)

			if promptTimer > promptStop:
				startTimerP = time()
				checkPrompt = 0
				img = imageLocation(127, 940, 393, 1008)
				x, y, xMax, yMax = imageFind('images/prompt.png', img, 127, 940, imageShape=1)
				if x > 0:
					xMaxMove = randomValue(6, xMax, -6)
					yMaxMove = randomValue(6, yMax, -6)
					humanMove((x + xMaxMove), (y + yMaxMove), 3, 5, -10, 10)
					humanClick('left')

					humanMove(randint(-820, -212), randint(862, 897), 4, 6, -7, 7)
					humanClick("left")

					appendFile = open('logs/logfile_data.txt', 'a')
					appendFile.write('ClickPrompt@{}\n'.format(strftime("%c")))
					appendFile.close()

			if dropTimer > forcedropStop:
				startTimerF = time()
				forcedrop = randint(0, 99)

				logout()

				if forcedrop == 22:
					beforechance = randint(0, 100)
					if beforechance < 40:
						print("sleep before item drop")
						sleep(ransleep)
					print("Force Drop!")
					appendFile = open('logs/logfile_data.txt', 'a')
					appendFile.write('ForceDrop@{}\n'.format(strftime("%c")))
					appendFile.close()

					itemDrop()
			if logoutTimer > logoutStop:
				startTimeL = time()
				superSleep = time() - superTime

				logChance = randint(-100, 100)
				if superSleep > 18000:
					logChance = randint(30, 100)
				longSleep = randint(900, 1800)
				if logChance == 47:
					superTime = time()
					print("LONG SLEEP {}sec".format(longSleep))
					appendFile = open('logs/logfile_data.txt', 'a')
					appendFile.write('Long Sleep@{} length:{}\n'.format(strftime("%c"), longSleep))
					appendFile.close()
					sleep(longSleep)
	sleep(1)


timeout = threading.Thread(target=runTime)
timeout.start()
stopper = threading.Thread(target=stopAll)
stopper.start()
sfill = threading.Thread(target=fill)
sfill.start()
