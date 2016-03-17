import bottle
import os


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
    head_url = '%s://%s/static/snake.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#007419',
        'head': head_url
    }


@bottle.post('/start')
def start():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'LETS GET IT ON'
    }


@bottle.post('/move')
def move():
	
	# getting and initializing data values
	data = bottle.request.json
	height = data.get('height')
	width = data.get('width')
	snake = []
	lastMove = ""
	nextMove = ""
	
	# getting own snake
	for tempSnake in data.get('snakes'):
		if tempSnake.get('id') == 'f795c973-42a3-400e-aadd-4f7bc540c24b':
			snake = tempSnake

	# determining our snake attributes
	health = snake.get('health')
	coords = snake.get('coords')
	head = coords[0]
	neck = coords[1]
	#tail = coords[-1]
	around = [[0,0],[0,0],[0,0]]
			
	# determining the previous move
	if head[0] < neck[0]:
		lastMove = "west"
	elif head[0] > neck[0]:
		lastMove = "east"
	elif head[1] < neck[1]:
		lastMove = "north"
	elif head[1] > neck[1]:
		lastMove = "south"
		
	# determining the coords for the three locations around snakes head
	print(head)
	if lastMove == "north":
		around[0] = [head[0]-1,head[1]]
		around[1] = [head[0]+1,head[1]]
		around[2] = [head[0],head[1]-1]
		print(around)
	elif lastMove == "south":
		around[0] = [head[0]-1,head[1]]
		around[1] = [head[0]+1,head[1]]
		around[2] = [head[0],head[1]+1]
		print(around)
	elif lastMove == "east":
		around[0] = [head[0],head[1]-1]
		around[1] = [head[0],head[1]+1]
		around[2] = [head[0]+1,head[1]]
		print(around)
	elif lastMove == "west":
		around[0] = [head[0],head[1]-1]
		around[1] = [head[0],head[1]+1]
		around[2] = [head[0]-1,head[1]]
		print(around)
	
	
	
	#critical situation test setup
	con1 = False
	con2 = False
	con3 = False
	for someSnake in data.get('snakes'):
		for coord in someSnake:
			if coord == around[0]:
				con1 = True
			if coord == around[1]:
				con2 = True
			if coord == around[2]:
				con3 = True
					
	# food test setup
	foodNext1 = False
	foodNext2 = False
	foodNext3 = False
	for coord in data.get('food'):
		if coord == around[0]:
			foodNext1 = True
		if coord == around[1]:
			foodNext2 = True
		if coord == around[2]:
			foodNext3 = True

	# the if statement hell that is cheching all possible conditions
	if (con1 and con2) or (con1 and con3) or (con2 and con3):
		print("	CRITICAL SITUATION HAPPENIN")
		if lastMove == "north":
			if con1 and con2:
				nextMove = "north"
			elif con1 and con3:
				nextMove = "east"
			elif con2 and con3:
				nextMove = "west"
		elif lastMove == "south":
			if con1 and con2:
				nextMove = "south"
			elif con1 and con3:
				nextMove = "east"
			elif con2 and con3:
				nextMove = "west"
		elif lastMove == "east":
			if con1 and con2:
				nextMove = "east"
			elif con1 and con3:
				nextMove = "south"
			elif con2 and con3:
				nextMove = "north"
		elif lastMove == "west":
			if con1 and con2:
				nextMove = "west"
			elif con1 and con3:
				nextMove = "south"
			elif con2 and con3:
				nextMove = "north"
	elif health < 30:
		location = []
		closest = math.sqrt((heigth**2) + (width**2))
		for food in data.get('food'):
			a = abs(head[0] - food[0]) 
			b = abs(head[1] - food[1])
			distance = math.sqrt((a**2) + (b**2))
			if distance < closest:
				closest = distance
				location = food
		if head[0] < location[0] and lastMove != 'west':
			nextMove = "east"
		if head[0] > location[0] and lastMove != 'east':
			nextMove = "west"
		if head[1] < location[1] and lastMove != 'north':
			nextMove = "south"
		if head[1] > location[1] and lastMove != 'south':
			nextMove = "north"
	elif head[0] == 1:
		if lastMove == "west":
			if foodNext3:
				nextMove = "west"
			elif head[1] <= 1:
				nextMove = "south"
			else:
				nextMove = "north"
		if lastMove == "east":
			if head[1] == 1:
				nextMove = "east"
			elif head[1] == 0:
				nextMove = "south"
			else:
				nextMove = "north"
		if lastMove == "north":
			if foodNext3:
				nextMove = "north"
			elif head[1] <= 1:
				nextMove = "east"
			elif foodNext1:
				nextMove = "west"
		if lastMove == "south":
			if head[1] >= height-2:
				nextMove = "east"
			elif foodNext1:
				nextMove = 'west'
	elif head[0] == width-2:
		if lastMove == "east":
			if foodNext3:
				nextMove = "east"
			elif head[1] >= height-2:
				nextMove = "north"
			else: 
				nextMove = "south"
		if lastMove == "west":
			if head[1] == height-2:
				nextMove = "west"
			elif head[1] == height-1:
				nextMove = "north"
			else:
				nextMove = "south"
		if lastMove == "north":
			if head[1] <= 1:
				nextMove = "west"
			elif foodNext2:
				nextMove = "east"
		if lastMove == "south":
			if foodNext3:
				nextMove = "south"
			elif head[1] >= height-2:
				nextMove = "west"
			elif foodNext2:
				nextMove = "east"
	elif head[1] == 1:
		if lastMove == "north":
			if foodNext3:
				nextMove = "north"
			elif head[0] >= width-2:
				nextMove = "west"
			else:
				nextMove = "east"
		if lastMove == "south":
			if head[0] == width-2:
				nextMove = "south"
			elif head[0] == width-1:
				nextMove = "west"
			else:
				nextMove = "east"
		if lastMove == "east":
			if head[0]>=width-2:
				nextMove = "sout"'
			elif foodNext1:
				nextMove = "north"
		if lastMove == "west":
			if head[0] <= 1:
				nextMove = "south"
			elif foodNext1:
				nextMove = "north"
	elif head[1] == height-2:
		if lastMove == "south":
			if foodNext3:
				nextMove = "south"
			elif head[0] <= 1:
				nextMove = "east"
			else:
				nextMove = "west"
		if lastMove == "north":
			if head[0] == 1:
				nextMove = "north"
			elif head[0] == 0:
				nextMove = "east"
			else:
				nextMove = "west"
		if lastMove == "east":
			if head[0] >= width-2:
				nextMove = "north"
			elif foodNext2:
				nextMove = "south"
		if lastMove == "west":
			if head[0] <= 1:
				nextMove = "north"
			elif foodNext2:
				nextMove = "south"
	elif head[0] == 0:
 		if lastMove == "west":
 			if head[1] == 0:
 				nextMove = "south"
 			else:
 				nextMove = "north"
 		else:
			nextMove = "east"
 	elif head[0] == width-1:
 		if lastMove == "east":
 			if head[1] == height-1:
 				nextMove = "north"
 			else: 
 				nextMove = "south"
 		else:
			nextMove = "west"
 	elif head[1] == 0:
 		if lastMove == "north":
 			if head[0] == width-1:
 				nextMove = "west"
 			else:
 				nextMove = "east"
 		else:
			nextMove = "south"
 	elif head[1] == height-1:
 		if lastMove == "south":
 			if head[0] == 0:
 				nextMove = "east"
 			else:
 				nextMove = "west"
 		else:
			nextMove = "north"
	else:
		nextMove = lastMove 
		
	# checking whether there is a snake in the location we want to go
	going = []
	print("next move is:")
	print(nextMove)
	print("the last move is:")
	print(lastMove)
	if nextMove == "north":
		print("north is true!!!")
		going = [head[0], head[1]-1]
	if nextMove == "east":
		print("east is true!!!")
		going = [head[0]+1, head[1]]
	if nextMove == "south":
		print("south is true!!!")
		going = [head[0], head[1]+1]
	if nextMove == "west":
		print("west is true!!!")
		going = [head[0]-1, head[1]]
	a = around[2][0]
	b = around[2][1]
	print("HERE GOES GOING:")
	print(going)
	# checking wether we're about to collide head on with some snake
	con4 = False
	aroundInFront = []
	aroundInFront.append([going[0]-1, going[1]])
	aroundInFront.append([going[0], going[1]-1])
	aroundInFront.append([going[0]+1, going[1]])
	aroundInFront.append([going[0], going[1]+1])
	inFrontCount = 0
	for someSnake in data.get('snakes'):
		for coord in aroundInFront:
			if someSnake.get('coords')[0] == coord:
				inFrontCount += 1
	if inFrontCount > 1:
		con4 = True

	if (going == around[0] and con1) or con4:
		print("omg planned direction has snake in it!!! gotta change now:p")
		if con3 or a == -1 or a == width or b == -1 or b == height:
			if nextMove == 'north' or nextMove == 'south':
				nextMove = 'east'
			elif nextMove == 'west' or nextMove == 'east':
				nextMove = 'south'
		else:
			nextMove = lastMove
	elif (going == around[1] and con2) or con4:
		print("omg planned direction has snake in it!!! gotta change now:p")	
		if con3 or a == -1 or a == width or b == -1 or b == height:
			if nextMove == 'north' or nextMove == 'south':
				nextMove = 'west'
			elif nextMove == 'west' or nextMove == 'east':
				nextMove = 'north'
		else:
			nextMove = lastMove
	elif (going == around[2] and con3) or con4:
		print("omg planned direction has snake in it!!! gotta change now:p")
		#go toward most of board if possible
		if nextMove == 'north' or nextMove == 'south':
			if head[0] <= width/2:
				if not con2:
					nextMove = 'east'
				else:
					nextMove = 'west'
			else:
				if not con1:
					nextMove = 'west'
				else:
					nextMove = 'east'
		if nextMove == 'east' or nextMove == 'west':
			if head[1] <= height/2:
				if not con2:
					nextMove = 'south'
				else: 
					nextMove = 'north'
			else:
				if not con1:
					nextMove = 'north'
				else:
					nextMove = 'south'
					
	# some custom taunts
	turn = data.get('turn')
	say = ''
	if turn % 2 == 0:
		say = "hot hot tamale"
	else:
		say = "hot tamale"
	
	
	return {
		'move': nextMove,
		'taunt': say
		}


@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'FUCK no'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
