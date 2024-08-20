import pygame
running = True
reload=False
SCREEN_HEIGHT=600
SCREEN_WIDTH=600

left_mouse_clicked=False
right_mouse_clicked=False

mouse_pos_on_game_x=0
mouse_pos_on_game_y=0

first_click = True

clicked_areas=[]
bomb_area_cordinates=[]
flag_area_cordinates=[]

bomb_png=pygame.image.load("images/bomb.png")
bomb_png=pygame.transform.scale(bomb_png, (SCREEN_WIDTH/12, SCREEN_HEIGHT/12))

flag_png=pygame.image.load("images/flag.png")
flag_png=pygame.transform.scale(flag_png, (SCREEN_WIDTH/12, SCREEN_HEIGHT/12))


rect1_status="NOT_COLLIDED"
rect2_status="NOT_COLLIDED"

SCREEN_TYPE="STARTING"
