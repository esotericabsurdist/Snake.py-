'''
Name :  Yaser Algomia
CWID :  893-80-2173
Email:  mr.yaserig@csu.fullerton.edu

Description:
    a game inspired by the traditional game "Snake" that is found on old Nokia phones, wiht a bouncing balls twist
    this file represent the whole game visuals and logic. README.txt file will have more details about the game.
'''
#===============================================================================
import pygame
import time
import random
#===============================================================================

class Ball:
    # Class to keep track of a ball's location and vector.
    def __init__(self):
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0

#===============================================================================

            #*********** Globals variables and Setup ***********

pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)
darkBlue = (59, 66, 234)
grey = (201, 203, 204)

light_red = (255,0,0)

yellow = (200,200,0)
light_yellow = (255,255,0)

#green = (34,177,76)
light_green = (0,255,0)


# size of the screen.
display_width = 800
display_height  = 600

# size of map.
map_width = 2400
map_height = 3000

lead_x = display_width/2
lead_y = display_height/2

# camera position. should be camera_x = 800 , camera_y = 2400 ..
camera_x = 0
camera_y = 0

# store the snake body in a list.
snakeList = []

# inner boundary dimensions.
INNER_TOP = 200
INNER_LEFT = 200
INNER_RIGHT = 600
INNER_BOTTOM = 400

# get map image.
map_image = pygame.image.load('images/map_test.png')

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Snakes on the plane')

# Clock
clock = pygame.time.Clock()

BALL_SIZE = 25
block_size = 20
FPS = 15


#===============================================================================

                #******** Sprite Images *******

# Snake Sprite Images.
snakeDirection = None
snakeHead = pygame.image.load('images/snake_head.png')
snakeBody1 = pygame.image.load('images/snake_body1.png')
snakeBody2 = pygame.image.load('images/snake_body2.png')
snakeTail = pygame.image.load('images/snake_tail0.png')
samuelJackson = pygame.image.load('images/samuel_head.png')



#===============================================================================

                  #******** Font Sizes *******

large_font = pygame.font.SysFont(None, 68)
medium_font = pygame.font.SysFont(None, 50)
small_font = pygame.font.SysFont(None, 25)


#===============================================================================

#******** Helper Functions *******

#===============================================================================

def make_ball():

    # Function to make a new, random ball.

    ball = Ball()

    ball.x = random.randrange(BALL_SIZE, display_width - BALL_SIZE)
    ball.y = random.randrange(BALL_SIZE, display_height - BALL_SIZE)

    # Speed and direction of balls
    ball.change_x = random.randrange(-3, 4)
    ball.change_y = random.randrange(-3, 4)

    return ball

#===============================================================================


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        message_to_screen("Welcome to Snake & Bouncy balls", darkBlue, -150, "large")
        message_to_screen("Remember to be smart when generating or removing balls", black, -30)
        message_to_screen("Each ball you have in the screen will give you +1 point when you eat an apple", black, 0)
        message_to_screen("The more balls you have, the more points you can get! but it's more difficult", black, 30)
        message_to_screen("If it gets difficult, remove balls to move freely, you have 15 max collisions before you lose", black, 60)
        message_to_screen("to add a ball, press 'a' , to delete a ball press 'd' ", green, 90)
        message_to_screen("For detailed instructions, refer to README.txt file", darkBlue, 140)
        message_to_screen("Press 'C' to play or 'Q' to quit.", red, 180,"medium")

        pygame.display.update()
        clock.tick(15)

#===============================================================================
# snake(snakeList) draws the snake to screen based on the current position
# of each snake segment listed in the snakeList.
def snake(snakeList):
    print 'snakeList: ', snakeList
    global snakeDirection
    global snakeHead
    global lead_x
    global lead_y

    # create a new head sprite to rotate appropriately.
    head = pygame.image.load('images/snake_head.png')

    # change the direction based on the given direction.
    if snakeDirection == 'left':
        print 'going left'
        snakeHead = pygame.transform.rotate(head, 90)
    if snakeDirection == 'right':
        print 'going right'
        snakeHead = pygame.transform.rotate(head, 270)
    if snakeDirection == 'down':
        print 'going down'
        snakeHead = pygame.transform.rotate(head, 180)
    if snakeDirection == 'up':
        print 'going up'
        snakeHead = pygame.transform.rotate(head, 0)

    # draw the rest of the snake's body:
    for i, bodySegmentCoordinate in enumerate(snakeList):
        # positions.
        x = 0
        y = 1

        # draw the tail if it is the last segment. else if it's an odd segment, draw the first type of segment, otherwise draw the second type of segment.
        if i == 0 and (len(snakeList) > 1):
            gameDisplay.blit(snakeTail, (bodySegmentCoordinate[x], bodySegmentCoordinate[y]))
        elif i == len(snakeList)-1:
            gameDisplay.blit(snakeHead, (bodySegmentCoordinate[x], bodySegmentCoordinate[y]))
        elif i%2 == 0:
            gameDisplay.blit(snakeBody1, (bodySegmentCoordinate[x], bodySegmentCoordinate[y]))
        else:
            gameDisplay.blit(snakeBody2, (bodySegmentCoordinate[x], bodySegmentCoordinate[y]))

#===============================================================================

def text_objects(text,color,size):
    if size == "small":
        textSurface = small_font.render(text, True, color)
    elif size == "medium":
        textSurface = medium_font.render(text, True, color)
    elif size == "large":
        textSurface = large_font.render(text, True, color)


    return textSurface, textSurface.get_rect()

#===============================================================================

def message_to_screen(msg,color, y_displace=0, size = "small"):
    textSurf, textRect = text_objects(msg,color, size)
    textRect.center = (display_width / 2), (display_height / 2)+y_displace
    gameDisplay.blit(textSurf, textRect)


#===============================================================================
def bars(snake_life, poison_ability):

    if snake_life > 10:         # there's a problem here, colors don't match up ...
        snake_life_color = green
    elif snake_life > 5:
        snake_life_color = yellow
    else:
        snake_life_color = red

#assuming if u reach a 100, u get poision ability ..
    if poison_ability > 75:
        poison_ability_color = black
    elif poison_ability > 50:
        poison_ability_color = grey
    else:
        poison_ability_color = light_yellow

    pygame.draw.rect(gameDisplay, snake_life_color, (680, 25, snake_life, 25))
    pygame.draw.rect(gameDisplay, poison_ability_color, (20, 25, poison_ability, 25))

    #int(max(min(currentHP / float(maxHP) * health_bar_width, health_bar_width), 0))
#===============================================================================
def pause():

    paused = True
    message_to_screen("Paused",black,-100,size="large")
    message_to_screen("Press C to continue playing or Q to quit",black,25)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        paused = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()


#===============================================================================


                #********** Main Game Loop **********

def gameLoop():
    # control variables.
    gameExit = False
    gameOver = False

    # this is the snakes position in screen space.
    # x,y positions of the head of the snake. lead, refers to head.
    global lead_x #= display_width/2
    global lead_y #= display_height/2
    lead_x = 400
    lead_y = 300

    # the snakes position in map space.
    snake_x = 400#1200
    snake_y = 300#2700 # depends on the size of the map image.

    # the change in the lead positions represent the direction and the number of pixels to move for every frame.
    lead_x_change = 0
    lead_y_change = 0

    #to keep track of snake life and poisin ability, snake_life = colision_
    snake_life = 15
    poison_ability = 0

    # initialize the map variables for scrolling purposes:
    # camera position.
    global camera_x
    global camera_y

    # initialize the snake.
    global snakeList#snakeList = []
    snakeLength = 1
    global snakeDirection # do we need to make this global, or can we declare it in main.

    # initialize environment and etc.
    total_socre = 0
    num_of_balls = 3
    num_of_snake_ball_collision = 0
    ball_list = []
    ball = make_ball()
    ball_list.append(ball)

    #set up random apple locations
    randAppleX = round(random.randrange(0, display_width-block_size))
    randAppleY = round(random.randrange(0, display_height-block_size))

    while not gameExit:
        #====================================
        # Show game over menu when it's game over. Game over occurs when snake loses health or when snake collides with the wall, or snake collides with itself.
        while gameOver == True:
            gameDisplay.fill(white)
            message_to_screen("Game over, Press 'C' to play or 'Q' to quit.", red , y_displace=-50 , size="medium")
            message_to_screen("Total Score: "+str(total_socre),darkBlue ,  y_displace=0 , size="medium")
            message_to_screen("number of snake-ball collision :"+str(num_of_snake_ball_collision), darkBlue ,  y_displace=50 , size="medium")
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()

            camera_x = 0
            camera_y = 0

        #====================================

        # input controls from user (keyboard inputs)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                # snake movement , left, right, up , down
                if event.key == pygame.K_LEFT:
                    snakeDirection = 'left'
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    snakeDirection = 'right'
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    snakeDirection = 'up'
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    snakeDirection = 'down'
                    lead_y_change = block_size
                    lead_x_change = 0

                # 'a' key add a new ball.
                if event.key == pygame.K_a:
                    ball = make_ball()
                    ball_list.append(ball)
                    num_of_balls = num_of_balls + 1
                    #print ("ball added")        #debug
                # 'd' key to delete a ball
                if event.key == pygame.K_d:
                    if(ball_list):
                        ball_list.remove(ball)
                        num_of_balls = num_of_balls - 1
                        #print ("ball removed") #debug
                if event.key == pygame.K_p:
                    pause()
        #====================================

        # draw the moving enemie/balls/SamuelLJacksons
        for ball in ball_list:
            # Move the ball's center
            ball.x += ball.change_x
            ball.y += ball.change_y

            # Bounce the ball if needed
            if ball.y > display_height - BALL_SIZE or ball.y < BALL_SIZE:
                ball.change_y *= -1
            if ball.x > display_width - BALL_SIZE or ball.x < BALL_SIZE:
                ball.change_x *= -1

        #====================================

        #if snake hits screen boundries, game over
        if snake_x >= map_width and lead_x >= 800:
            print 'map_width', map_width
            print 'snake_x', snake_x
            print 'lead_x', lead_x
            gameOver = True
        elif snake_y >= map_height and lead_y >= 600:
            print 'map_width', map_width
            print 'snake_y', snake_y
            print 'lead_y', lead_y
            gameOver = True
        elif lead_x <= 0 or lead_y <= 0:
            gameOver = True

        # if snake_x >= map_width or lead_x < 0 or snake_y >= map_height or lead_y < 0:
        #     gameOver = True

        #====================================

        # print 'camera_x', camera_x
        # print 'snake_x, snake_y', snake_x, snake_y

        # Update the position of the snake based on the changes inputted by arrow keys, and based on the snakes location in the map.
        if snakeDirection == 'left':
            if lead_x == INNER_LEFT: # if snake is at the left boundary, just move the camera, not the snake.
                # update the snake's position in map space.
                snake_x -= block_size
                # update the camera
                if camera_x is not 0:
                    camera_x -= lead_x_change
                else:
                    # update the snake.
                    lead_x += lead_x_change
                    lead_y += lead_y_change
                    # update the
            else: # if the snake is not at the left boundary, scroll just the snake.
                # update the snake in screen space.
                lead_x += lead_x_change
                lead_y += lead_y_change
        elif snakeDirection == 'right':
            # update the snake's position in map space.
            snake_x += block_size

            if lead_x == INNER_RIGHT:
                # update the camera
                if abs(camera_x - display_width) < map_width:
                    # print 'here is the camera position ', camera_x
                    # print 'here is the camera width + display width ', (camera_x + display_width)
                    # print 'lead_x_change', lead_x_change
                    camera_x -= lead_x_change
                else:
                    lead_x += lead_x_change
                    lead_y += lead_y_change
            else:
                # update the snake.
                lead_x += lead_x_change
                lead_y += lead_y_change
        elif snakeDirection == 'up':
            # update the snake's position in map space.
            snake_y -= block_size

            if lead_y == INNER_TOP: # update the camera
                if camera_y is not 0:
                    camera_y -= lead_y_change
                else:
                    lead_x += lead_x_change
                    lead_y += lead_y_change
            else: # update the snake.
                lead_x += lead_x_change
                lead_y += lead_y_change
        elif snakeDirection == 'down':
            # update the snake's position in map space.
            snake_y += block_size

            if lead_y == INNER_BOTTOM: # update the camera
                if abs(camera_y - display_height) < map_height: # if the camera hasn't reached the end of the map, just scroll the map.
                    camera_y -= lead_y_change
                else: #
                    lead_x += lead_x_change
                    lead_y += lead_y_change
            else:
                # update the snake.
                lead_x += lead_x_change
                lead_y += lead_y_change


        pygame.display.update()

        #====================================

        #lead_x += lead_x_change
        #lead_y += lead_y_change

        # draw the background
        #gameDisplay.fill(white)
        gameDisplay.blit(map_image, (camera_x, camera_y))

        # place an apple as a red rectangle randomly in the screen
        AppleThickness = 30
        pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, AppleThickness, AppleThickness])

        # build snake.
        if lead_x == INNER_RIGHT and snakeDirection == 'right':
            # append body behind head.
            snakeList = []
            for i in range(0, snakeLength):
                snakeList.append([(lead_x - i*block_size), lead_y])
            # reverse the list because the for loop above builds it backwards.
            snakeList.reverse()
            # draw snake.
            snake(snakeList)
        elif lead_x == INNER_LEFT and snakeDirection == 'left':
            # append body behind head.
            snakeList = []
            for i in range(0, snakeLength):
                snakeList.append([(lead_x + i*block_size), lead_y])
            # reverse the list because the for loop above builds it backwards.
            snakeList.reverse()
            # draw snake.
            snake(snakeList)
        elif lead_y == INNER_BOTTOM and snakeDirection == 'down':
            # append body behind head.
            snakeList = []
            for i in range(0, snakeLength):
                snakeList.append([lead_x, (lead_y - i*block_size)])
            # reverse the list because the for loop above builds it backwards.
            snakeList.reverse()
            # draw snake.
            snake(snakeList)
        elif lead_y == INNER_TOP and snakeDirection == 'up':
            # append body behind head.
            snakeList = []
            for i in range(0, snakeLength):
                snakeList.append([lead_x, (lead_y + i*block_size)])
            # reverse the list because the for loop above builds it backwards.
            snakeList.reverse()
            # draw snake.
            snake(snakeList)
        else:
            # if we are not at the inner boundary, update the snake body's position.
            snakeSegment = []
            snakeSegment.append(lead_x)
            snakeSegment.append(lead_y)
            snakeList.append(snakeSegment)
            # smooth movment for the snake without leaving blcoks behind,
            if len(snakeList) > snakeLength:
                del snakeList[0]
            # draw the snake
            snake(snakeList)




        #this works, but segments stack up onto the same position as head when snake is at inner boundary.
        # collision detection for snake running into itself
        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True



        # draw balls in the screen, randomly
        for ball in ball_list:
            #pygame.draw.circle(gameDisplay, black, [ball.x, ball.y], BALL_SIZE)
            gameDisplay.blit(samuelJackson, (ball.x, ball.y))
            #print("ball displayed...")  debug




        # keep track of total score
        text = small_font.render("Score: "+str(total_socre), True, black)
        gameDisplay.blit(text, [0,0])

        # keep track of total number of snake-ball collision, max is 15, then game over!
        text = small_font.render("number of snake-ball collision :"+str(num_of_snake_ball_collision), True, black)
        gameDisplay.blit(text, [0,20])

        bars(snake_life,poison_ability)



        # make snake longer when eating an apple, collision detection ,
        if lead_x > randAppleX and lead_x < randAppleX + AppleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + AppleThickness:

            if lead_y > randAppleY and lead_y < randAppleY + AppleThickness:

                randAppleX = round(random.randrange(0, display_width-block_size))
                randAppleY = round(random.randrange(0, display_height-block_size))
                snakeLength += 1

                # logic for calculating the total score based on the balls present in the screen
                if num_of_balls == 0:
                    total_socre = total_socre + 1;
                    #poison_ability can be developed with better algorithm to keep up with the game level
                    poison_ability = poison_ability + 1;
                else:
                    total_socre = total_socre + num_of_balls
                    #for now, we're treating poison_ability as total score
                    poison_ability = poison_ability + num_of_balls;


            elif lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + AppleThickness:

                randAppleX = round(random.randrange(0, display_width-block_size))
                randAppleY = round(random.randrange(0, display_height-block_size))
                snakeLength += 1

                # logic for calculating the total score based on the balls present in the screen
                if num_of_balls == 0:
                    total_socre = total_socre + 1
                    #poison_ability can be developed with better algorithm to keep up with the game level
                    poison_ability = poison_ability + 1;
                else:
                    total_socre = total_socre + num_of_balls
                    #for now, we're treating poison_ability as total score
                    poison_ability = poison_ability + num_of_balls;



        # collision detection for the snake when it touches the bouncing balls, not perfect
        for ball in ball_list:

            if lead_x > ball.x and lead_x < ball.x + BALL_SIZE or lead_x + block_size > ball.x and lead_x + block_size < ball.x + BALL_SIZE:

                if lead_y > ball.y and lead_y < ball.y + BALL_SIZE:
                    #print ("ball touched....") # debug
                    text = medium_font.render("you touched the ball!!", True, red)
                    gameDisplay.blit(text, [300,0])

                    # calculating the num_of_snake_ball_collision, if it reaches to 15, then game over ,
                    num_of_snake_ball_collision = num_of_snake_ball_collision + 1
                    #snake_life as max collision
                    snake_life -= num_of_snake_ball_collision;
                    if num_of_snake_ball_collision == 15:
                        gameOver = True


                elif lead_y + block_size > ball.y and lead_y + block_size < ball.y + BALL_SIZE:
                    #print ("ball touched....") # debug
                    text = medium_font.render("you touched the ball!!", True, red)
                    gameDisplay.blit(text, [300,0])

                    # calculating the num_of_snake_ball_collision, if it reaches to 15, then game over ,
                    num_of_snake_ball_collision = num_of_snake_ball_collision + 1
                    snake_life -= num_of_snake_ball_collision;
                    if num_of_snake_ball_collision == 15:
                        gameOver = True



        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()
#===============================================================================





#===============================================================================
game_intro() # Run the game intro with instructions for game play.
gameLoop()  # Play the game.
#===============================================================================
