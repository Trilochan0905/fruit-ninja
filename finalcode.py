import pygame, sys                                                     #import pygame
import os
import random

player_health = 3                                                      #trace the player health
game_score = 0                                                         #mark the players score
list_of_fruits = ['melon', 'orange', 'pomegranate', 'guava', 'bomb']   #enter the list of fruits used in game

#creating a window in pygame
FPS = 5  
width = 1100
height = 650
#frames per second (number of frames displayed through 1 second)

#we have to call a function that initialize all the pygame modules
pygame.init()                                                          #the first function to call in pygame application                              
pygame.display.set_caption('Fruit-Ninja Game by GTV')                  #set the name for display bar 
display_game_screen = pygame.display.set_mode((1100, 650))             #set the size of the display bar
time_rate = pygame.time.Clock()                                        #class used to control the frame rate

# Define colors
WHITE = (255,255,255)

backdrop = pygame.image.load('bg1.jpg')                                            #set the background image
font = pygame.font.Font(os.path.join(os.getcwd(), 'comic.ttf'), 42)                 #set font
scoring_label = font.render('Score : ' + str(game_score), True, WHITE)              #score display using provided font
white_lives_icon = pygame.image.load('images/white_lives.png')                      #images that shows remaining lives

# function to generate random fruits
def random_fruit_generator(fruit):
    images_of_fruits = "images/" + fruit + ".png"
    #create a dictionary to store data of fruits
    store_data[fruit] = {
        'img': pygame.image.load(images_of_fruits),
        'x' : random.randint(150,850),                       #selecting the random position on x to generate fruits
        'y' : 800,
        'speed_x': random.randint(-10,10),                   #speed in x axis so that it moves diagonally
        'speed_y': random.randint(-80, -60),                 #fruits speed in y-direction (only upward)
        'throw': False,                                      #it checks weather a fruit should be discarded or not
        't': 0,                                 
        'hit': False,
    }

    if random.random() >= 0.75:                  #we are generating a probability that the 75% of fruits 
        store_data[fruit]['throw'] = True        #should be kept and
    else:                                        #25% of the generated fruits should not appear in the screen
        store_data[fruit]['throw'] = False

# Dictionary to store the data of random fruits generator
store_data = {}
for fruit in list_of_fruits:
    random_fruit_generator(fruit)

# create a function and load the red lives images
def display_red_lives(x, y):
    display_game_screen.blit(pygame.image.load("images/red_lives.png"), (x, y))      #we will transfer image using blit

# Generic method to draw fonts on the screen
font_name = pygame.font.match_font('comic.ttf')
def draw_text(display, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    display_game_screen.blit(text_surface, text_rect)

# function to display lives in position
def position_of_lives(display, x, y, lives, image) :
    for i in range(lives) :
        img = pygame.image.load(image)
        img_rect = img.get_rect()       #get the rectangle of the image
        img_rect.x = int(x + 35 * i)    #set the x coordinate to position them
        img_rect.y = y                  #how much size the cross should be
        display.blit(img, img_rect)

# creating a function for displaying game over
def display_game_over():
    display_game_screen.blit(backdrop, (0,0))
    #add score and replay in the game over display
    draw_text(display_game_screen, "FRUIT NINJA!", 90, width / 2, height / 4)
    if not end_game :
        draw_text(display_game_screen,"Score : " + str(game_score), 50, width / 2, height /2)
    draw_text(display_game_screen, "Press a key to play", 64, width / 2, height * 3 / 4)
    pygame.display.flip()
    
    #setting og keyup moment
    waiting = True
    while waiting:
        time_rate.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

# to run the game
start_game = True
end_game = True      
game_in_progress = True   
while game_in_progress :
    if end_game :
        if start_game :
            display_game_over()
            start_game = False
        end_game = False
        player_health = 3
        position_of_lives(display_game_screen, 690, 5, player_health, 'images/red_lives.png')
        game_score = 0

    for event in pygame.event.get():
        # for closing the window
        if event.type == pygame.QUIT:
            game_in_progress = False

    display_game_screen.blit(backdrop, (0, 0))
    display_game_screen.blit(scoring_label, (0, 0))
    position_of_lives(display_game_screen, 980, 5, player_health, 'images/red_lives.png')
# loop for increasing the speed in y for the next loop 
    for key, value in store_data.items():
        if value['throw']:
            value['x'] += value['speed_x']          
            value['y'] += value['speed_y']          
            value['speed_y'] += (1 * value['t'])    
            value['t'] += 1                         

            if value['y'] <= 800:
                display_game_screen.blit(value['img'], (value['x'], value['y']))    #displaying the images at random position and random fruits
            else:
                random_fruit_generator(key)

            current_position = pygame.mouse.get_pos()   #by using the mouse module we will get the position of the curser

#if the cursor position is inside the dimensions in the range where the fruit is generated then 
            if not value['hit'] and current_position[0] > value['x'] and current_position[0] < value['x']+60 \
                    and current_position[1] > value['y'] and current_position[1] < value['y']+60:
                #if we will hit the bomb one live will be removed
                if key == 'bomb':
                    player_health -= 1
                    if player_health == 0:
                        display_red_lives(690, 15)
                    elif player_health == 1 :
                        display_red_lives(725, 15)
                    elif player_health == 2 :
                        display_red_lives(760, 15)
                    #if three lives are over and we hit the bomb again then it will display the game over screen
                    if player_health < 0 :
                        display_game_over()
                        end_game = True
        #if the mouse is on the bomb then the bomb displays the image of the explosion
                    half_fruit_path = "images/explosion.png"
                else:
        #if the mouse position is correct then it will display the cut image of that fruit
                    half_fruit_path = "images/" + "half_" + key + ".png"

                value['img'] = pygame.image.load(half_fruit_path)
        #and it speed will increase as the cut fruit is falling down 
                value['speed_x'] += 10
        #if key is not bomb then the score is increased by 1
                if key != 'bomb' :
                    game_score += 1
                scoring_label = font.render('Score : ' + str(game_score), True, (255, 255, 255))
                value['hit'] = True
        else:
            random_fruit_generator(key)
#next we have to update our display
    pygame.display.update()
#keep the loop running by given FPS
    time_rate.tick(FPS)    
                        
#now close the pygame
pygame.quit()