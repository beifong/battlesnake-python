import bottle
import os


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
    head_url = '%s://%s/static/head.png' % (
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
	"""
	height = data.get('height')
	width = data.get('width')
	snake = []
	lastMove = ""
	
	# getting own snake
	for tempSnake in data.get('snakes'):
		if tempSnake.get('id') == 'f795c973-42a3-400e-aadd-4f7bc540c24b':
			snake = tempSnake

	# determining snakes position
	coords = snake.get('coords')
	head = coords[0]
	neck = coords[1]
	tail = coords[-1]
			
	# determining the previous move
	if head[0] < neck[0]:
		lastMove = 'west'
	if head[0] > neck[0]:
		lastMove = 'east'
	if head[1] < neck[1]:
		lastMove = 'north'
	if head[1] > neck[1]:
		lastMove = 'south'
		
	# critical situation
	"""
	return {
        'move': 'north',
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
