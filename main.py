''' ---------- GAME SETTINGS ---------- '''

import pygame as pg
import random, time
import asyncio
pg.init()
clock = pg.time.Clock()

black = (0, 0, 0)


win_width = 800
win_height = 600
screen = pg.display.set_mode((win_width, win_height))
pg.display.set_caption('Pancake Stack')

font = pg.font.Font(None, 30)

speed = 8
score = 0
running = True


player_size = 150
player_pos = [win_width / 2, win_height - player_size]
player_image = pg.image.load('./assets/images/Pancake2.png')
player_image = pg.transform.scale(player_image, (player_size, player_size))

obj_size = 80
obj_data = []
obj = pg.image.load('./assets/images/Pancake1.png')
obj = pg.transform.scale(obj, (obj_size, obj_size))

chilli_size = 60
chilli_data = []
chilli = pg.image.load('./assets/images/chilli2.png')
chilli = pg.transform.scale(chilli, (chilli_size, chilli_size))

maple_size = 60
maple_data = []
maple = pg.image.load('./assets/images/Maple.png')
maple = pg.transform.scale(maple, (maple_size, maple_size))

bg_image = pg.image.load('./assets/images/BACK2.jpg')
bg_image = pg.transform.scale(bg_image, (win_width, win_height))



''' ---------- CREATE_OBJECT FUNCTION ---------- ''' 

def create_object(obj_data):

    if len(obj_data) < 3 and random.random() < 0.1:
        x = random.randint(0, win_width - obj_size)
        y = 0
        obj_data.append([x, y, obj])

def create_chilli(chilli_data):

    if len(chilli_data) < 1 and random.random() < 0.1:
        x = random.randint(0, win_width - chilli_size)
        y = 0
        chilli_data.append([x, y, chilli])
def create_maple(maple_data):
    if len(maple_data) < 1 and random.random() < 0.01:
        x = random.randint(0, win_width - maple_size)
        y = 0
        maple_data.append([x, y, maple])
        
''' ---------- UPDATE_OBJECTS FUNCTION ---------- '''

def update_objects(obj_data):

    global score

    for object in obj_data:
        x, y, image_data = object

        if y< win_height:
            y += (speed + score / 50)
            object[1] = y
            screen.blit(image_data, (x, y))
        else:
            obj_data.remove(object)
            
def update_chillis(chilli_data):

    global score

    for chilli in chilli_data:
        x, y, image_data = chilli

        if y< win_height:
            y += (speed + score / 80)
            chilli[1] = y
            screen.blit(image_data, (x, y))
        else:
            chilli_data.remove(chilli)

def update_maples(maple_data):

    global score

    for maple in maple_data:
        x, y, image_data = maple

        if y< win_height:
            y += (speed + score / 100)
            maple[1] = y
            screen.blit(image_data, (x, y))
        else:
            maple_data.remove(maple)
      
''' ---------- COLLISION_CHECK FUNCTION ---------- '''
def collision_check(obj_data, player_pos):
    global running, score
    for object in obj_data:
        x, y, image_data = object
        player_x, player_y = player_pos[0], player_pos[1]
        obj_rect = pg.Rect(x, y, obj_size, obj_size)
        player_rect = pg.Rect(player_x, player_y, player_size, player_size)
        if player_rect.colliderect(obj_rect):
            score = score + 10
            obj_data.remove(object)

def collision_check_maple(maple_data, player_pos):
    global running, score
    for maple in maple_data:
        x, y, image_data = maple
        player_x, player_y = player_pos[0], player_pos[1]
        maple_rect = pg.Rect(x, y, maple_size, maple_size)
        player_rect = pg.Rect(player_x, player_y, player_size, player_size)
        if player_rect.colliderect(maple_rect):
            score = score + 50
            maple_data.remove(maple)

def collision_check_chilli(chilli_data, player_pos):
    global running
    for chilli in chilli_data:
        x,  y, image_data = chilli
        player_x, player_y = player_pos[0], player_pos[1]
        chilli_rect = pg.Rect(x, y, chilli_size, chilli_size)
        player_rect = pg.Rect(player_x, player_y, player_size, player_size)


        if player_rect.colliderect(chilli_rect):
            time.sleep(2)
            running = False
            break
  
''' ---------- EVENT HANDLERS ---------- '''

async def main():
    global running, player_pos

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            # if event.type == pg.KEYDOWN:
            #     x, y = player_pos[0], player_pos[1]
            #     if event.key == pg.K_LEFT:
            #         x -= 20
            #     elif event.key == pg.K_RIGHT:
            #         x += 20
            #     player_pos = [x, y]
        x, y = player_pos[0], player_pos[1]
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            x -= 20
        if keys[pg.K_RIGHT]:
            x += 20
        player_pos = [x, y]

        screen.blit(bg_image, (0, 0))
        screen.blit(player_image, (player_pos[0], player_pos[1]))

        text = f'Score:{score}'
        text = font.render(text, 10, black)
        screen.blit(text, (win_width - 200, win_height - 40))

        create_object(obj_data)
        update_objects(obj_data)
        collision_check(obj_data, player_pos)

        create_chilli(chilli_data)
        update_chillis(chilli_data)
        collision_check_chilli(chilli_data, player_pos)

        create_maple(maple_data)
        update_maples(maple_data)
        collision_check_maple(maple_data, player_pos)

        clock.tick(30)

        pg.display.flip()

        await asyncio.sleep(0)

asyncio.run(main())