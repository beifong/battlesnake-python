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
	
	# getting data values
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
		lastMove = 'west'
	elif head[0] > neck[0]:
		lastMove = 'east'
	elif head[1] < neck[1]:
		lastMove = 'north'
	elif head[1] > neck[1]:
		lastMove = 'south'
		
	# ous snake surrounding
	print(head)
	if lastMove == 'north':
		around[0] = [head[0]-1,head[1]]
		around[1] = [head[0]+1,head[1]]
		around[2] = [head[0],head[1]-1]
		print(around)
	elif lastMove == 'south':
		around[0] = [head[0]-1,head[1]]
		around[1] = [head[0]+1,head[1]]
		around[2] = [head[0],head[1]+1]
		print(around)
	elif lastMove == 'east':
		around[0] = [head[0],head[1]-1]
		around[1] = [head[0],head[1]+1]
		around[2] = [head[0]+1,head[1]]
		print(around)
	elif lastMove == 'west':
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
			print("FOUND FOOD ONE 1 !!!!!!")
			foodNext1 = True
		if coord == around[1]:
			print("FOUND FOOD TWO 2 !!!!!!")
			foodNext2 = True
		if coord == around[2]:
			print("FOUND FOOD THREE 3 !!!!!!")
			foodNext3 = True
		
	
	# the if statement hell that os cheching all possible conditions
	if (con1 and con2) or (con1 and con3) or (con2 and con3):
		if lastMove == 'north':
			if con1 and con2:
				nextMove = "noth"
			elif con1 and con3:
				nextMove = "east"
			elif con2 and con3:
				nextMove = "west"
		elif lastMove == 'south':
			if con1 and con2:
				nextMove = "south"
			elif con1 and con3:
				nextMove = "east"
			elif con2 and con3:
				nextMove = "west"
		elif lastMove == 'east':
			if con1 and con2:
				nextMove = "east"
			elif con1 and con3:
				nextMove = "south"
			elif con2 and con3:
				nextMove = "north"
		elif lastMove == 'west':
			if con1 and con2:
				nextMove = "west"
			elif con1 and con3:
				nextMove = "south"
			elif con2 and con3:
				nextMove = "north"
	elif head[0] == 1:
		if lastMove == 'west':
			if foodNext3:
				nextMove = 'west'
			elif head[1] <= 1:
				nextMove = 'south'
			else:
				nextMove = 'north'
		if lastMove == 'east':
			if head[1] == 1:
				nextMove = 'east'
			elif head[1] == 0:
				nextMove = 'south'
			else:
				nextMove = 'north'
		if lastMove == 'north':
			if foodNext3:
				nextMove = 'north'
			elif head[1] <= 1:
				nextMove = 'east'
			elif foodNext1:
				nextMove = 'west'
		if lastMove == 'south':
			if head[1] >= height-2:
				nextMove = 'east'
			elif foodNext1:
				nextMove = 'west'
	elif head[0] == width-2:
		if lastMove == 'east':
			if foodNext3:
				nextMove = 'east'
			elif head[1] >= height-2:
				nextMove = 'north'
			else: 
				nextMove = 'south'
		if lastMove == 'west':
			if head[1] == height-2:
				nextMove = 'west'
			elif head[1] == height-1:
				nextMove = 'north'
			else:
				nextMove = 'south'
		if lastMove == 'north':
			if head[1] <= 1:
				nextMove = 'west'
			elif foodNext2:
				nextMove = 'east'
		if lastMove == 'south':
			if foodNext3:
				nextMove = 'south'
			elif head[1] >= height-2:
				nextMove = 'west'
			elif foodNext2:
				nextMove = 'east'
	elif head[1] == 1:
		if lastMove == 'north':
			if foodNext3:
				nextMove = 'north'
			elif head[0] >= width-2:
				nextMove = 'west'
			else:
				nextMove = 'east'
		if lastMove == 'south':
			if head[0] == width-2:
				nextMove = 'south'
			elif head[0] == width-1:
				nextMove = 'west'
			else:
				nextMove = 'east'
		if lastMove == 'east':
			if head[0]>=width-2:
				nextMove = 'south'
			elif foodNext1:
				nextMove = 'north'
		if lastMove == 'west':
			if head[0] <= 1:
				nextMove = 'south'
			elif foodNext1:
				nextMove = 'north'
	elif head[1] == height-2:
		if lastMove == 'south':
			if foodNext3:
				nextMove = 'south'
			elif head[0] <= 1:
				nextMove = 'east'
			else:
				nextMove = 'west'
		if lastMove == 'north':
			if head[0] == 1:
				nextMove = 'north'
			elif head[0] == 0:
				nextMove = 'east'
			else:
				nextMove = 'west'
		if lastMove == 'east':
			if head[0] >= width-2:
				nextMove = 'north'
			elif foodNext2:
				nextMove = 'south'
		if lastMove == 'west':
			if head[0] <= 1:
				nextMove = 'north'
			elif foodNext2:
				nextMove = 'south'
	elif head[0] == 0:
 		if lastMove == 'west':
 			if head[1] == 0:
 				nextMove = 'south'
 			else:
 				nextMove = 'north'
 		else:
			nextMove = 'east'
 	elif head[0] == width-1:
 		if lastMove == 'east':
 			if head[1] == height-1:
 				nextMove = 'north'
 			else: 
 				nextMove = 'south'
 		else:
			nextMove = 'west'
 	elif head[1] == 0:
 		if lastMove == 'north':
 			if head[0] == width-1:
 				nextMove = 'west'
 			else:
 				nextMove = 'east'
 		else:
			nextMove = 'south'
 	elif head[1] == height-1:
 		if lastMove == 'south':
 			if head[0] == 0:
 				nextMove = 'east'
 			else:
 				nextMove = 'west'
 		else:
			nextMove = 'north'
	else:
		nextMove = lastMove 
	
	return {
		'move': nextMove,
		'taunt': 'Y\'all jesus aint real yo'
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
