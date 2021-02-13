import pygame as pg
import json

size = (500,500)
pg.init()
screen = pg.display.set_mode(size)
switch = True

image = pg.image.load("sample2.jpg")
image = pg.transform.scale(image,(500,500))
screen.blit(image,(0,0))

new_coords = []

while switch:
    for event in pg.event.get():
        coord = (0,0)
        if pg.mouse.get_pressed()[0] :
            coord = pg.mouse.get_pos()
            new_coords.append(coord)
            pg.draw.circle(screen,(255,255,255),coord,1)
        elif event.type == pg.KEYDOWN and pg.key.get_pressed()[pg.K_x]:
            if len(new_coords) > 0:
                new_coords.pop(-1)
                screen.blit(image, (0, 0))
                for i in range(len(new_coords)):
                    pg.draw.circle(screen, (255, 255, 255), new_coords[i], 1)
        elif pg.key.get_pressed()[pg.K_z]:
            if len(new_coords) > 0:
                new_coords.pop(-1)
                screen.blit(image, (0, 0))
                for i in range(len(new_coords)):
                    pg.draw.circle(screen, (255, 255, 255), new_coords[i], 1)
        elif event.type == pg.KEYDOWN and pg.key.get_pressed()[pg.K_s]:
            file = open("coordinate_love.txt", "w")
            json.dump(new_coords,file)
            print(len(new_coords))
            file.close()
            switch = False
    pg.display.flip()
pg.quit()
