from utils import SCREEN_WIDTH, SCREEN_HEIGHT, mouse_pos_on_game_x, mouse_pos_on_game_y, clicked_areas, \
    bomb_area_cordinates, bomb_png, flag_png, flag_area_cordinates
import pygame, random

def background_color(screen, color):
    screen.fill(color)

def start_buttons(screen, rect1, rect2):
    rect_x1 = int(SCREEN_WIDTH / 12)
    rect_y1 = int(SCREEN_HEIGHT / 3 * 2)
    rect_width1 = int(SCREEN_WIDTH / 3)
    rect_height1 = int(SCREEN_HEIGHT / 6)
    button1_rect = pygame.Rect(rect_x1, rect_y1, rect_width1, rect_height1)
    if rect1=="NOT_COLLIDED":
        rect_color1 = "black"
    elif rect1=="ON_BUTTON":
        rect_color1 = "white"
    elif rect1=="CLICKED":
        rect_color1 = "brown"
        print("clicked1")
    pygame.draw.rect(screen, rect_color1, button1_rect)

    rect_x2 = int(SCREEN_WIDTH / 12 * 7)
    rect_y2 = int(SCREEN_HEIGHT / 3 * 2)
    rect_width2 = int(SCREEN_WIDTH / 3)
    rect_height2 = int(SCREEN_HEIGHT / 6)
    button2_rect = pygame.Rect(rect_x2, rect_y2, rect_width2, rect_height2)
    if rect2=="NOT_COLLIDED":
        rect_color2 = "black"
    elif rect2=="ON_BUTTON":
        rect_color2 = "white"
    elif rect2=="CLICKED":
        rect_color2 = "brown"
        print("clicked2")
    pygame.draw.rect(screen, rect_color2, button2_rect)

    return button1_rect, button2_rect

def start_screen(screen, rect1, rect2):
    background_color(screen, "blue")
    return start_buttons(screen, rect1, rect2)

def bomb_areas(bomb_numbers, first_click):
    for i in range (1,bomb_numbers+1):
        bomb_x=random.randint(1,10)
        bomb_y=random.randint(1,10)
        bomb_x*=SCREEN_WIDTH/12
        bomb_y*=SCREEN_HEIGHT/12

        while (bomb_x==first_click[0] and bomb_y == first_click[1]) or (bomb_x, bomb_y) in bomb_area_cordinates:
            bomb_x = random.randint(1, 10)
            bomb_y = random.randint(1, 10)
            bomb_x *= SCREEN_WIDTH / 12
            bomb_y *= SCREEN_HEIGHT / 12
        bomb_area_cordinates.append((bomb_x, bomb_y))

def draw_bombs(screen):
    for i in bomb_area_cordinates:
        screen.blit(bomb_png, (i[0], i[1]))

def draw_flags(screen):
    for i in flag_area_cordinates:
        screen.blit(flag_png, (i[0], i[1]))

def play_screen(screen, mousepos, left_button_clicked, right_buton_clicked, first_click):
    mouse_pos_x=mousepos[0]
    mouse_pos_y=mousepos[1]
    background_color(screen, "black")
    play_area = pygame.Rect(SCREEN_WIDTH/12, SCREEN_HEIGHT/12, SCREEN_WIDTH/12*10, SCREEN_HEIGHT/12*10)
    pygame.draw.rect(screen, "white", play_area)
    for y in range(2,11):
        pygame.draw.line(screen, "black", (SCREEN_WIDTH / 12 * y, SCREEN_HEIGHT / 12),(SCREEN_WIDTH / 12 * y, SCREEN_HEIGHT / 12 * 11), 3)
    for x in range (2,11):
        pygame.draw.line(screen, "black", (SCREEN_WIDTH / 12, SCREEN_HEIGHT / 12 * x),(SCREEN_WIDTH / 12 * 11, SCREEN_HEIGHT / 12 * x), 3)

    for column in range(1, 12):
        mouse_pos_on_game_x=0
        if mouse_pos_x<SCREEN_WIDTH/12*column and mouse_pos_x>SCREEN_WIDTH/12*(column-1) and mouse_pos_x>SCREEN_WIDTH/12 and mouse_pos_x<SCREEN_WIDTH/12*11 and mouse_pos_y>SCREEN_HEIGHT/12 and mouse_pos_y<SCREEN_HEIGHT/12*11:
            mouse_pos_on_game_x = column - 1
            break

    for row in range(1, 12):
        mouse_pos_on_game_y = 0
        if mouse_pos_y < SCREEN_HEIGHT / 12 * row and mouse_pos_y > SCREEN_HEIGHT / 12 * (row - 1) and mouse_pos_x>SCREEN_WIDTH/12 and mouse_pos_x<SCREEN_WIDTH/12*11 and mouse_pos_y>SCREEN_HEIGHT/12 and mouse_pos_y<SCREEN_HEIGHT/12*11:
            mouse_pos_on_game_y = row - 1
            break

    if left_button_clicked and mouse_pos_on_game_x!=0 and mouse_pos_on_game_y!=0:
        if first_click:
            clicked_areas.append([SCREEN_WIDTH / 12 * mouse_pos_on_game_x, SCREEN_HEIGHT / 12 * mouse_pos_on_game_y])
            bomb_areas(10, clicked_areas[0])
            first_click=False
        else:
            clicked_areas.append([SCREEN_WIDTH / 12 * mouse_pos_on_game_x, SCREEN_HEIGHT / 12 * mouse_pos_on_game_y])

    if right_buton_clicked and mouse_pos_on_game_x!=0 and mouse_pos_on_game_y!=0:
        flag_area_cordinates.append([SCREEN_WIDTH / 12 * mouse_pos_on_game_x, SCREEN_HEIGHT / 12 * mouse_pos_on_game_y])
    for i in clicked_areas:
        draw_area=pygame.Rect(i[0], i[1], SCREEN_WIDTH / 12, SCREEN_HEIGHT / 12)
        pygame.draw.rect(screen, "black", draw_area)
    draw_bombs(screen)
    draw_flags(screen)
    return first_click


def reload_screen(areas, cordinates, first_click):
    first_click=True
    first_playack = True
    areas.clear()
    cordinates.clear()
    return first_click, first_playack