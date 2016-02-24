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

	# determining snakes position
	coords = snake.get('coords')
	head = coords[0]
	neck = coords[1]
	#tail = coords[-1]
	around = [[0,0],[0,0],[0,0]]
			
	# determining the previous move
	if head[0] < neck[0]:
		lastMove = 'west'
	if head[0] > neck[0]:
		lastMove = 'east'
	if head[1] < neck[1]:
		lastMove = 'north'
	if head[1] > neck[1]:
		lastMove = 'south'
		
	# critical situation setup
	if lastMove == 'north':
		around[0] = [head[0]-1,head[1]]
		around[1] = [head[0]+1,head[1]]
		around[2] = [head[0],head[1]-1]
	elif lastMove == 'south':
		around[0] = [head[0]-1,head[1]]
		around[1] = [head[0]+1,head[1]]
		around[2] = [head[0],head[1]+1]
	elif lastMove == 'east':
		around[0] = [head[0],head[1]-1]
		around[1] = [head[0],head[1]+1]
		around[2] = [head[0]+1,head[1]]
	elif lastMove == 'west':
		around[0] = [head[0],head[1]-1]
		around[1] = [head[0],head[1]+1]
		around[2] = [head[0]-1,head[1]]
	
	#critical situation test
	con1 = False
	con2 = False
	con3 = False
	for someSnake in data.get('snakes'):
		if someSnake != snake:
			for coord in someSnake:
				if coord == around[0]:
					con1 = True
				if coord == around[1]:
					con2 = True
				if coord == around[2]:
					con3 = True
	
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
	elif head[0] == 0:
		if lastMove == 'west':
			if head[1] == 0:
				nextMove = 'south'
			else:
				nextMove = 'north'
		if lastMove == 'north' and head[1] == 0:
			nextMove = 'east'
		if lastMove == 'south' and head[1] == height-1:
			nextMove = 'east'
	elif head[0] == width-1:
		if lastMove == 'east':
			if head[1] == height-1:
				nextMove = 'west'
			else: 
				nextMove = 'south'
		if lastMove == 'north' and head[1] == 0:
			nextMove = 'west'
		if lastMove == 'south' and head[1] == height-1:
			nextMove = 'west'
	elif head[1] == 0:
		if lastMove == 'north':
			if head[0] == width-1:
				nextMove = 'west'
			else:
				nextMove = 'east'
		if lastMove == 'east' and head[0]==width-1:
			nextMove = 'south'
		if lastMove == 'west' and head[0] == 0:
			lastMove = 'south'
	elif head[1] == height-1:
		if lastMove == 'south':
			if head[0] == 0:
				nextMove = 'east'
			else:
				nextMove = 'west'
		if lastMove == 'east' and head[0]==width-1:
			nextMove = 'north'
		if lastMove == 'west' and head[0] == 0:
			lastMove = 'north'
	else:
		nextMove = lastMove 
	
	return {
		'move': nextMove,
		'taunt': 'battlesnake-python!'
		}


@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
