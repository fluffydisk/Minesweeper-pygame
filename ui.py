from utils import SCREEN_WIDTH, SCREEN_HEIGHT, mouse_pos_on_game_x, mouse_pos_on_game_y, clicked_areas, \
    bomb_area_cordinates, bomb_png, flag_png, flag_area_cordinates, number_of_bombs
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

def how_many_bombs_around(bomb_locations, clicked_point):
    number_of_bombs_around=0
    clicked_x=clicked_point[0]
    clicked_y=clicked_point[1]
    for i in bomb_locations:
        if clicked_x-SCREEN_WIDTH/12==i[0] and clicked_y-SCREEN_HEIGHT/12==i[1]:
            number_of_bombs_around+=1
        if clicked_x-SCREEN_WIDTH/12==i[0] and clicked_y+SCREEN_HEIGHT/12==i[1]:
            number_of_bombs_around+=1
        if clicked_x-SCREEN_WIDTH/12==i[0] and clicked_y==i[1]:
            number_of_bombs_around+=1
        if clicked_x==i[0] and clicked_y+SCREEN_HEIGHT/12==i[1]:
            number_of_bombs_around+=1
        if clicked_x==i[0] and clicked_y-SCREEN_HEIGHT/12==i[1]:
            number_of_bombs_around+=1
        if clicked_x+SCREEN_WIDTH/12==i[0] and clicked_y+SCREEN_HEIGHT/12==i[1]:
            number_of_bombs_around+=1
        if clicked_x+SCREEN_WIDTH/12==i[0] and clicked_y == i[1]:
            number_of_bombs_around+=1
        if clicked_x+SCREEN_WIDTH/12==i[0] and clicked_y-SCREEN_HEIGHT/12==i[1]:
            number_of_bombs_around+=1

    return number_of_bombs_around

def every_square_position(bomb_locations):
    list=[]
    status_of_square=[]
    for i in range(1,11):
        for a in range(1,11):
            list.append((a*50, i*50))
    for x in list:
        number_of_bombs = str(how_many_bombs_around(bomb_locations, x))
        if x in bomb_locations:
            status_of_square.append((x, "BOMB"))
        elif number_of_bombs=="0":
            status_of_square.append((x, "EMPTY"))
        else:
            status_of_square.append((x, number_of_bombs))
    return status_of_square

def status_check(wanted_position_to_check, position_info_list):
    for i in position_info_list:
        if i[0]==wanted_position_to_check:
            return i[1]
    return "couldnt find"


def check_if_neighbour_is_empty(clicked_point, position_info_list, clicked_areas):
    x_check = SCREEN_WIDTH / 12
    y_check = SCREEN_HEIGHT / 12

    directions = [
        (0, -y_check),  # up
        (x_check, 0),  # right
        (0, y_check),  # down
        (-x_check, 0),  # left
        (-x_check, -y_check),  # up-left
        (x_check, -y_check),  # up-right
        (-x_check, y_check),  # down-left
        (x_check, y_check)  # down-right
    ]

    to_check = [clicked_point]

    while to_check:
        current_point = to_check.pop()
        for direction in directions:
            neighbor_point = (current_point[0] + direction[0], current_point[1] + direction[1])

            # Updated boundary check to include zero index
            if not (SCREEN_WIDTH /12 <= neighbor_point[0] <= SCREEN_WIDTH / 12 * 10) or not (SCREEN_HEIGHT/12 <= neighbor_point[1] <= SCREEN_HEIGHT / 12 * 10):
                continue

            status = status_check(neighbor_point, position_info_list)

            # If it's empty and hasn't been clicked before, reveal it and check its neighbors
            if status == "EMPTY" and neighbor_point not in clicked_areas:
                clicked_areas.append(neighbor_point)
                to_check.append(neighbor_point)

            # If the neighbor contains a number, reveal it but don't add it to the queue
            elif status != "BOMB" and neighbor_point not in clicked_areas:
                clicked_areas.append(neighbor_point)


def write_remaining_flags(screen, remaining_flags):
    rect=pygame.Rect(SCREEN_WIDTH/12, SCREEN_HEIGHT/36, SCREEN_WIDTH/3, SCREEN_HEIGHT/24)
    pygame.draw.rect(screen, "white", rect)
    font = pygame.font.SysFont("Arial", int(SCREEN_HEIGHT / 24), 1)
    bomb_number = font.render(("Kalan bayrak: " + str(remaining_flags)), 1, "red")
    screen.blit(bomb_number, (SCREEN_WIDTH/12, SCREEN_HEIGHT/36))

def draw_bombs(screen):
    for i in bomb_area_cordinates:
        screen.blit(bomb_png, (i[0], i[1]))

def draw_flags(screen):
    for i in flag_area_cordinates:
        screen.blit(flag_png, (i[0], i[1]))

def draw_numbers(screen, clicked_points, bomb_locations):
    every_square_position(bomb_locations)
    one="blue"
    two="green"
    three="brown"
    four="red"
    color="black"
    font = pygame.font.SysFont("Arial", int(SCREEN_HEIGHT/12), 1)
    for i in clicked_points:
        number_of_bombs = str(how_many_bombs_around(bomb_locations, i))
        if number_of_bombs=="1":
            color=one
        elif number_of_bombs=="2":
            color=two
        elif number_of_bombs=="3":
            color=three
        elif number_of_bombs=="4":
            color=four
        bomb_number = font.render(number_of_bombs, 1, color)
        if number_of_bombs!="0" and i not in bomb_locations:
            screen.blit(bomb_number, (i[0]+SCREEN_WIDTH/48, i[1]+SCREEN_HEIGHT/96))


def draw_clicked_empty_boxes(screen, clicked_areas, bomb_areas):
    for i in clicked_areas:
        if i not in bomb_areas:
            draw_area=pygame.Rect(i[0], i[1], SCREEN_WIDTH / 12, SCREEN_HEIGHT / 12)
            pygame.draw.rect(screen, "gray", draw_area)


def play_screen(screen, mousepos, left_button_clicked, right_buton_clicked, first_click, remaining_flags):
    game_finished=False
    game_win=False
    mouse_pos_x=mousepos[0]
    mouse_pos_y=mousepos[1]
    background_color(screen, "black")
    play_area = pygame.Rect(SCREEN_WIDTH/12, SCREEN_HEIGHT/12, SCREEN_WIDTH/12*10, SCREEN_HEIGHT/12*10)
    pygame.draw.rect(screen, "white", play_area)

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

    if left_button_clicked and mouse_pos_on_game_x!=0 and mouse_pos_on_game_y!=0 and (mouse_pos_on_game_x*SCREEN_WIDTH/12, mouse_pos_on_game_y*SCREEN_HEIGHT/12) not in clicked_areas:
        clicked_point=(SCREEN_WIDTH / 12 * mouse_pos_on_game_x, SCREEN_HEIGHT / 12 * mouse_pos_on_game_y)
        if first_click:
            clicked_areas.append(clicked_point)
            bomb_areas(number_of_bombs, clicked_areas[0])
            first_click=False
        elif [mouse_pos_on_game_x*SCREEN_WIDTH/12, mouse_pos_on_game_y*SCREEN_HEIGHT/12] not in clicked_areas:
            clicked_areas.append(clicked_point)
        status_of_squares = every_square_position(bomb_area_cordinates)
        square_status=status_check((clicked_point), status_of_squares)
        if square_status=="BOMB":
            game_finished=True


        if status_check(clicked_point, status_of_squares) == "EMPTY":
            check_if_neighbour_is_empty(clicked_point, status_of_squares, clicked_areas)

    if right_buton_clicked and mouse_pos_on_game_x!=0 and mouse_pos_on_game_y!=0:
        status_of_squares = every_square_position(bomb_area_cordinates)
        clicked_point = (SCREEN_WIDTH / 12 * mouse_pos_on_game_x, SCREEN_HEIGHT / 12 * mouse_pos_on_game_y)
        if clicked_point not in clicked_areas:
            if clicked_point not in flag_area_cordinates:
                if remaining_flags>0:
                    flag_area_cordinates.append(clicked_point)
                    remaining_flags-=1
            else:
                flag_area_cordinates.remove(clicked_point)
                remaining_flags += 1
    draw_clicked_empty_boxes(screen, clicked_areas, bomb_area_cordinates)
    for i in clicked_areas:
        if i in bomb_area_cordinates:
            draw_bombs(screen)

    draw_flags(screen)
    draw_numbers(screen, clicked_areas, bomb_area_cordinates)
    write_remaining_flags(screen, remaining_flags)
    for y in range(2,11):
        pygame.draw.line(screen, "black", (SCREEN_WIDTH / 12 * y, SCREEN_HEIGHT / 12),(SCREEN_WIDTH / 12 * y, SCREEN_HEIGHT / 12 * 11), 3)
    for x in range (2,11):
        pygame.draw.line(screen, "black", (SCREEN_WIDTH / 12, SCREEN_HEIGHT / 12 * x),(SCREEN_WIDTH / 12 * 11, SCREEN_HEIGHT / 12 * x), 3)


    correct_flags=0

    for i in bomb_area_cordinates:
        if i in flag_area_cordinates:
            correct_flags+=1
    if correct_flags==number_of_bombs:
        game_win=True

    return first_click, game_finished, remaining_flags, game_win


def reload_screen(areas, cordinates, first_click, remaining_flags):
    remaining_flags=15
    first_click=True
    areas.clear()
    cordinates.clear()
    flag_area_cordinates.clear()
    return first_click, remaining_flags