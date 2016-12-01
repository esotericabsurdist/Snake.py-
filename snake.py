'''
Name :  Yaser Algomia
CWID :  893-80-2173
Email:  mr.yaserig@csu.fullerton.edu

Description:
    a game inspired by the traditional game "Snake" that is found on old Nokia phones, wiht a bouncing balls twist
    this file represent the whole game visuals and logic. README.txt file will have more details about the game.
'''

import pygame
import time
import random


class Ball:

    # Class to keep track of a ball's location and vector.

    def __init__(self):
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0


pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)
darkBlue = (59, 66, 234)

display_width = 800
display_height  = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Snake And Bouncy balls')

img = pygame.image.load('images/snake_head_400x400.png')


clock = pygame.time.Clock()

BALL_SIZE = 25
block_size = 20
FPS = 15



large_font = pygame.font.SysFont(None, 68)
medium_font = pygame.font.SysFont(None, 50)
small_font = pygame.font.SysFont(None, 25)


def make_ball():

    # Function to make a new, random ball.

    ball = Ball()

    ball.x = random.randrange(BALL_SIZE, display_width - BALL_SIZE)
    ball.y = random.randrange(BALL_SIZE, display_height - BALL_SIZE)

    # Speed and direction of balls
    ball.change_x = random.randrange(-3, 4)
    ball.change_y = random.randrange(-3, 4)

    return ball

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
        message_to_screen("Welcome to Snake & Bouncy balls",
                          darkBlue,
                          -150,
                          "large")
        message_to_screen("Remember to be smart when generating or removing balls",
                          black,
                          -30)

        message_to_screen("Each ball you have in the screen will give you +1 point when you eat an apple",
                          black,
                          0)
        message_to_screen("The more balls you have, the more points you can get! but it's more difficult",
                          black,
                          30)

        message_to_screen("If it gets difficult, remove balls to move freely, you have 15 max collisions before you lose",
                          black,
                          60)

        message_to_screen("to add a ball, press 'a' , to delete a ball press 'd' ",
                          green,
                          90)

        message_to_screen("For detailed instructions, refer to README.txt file",
                          darkBlue,
                          140)

        message_to_screen("Press 'C' to play or 'Q' to quit.",
                          red,
                          180,"medium")

        pygame.display.update()
        clock.tick(15)

def snake(block_size, snakelist):

    gameDisplay.blit(img, (snakelist[-1][0], snakelist[-1][1]))
    for XnY in snakelist[:-1]:
        pygame.draw.rect(gameDisplay, green, [XnY[0],XnY[1],block_size,block_size])


def text_objects(text,color,size):
    if size == "small":
        textSurface = small_font.render(text, True, color)
    elif size == "medium":
        textSurface = medium_font.render(text, True, color)
    elif size == "large":
        textSurface = large_font.render(text, True, color)


    return textSurface, textSurface.get_rect()


def message_to_screen(msg,color, y_displace=0, size = "small"):
    textSurf, textRect = text_objects(msg,color, size)
    textRect.center = (display_width / 2), (display_height / 2)+y_displace
    gameDisplay.blit(textSurf, textRect)


def gameLoop():
    gameExit = False
    gameOver = False

    lead_x = display_width/2
    lead_y = display_height/2

    lead_x_change = 0
    lead_y_change = 0

    snakeList = []
    snakeLength = 1

    total_socre = 0
    num_of_balls = 1

    num_of_snake_ball_collision = 0

    ball_list = []
    ball = make_ball()
    ball_list.append(ball)

    #s et up random apple locations
    randAppleX = round(random.randrange(0, display_width-block_size))
    randAppleY = round(random.randrange(0, display_height-block_size))

    while not gameExit:

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


        # input controls from user (keyboard inputs)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                # snake movement , left, right, up , down
                if event.key == pygame.K_LEFT:
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
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

        for ball in ball_list:
            # Move the ball's center
            ball.x += ball.change_x
            ball.y += ball.change_y

            # Bounce the ball if needed
            if ball.y > display_height - BALL_SIZE or ball.y < BALL_SIZE:
                ball.change_y *= -1
            if ball.x > display_width - BALL_SIZE or ball.x < BALL_SIZE:
                ball.change_x *= -1




        # if snake hit screen boundries, game over
        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameOver = True


        lead_x += lead_x_change
        lead_y += lead_y_change

        gameDisplay.fill(white)

        # place an apple as a red rectangle randomly in the screen
        AppleThickness = 30
        pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, AppleThickness, AppleThickness])


        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        # smooth movment for the snake without leaving blcoks behind,
        if len(snakeList) > snakeLength:
            del snakeList[0]


        #function to make the snake
        snake(block_size, snakeList)

        # draw balls in the screen, randomly
        for ball in ball_list:
            pygame.draw.circle(gameDisplay, black, [ball.x, ball.y], BALL_SIZE)
            #print("ball displayed...")  debug




        # keep track of total score
        text = small_font.render("Score: "+str(total_socre), True, black)
        gameDisplay.blit(text, [0,0])

        # keep track of total number of snake-ball collision, max is 15, then game over!
        text = small_font.render("number of snake-ball collision :"+str(num_of_snake_ball_collision), True, black)
        gameDisplay.blit(text, [0,20])



        # make snake longer when eating an apple, collision detection ,
        if lead_x > randAppleX and lead_x < randAppleX + AppleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + AppleThickness:

            if lead_y > randAppleY and lead_y < randAppleY + AppleThickness:

                randAppleX = round(random.randrange(0, display_width-block_size))
                randAppleY = round(random.randrange(0, display_height-block_size))
                snakeLength += 1

                # logic for calculating the total score based on the balls present in the screen
                if num_of_balls == 0:
                    total_socre = total_socre + 1;
                else:
                    total_socre = total_socre + num_of_balls

            elif lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + AppleThickness:

                randAppleX = round(random.randrange(0, display_width-block_size))
                randAppleY = round(random.randrange(0, display_height-block_size))
                snakeLength += 1

                # logic for calculating the total score based on the balls present in the screen
                if num_of_balls == 0:
                    total_socre = total_socre + 1
                else:
                    total_socre = total_socre + num_of_balls



        # collision detection for the snake when it touches the bouncing balls, not perfect

        for ball in ball_list:

            if lead_x > ball.x and lead_x < ball.x + BALL_SIZE or lead_x + block_size > ball.x and lead_x + block_size < ball.x + BALL_SIZE:

                if lead_y > ball.y and lead_y < ball.y + BALL_SIZE:
                    #print ("ball touched....") # debug
                    text = medium_font.render("you touched the ball!!", True, red)
                    gameDisplay.blit(text, [300,0])

                    # calculating the num_of_snake_ball_collision, if it reaches to 15, then game over ,
                    num_of_snake_ball_collision = num_of_snake_ball_collision + 1
                    if num_of_snake_ball_collision == 15:
                        gameOver = True


                elif lead_y + block_size > ball.y and lead_y + block_size < ball.y + BALL_SIZE:
                    #print ("ball touched....") # debug
                    text = medium_font.render("you touched the ball!!", True, red)
                    gameDisplay.blit(text, [300,0])

                    # calculating the num_of_snake_ball_collision, if it reaches to 15, then game over ,
                    num_of_snake_ball_collision = num_of_snake_ball_collision + 1
                    if num_of_snake_ball_collision == 15:
                        gameOver = True



        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()

game_intro()
gameLoop()
