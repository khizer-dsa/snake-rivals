# Importing Libraries
import sys
import pygame
import random
from pygame.locals import *

# Queue Helper Functions
def enQueue(lst, data):
    lst.append(data)
def deQueue(lst):
    if len(lst) == 0:
        return "Queue is empty"
    else:
        deq = lst.pop(0)
        return deq
def is_empty(lst):
    return len(lst) == 0
# ----------------------------------------------------------------------------- #
# Citation
#   Title: Snaky
#   Author: memoiry
#   Date: Mar 20, 2017
#   Code version: 1.0
#   Availability: https://github.com/memoiry/Snaky/blob/master/snaky_ai_v2.py

#   lines 246-304 and 92-173
# ----------------------------------------------------------------------------- #

# Defining Frames/sec
FPS = 15

# Defining  Window Size
# Window width  and Window height must be a multiple of cell size.
WINDOWWIDTH = 800
WINDOWHEIGHT = 700
CELLSIZE = 20

# Defining number of cells across the window width and window height
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

# Defining colours
#             R    G    B     #defining primary colours   
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
BLUE      = (  0,   0, 255)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
YELLOW    = (255, 255,   0)

# Defining Fonts
font = 'Monster of South hollow St.ttf'
font2 = 'freesansbold.ttf'

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

pause = True  # Pause is initialized at True

apple = {'x': 0, 'y': 0}  # apple is initialized at (0,0) coordinates

HEAD = 0  # index of snake's head
HEAD_2 = 0  # index of worm's head

DIRECTION = [UP, DOWN, LEFT, RIGHT]  # list of possible movements
distance = []

for y in range(CELLHEIGHT):
    distance.append([])
    for x in range(CELLWIDTH):
        distance[y].append(8888)
# ----------------------------------------------------------------------------- #
# Worm Helper Functions

# returns True if the coordinates (X) are not visited by the worm
# and the apple is not present there
# and donot lie outside the screen's window

def into_queue(X, queue, visited, worm):
    (x, y) = X
    if (x, y) == (apple['x'], apple['y']):
        return False
    elif x < 0 or x >= CELLWIDTH:
        return False
    elif y < 0 or y >= CELLHEIGHT:
        return False
    elif (x, y) in queue:
        return False
    elif (x, y) in visited:
        return False
    elif is_worm(x, y, worm):
        return False
    else:
        return True

# checks if worm exists at (x,y) coordinates
# returns True if the worm's body exists at (x,y)

def is_worm(x, y, worm):   # to check if there is worm
    for body in worm:
        if body['x'] == x and body['y'] == y:
            return True
    return False

# Implements BFS - navigates a path towards the apple based on the vertex
# added first into the queue

def cal_distance(worm):
    queue = [(apple['x'], apple['y'])]
    visited = []
    for y in range(CELLHEIGHT):
        for x in range(CELLWIDTH):
            distance[y][x] = 9999

    distance[apple['y']][apple['x']] = 0

    while not is_empty(queue):
        head = queue[0]
        visited.append(head)
        up_grid = head[0], head[1] - 1
        down_grid = head[0], head[1] + 1
        left_grid = head[0] - 1, head[1]
        right_grid = head[0] + 1, head[1]

        for grid in [up_grid, down_grid, left_grid, right_grid]:
            if into_queue(grid, queue, visited, worm):
                enQueue(queue, grid)
                if distance[grid[1]][grid[0]] != 99999:
                    distance[grid[1]][grid[0]] = distance[head[1]][head[0]] + 1
        deQueue(queue)

# checks if the worm can move or not to x, y
# returns true if it can move to (x,y)

def can_move(X, worm):  # checks if the worm can move or not to x, y
    (x, y) = X
    if x < 0 or x >= CELLWIDTH:
        return False
    elif y < 0 or y >= CELLHEIGHT:
        return False
    elif is_worm(x, y, worm):
        return False
    elif (x, y) == (worm[HEAD]['x'], worm[HEAD]['y']):
        return False
    else:
        return True

# returns False if random location of food and snakes body is not the same
def test_not_ok(temp, worm):
    for body in worm:
        if temp['x'] == body['x'] and temp['y'] == body['y']:
            return True
    return False


# returns updated location of the snake
# Parameters - now is the current location of the snake (dictionary)
# direc - desired direction
def update_dirc(now, direc):
    loc = {'x': 0, 'y': 0}
    if direc == UP:
        loc = {'x': now['x'], 'y': now['y']-1}
    elif direc == DOWN:
        loc = {'x': now['x'], 'y': now['y']+1}
    elif direc == RIGHT:
        loc = {'x': now['x']+1, 'y': now['y']}
    elif direc == LEFT:
        loc = {'x': now['x']-1, 'y': now['y']}
    return loc
# ----------------------------------------------------------------------------- #

def main():
    global FPSCLOCK, DISPLAYSURF
    # Initializing pygame
    pygame.init()
    # FPS Controller
    FPSCLOCK = pygame.time.Clock()
    # Initialize game window
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Snake Game')

    # Main Menu
    start_menu()

    while True:
        s = runGame()
        if s[0] > s[1]:           # snake score > worm score
            GameOver('You Won')
        elif s[0] < s[1]:         # snake score < worm score
            GameOver('You Lost')
        else:
            GameOver('Draw')

def runGame():
    global running_, apple, DIRECTION

    # Set a random start point. for snake
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    snakePos = [{'x': startx,     'y': starty},  # each dictionary represents coordinates of cell/segment of snake's body
                # Initial length of snake is 3 cells
                {'x': startx - 1, 'y': starty},
                {'x': startx - 2, 'y': starty}]
    direction = RIGHT  # Default direction of snake

    # Set a random start point. for worm
    startx = random.randint(0, CELLWIDTH - 1)
    starty = random.randint(0, CELLHEIGHT - 1)
    wormPos = [{'x': startx,     'y': starty},  # each dictionary represents coordinates of cell/segment of worm's body
               # Initial length of worm is 3 cells
               {'x': startx - 1, 'y': starty},
               {'x': startx - 2, 'y': starty}]
    direction_2 = RIGHT  # Default direction of worm
    running_ = True
    cal_distance(wormPos)

    # Start the apple in a random place.
    apple = getRandomLocation(wormPos)

    while True:  # main game loop
        pre_direction = direction

        for event in pygame.event.get():  # event handling loop
            if event.type == pygame.QUIT:
                terminate()
            # snake's movement handling
            elif event.type == pygame.KEYDOWN:  # to enable keyboard
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != UP:
                    direction = DOWN
                elif event.key == pygame.K_ESCAPE:  # Escaping/Exiting game
                    terminate()
                elif event.key == pygame.K_p:  # Pausing
                    pause = True
                    paused()
                if event.key == pygame.K_u:  # Unpausing
                    pause = False
# ----------------------------------------------------------------------------- #
        # worm's movement handling
        # Dijkstra's Algorithm, where 99999 represents infinity
        # Finding shortest path between  worm's head and apple
        shortest_dis = [99999, 99999, 99999, 99999]  # [UP, RIGHT, DOWN, LEFT]

        # checks if worm can move up
        if can_move((wormPos[HEAD_2]['x'], wormPos[HEAD_2]['y'] - 1), wormPos):
            shortest_dis[0] = distance[wormPos[HEAD_2]['y'] - 1][wormPos[HEAD_2]['x']]

        # checks if worm can move right
        if can_move((wormPos[HEAD_2]['x'] + 1, wormPos[HEAD_2]['y']), wormPos):
            shortest_dis[1] = distance[wormPos[HEAD_2]['y']][wormPos[HEAD_2]['x'] + 1]

        # checks if worm can move down
        if can_move((wormPos[HEAD_2]['x'], wormPos[HEAD_2]['y'] + 1), wormPos):
            shortest_dis[2] = distance[wormPos[HEAD_2]['y'] + 1][wormPos[HEAD_2]['x']]

        # checks if worm can move left
        if can_move((wormPos[HEAD_2]['x'] - 1, wormPos[HEAD_2]['y']), wormPos):
            shortest_dis[3] = distance[wormPos[HEAD_2]['y']][wormPos[HEAD_2]['x'] - 1]
        # Finding minimum distance amongst moving up, right, down, left
        min_dis = min(shortest_dis)

        if shortest_dis[0] < 99999 and distance[wormPos[HEAD_2]['y'] - 1][wormPos[HEAD_2]['x']] == min_dis and direction_2 != DOWN:
            direction_2 = UP

        elif shortest_dis[1] < 99999 and distance[wormPos[HEAD_2]['y']][wormPos[HEAD_2]['x'] + 1] == min_dis and direction_2 != LEFT:
            direction_2 = RIGHT

        elif shortest_dis[2] < 99999 and distance[wormPos[HEAD_2]['y'] + 1][wormPos[HEAD_2]['x']] == min_dis and direction_2 != UP:
            direction_2 = DOWN

        elif shortest_dis[3] < 99999 and distance[wormPos[HEAD_2]['y']][wormPos[HEAD_2]['x'] - 1] == min_dis and direction_2 != RIGHT:
            direction_2 = LEFT

        else:
            # print(direction_2)
            index_ = 0
            for i in range(4):
                temp = update_dirc(wormPos[HEAD_2], DIRECTION[i])
                if can_move(temp, wormPos):
                    index_ = i
                    break
            direction_new = DIRECTION[index_]
            if direction_2 == UP:
                if direction_new != DOWN:
                    direction_2 = direction_new
            elif direction_2 == DOWN:
                if direction_new != UP:
                    direction_2 = direction_new
            elif direction_2 == RIGHT:
                if direction_new != LEFT:
                    direction_2 = direction_new
            elif direction_2 == LEFT:
                if direction_new != RIGHT:
                    direction_2 = direction_new
            # print(direction_2)
# ----------------------------------------------------------------------------- #
        # Game Over Conditions
        # check if the snake or worm has hit itself or the edge
        if snakePos[HEAD]['x'] == -1 or snakePos[HEAD]['x'] == CELLWIDTH or snakePos[HEAD]['y'] == -1 or snakePos[HEAD]['y'] == CELLHEIGHT:
            score = (len(snakePos) - 3, len(wormPos)-3)
            return score  # game over

        # If snake crosses the boundaries, make it enter from the other side

        #if snakePos[HEAD]['x'] == 0: snakePos[HEAD]['x'] == CELLWIDTH -2
        #if snakePos[HEAD]['y'] == 0: snakePos[HEAD]['y'] = CELLHEIGHT -2
        #if snakePos[HEAD]['x'] == CELLWIDTH -1 : snakePos[HEAD]['x'] = 1
        #if snakePos[HEAD]['y'] == CELLHEIGHT -1 : snakePos[HEAD]['y'] = 1

        for snakeBody in snakePos[1:]:
            if (snakeBody['x'] == snakePos[HEAD]['x'] and snakeBody['y'] == snakePos[HEAD]['y']) or (snakeBody['x'] == wormPos[HEAD_2]['x'] and snakeBody['y'] == wormPos[HEAD_2]['y']):
                score = (len(snakePos) - 3, len(wormPos)-3)
                return score  # game over

        if wormPos[HEAD]['x'] == -1 or wormPos[HEAD]['x'] == CELLWIDTH or wormPos[HEAD]['y'] == -1 or wormPos[HEAD]['y'] == CELLHEIGHT:
            score = (len(snakePos) - 3, len(wormPos)-3)
            return score  # game over

        for wormBody in wormPos[1:]:
            if (wormBody['x'] == wormPos[HEAD_2]['x'] and wormBody['y'] == wormPos[HEAD_2]['y']) or (wormBody['x'] == snakePos[HEAD]['x'] and wormBody['y'] == snakePos[HEAD]['y']):
                score = (len(snakePos) - 3, len(wormPos)-3)
                return score  # game over
#---snake movement----#
        # check if snake has eaten an apply
        if snakePos[HEAD]['x'] == apple['x'] and snakePos[HEAD]['y'] == apple['y']:
            # don't remove snake's tail segment
            apple = getRandomLocation(snakePos)  # set a new apple somewhere
        else:
            # remove snake's tail segment to maintain the size of the snake
            del snakePos[-1]

    # tail segment is removed, and a segment is added(in the following line) to the head
    #  in the direction of snake to move the snake forward.

        # move the snake by adding a segment in the direction it is moving
        if not check_direction(direction, pre_direction):
            direction = pre_direction
        if direction == UP:
            newHead = {'x': snakePos[HEAD]['x'], 'y': snakePos[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': snakePos[HEAD]['x'], 'y': snakePos[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': snakePos[HEAD]['x'] - 1, 'y': snakePos[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': snakePos[HEAD]['x'] + 1, 'y': snakePos[HEAD]['y']}
        snakePos.insert(0, newHead)  # adding new head to the next cell
#----worm movement----#
        # check if worm has eaten an apple
        if wormPos[HEAD_2]['x'] == apple['x'] and wormPos[HEAD_2]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation(wormPos)  # set a new apple somewhere
        else:
            del wormPos[-1]  # remove worm's tail segment
        # move the worm by adding a segment in the direction it is moving
        if direction_2 == UP:
            newHead = {'x': wormPos[HEAD_2]['x'],
                       'y': wormPos[HEAD_2]['y'] - 1}
        elif direction_2 == DOWN:
            newHead = {'x': wormPos[HEAD_2]['x'],
                       'y': wormPos[HEAD_2]['y'] + 1}
        elif direction_2 == LEFT:
            newHead = {'x': wormPos[HEAD_2]['x'] -1,
                         'y': wormPos[HEAD_2]['y']}
        elif direction_2 == RIGHT:
            newHead = {'x': wormPos[HEAD_2]['x'] +1,
                         'y': wormPos[HEAD_2]['y']}
        wormPos.insert(0, newHead)          # adding new head to the next cell

        cal_distance(wormPos)

        DISPLAYSURF.fill(BLACK)
        xyGrid()
        drawSnake(snakePos)
        drawWorm(wormPos)
        Food(apple)
        scores(len(snakePos) - 3, len(wormPos)-3)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


# returns False if snake is moving in the opposite direction to the key press
def check_direction(temp, direction):
    if direction == UP:
        if temp == DOWN:
            return False
    elif direction == RIGHT:
        if temp == LEFT:
            return False
    elif direction == LEFT:
        if temp == RIGHT:
            return False
    elif direction == DOWN:
        if temp == UP:
            return False
    return True

def text_format(message, textFont, textSize, textColor):  # text render function
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, True, textColor)

    return newText

img = pygame.image.load('snake4.png')
# picture scaling to the window size.
picture = pygame.transform.scale(img, (WINDOWWIDTH, WINDOWHEIGHT))

# Main Menu
def start_menu():
    game = True
    selected = "start"
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = "start"
                elif event.key == pygame.K_DOWN:
                    selected = "quit"
                if event.key == pygame.K_RETURN:
                    if selected == "start":
                        # print("Start")
                        return
                    if selected == "quit":
                        pygame.quit()
                        quit()
        # Main Menu UI

        DISPLAYSURF.blit(picture, (0, 0))
        pygame.display.flip()
        title = text_format("Snake Rivals", font, 100, GREEN)
        if selected == "start":
            text_start = text_format("Press Enter to START", font, 50, WHITE)
        else:
            text_start = text_format("START", font, 50, GREEN)
        if selected == "quit":
            text_quit = text_format("Press Enter to QUIT", font, 50, WHITE)
        else:
            text_quit = text_format("QUIT", font, 50, GREEN)

        title_rect = title.get_rect()
        title_rect.center = (WINDOWWIDTH/2), (WINDOWHEIGHT/2 - 100)

        start_rect = text_start.get_rect()
        start_rect.center = (WINDOWWIDTH/2), (WINDOWHEIGHT/2)

        quit_rect = text_quit.get_rect()
        quit_rect.center = (WINDOWWIDTH/2), (WINDOWHEIGHT/2 + 70)
        # Main Menu Text
        DISPLAYSURF.blit(title, title_rect)
        DISPLAYSURF.blit(text_start, start_rect)
        DISPLAYSURF.blit(text_quit, quit_rect)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def PressKeyMsg():
    pressKeySurf = text_format('Press a key to play.', font2, 18, WHITE)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

def checkForKeyPress():
    if len(pygame.event.get(pygame.QUIT)) > 0:
        terminate()
    keyUpEvents = pygame.event.get(pygame.KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == pygame.K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

def terminate():
    pygame.quit()
    sys.exit()

def paused():
    pause = True
    TextSurf = text_format("Paused", font, 100, GREEN)
    TextRect = TextSurf.get_rect()
    TextRect.center = ((WINDOWWIDTH/2), (WINDOWHEIGHT/2))
    DISPLAYSURF.blit(TextSurf, TextRect)
    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:  # Unpausing
                    pause = False

        # PressKeyMsg()
        # checkForKeyPress()
        pygame.display.update()
        FPSCLOCK.tick(15)

# returns random loaction of food that is != snake coordinates
def getRandomLocation(worm):
    temp = {'x': random.randint(0, CELLWIDTH - 1),
            'y': random.randint(0, CELLHEIGHT - 1)}
    while test_not_ok(temp, worm):
        temp = {'x': random.randint(0, CELLWIDTH - 1),
                'y': random.randint(0, CELLHEIGHT - 1)}
    return temp

def GameOver(result):
    gameoverSurf = text_format("Game Over", font, 100, GREEN)
    gameoverRect = gameoverSurf.get_rect()
    gameoverRect.center = ((WINDOWWIDTH/2), (WINDOWHEIGHT/2 - 150))
    DISPLAYSURF.blit(gameoverSurf, gameoverRect)

    if result == 'You Won':
        resultSurf = text_format('You Won!', font, 80, WHITE)
    elif result == 'You Lost':
        resultSurf = text_format('You Lost!', font, 80, WHITE)
    elif result == 'Draw':
        resultSurf = text_format('Draw!', font, 80, WHITE)

    resultRect = resultSurf.get_rect()
    resultRect.center = ((WINDOWWIDTH/2), (WINDOWHEIGHT/2))
    DISPLAYSURF.blit(resultSurf, resultRect)
    PressKeyMsg()
    pygame.display.update()
    pygame.time.wait(100)
    checkForKeyPress()  # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            # return
            main()

def scores(score1, score2):
    score1Surf = text_format('Score Snake: %s' % (score1), font2, 18, WHITE)
    score2Surf = text_format('Score Worm: %s' % (score2), font2, 18, WHITE)
    score1Rect = score1Surf.get_rect()
    score2Rect = score2Surf.get_rect()
    score1Rect.topleft = (WINDOWWIDTH - 150, 10)
    score2Rect.topright = (150, 10)
    DISPLAYSURF.blit(score1Surf, score1Rect)
    DISPLAYSURF.blit(score2Surf, score2Rect)

def drawSnake(snakePos):
    for coord in snakePos:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        snakeSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, snakeSegmentRect)
        snakeInnerSegmentRect = pygame.Rect(
            x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, snakeInnerSegmentRect)

def drawWorm(snakePos):
    for coord in snakePos:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, RED, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(
            x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, YELLOW, wormInnerSegmentRect)

def Food(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)

def xyGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))

running_ = True


main()
