import pygame
from enum import Enum
import numpy as np

class GameState(Enum):
    MENU = 0
    CELL_PLACEMENT = 1
    F1_PRESSED = 2
    PLAYING = 3
    QUIT = 4

playfield_x_width = 50
playfield_y_height = 50
playfield = np.zeros((2, playfield_x_width, playfield_y_height), dtype=bool)   
active_playfield = 0 n

life_cycles = 0

FOOTER = 50    # это добавляется к HEIGHT
WIDTH = 550     # ширина экрана
HEIGHT = 550+FOOTER    # и высота
screen_size = (WIDTH, HEIGHT)
BLACK = (0X0,0X0,0x0)
WHITE = (0xff, 0xff, 0xff)

scale_factor_width = WIDTH / playfield_x_width
scale_factor_height = (HEIGHT-FOOTER) / playfield_y_height
spirit_center_adj = scale_factor_width // 2   #this should be the center of the spirit on the screen

# мы начинаем с размещения клеток, прежде чем начать игру жизни
current_game_state = GameState.MENU
last_game_state = current_game_state
cursor_x_position = int(playfield_x_width/2) # поместите курсор в центр игрового поля
cursor_y_position = int(playfield_y_height/2)


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def clearPlayField():
    global life_cycles
    
    life_cycles = 0

    for x in range(playfield_x_width):
        for y in range(playfield_y_height):
            playfield[active_playfield,x,y] = False            

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def getCellNeighbourCount( pos ):
    neighbour_count = 0
    x = pos[0]
    y = pos[1]

    # нам нужно посмотреть на все восемь соседей вокруг этой клетки. 
    # чтобы узнать, есть ли у нас живые соседи.

    # для каждого вычисления этих значений, чтобы не было повторных накладных расходов
    # для каждого вызова функции
    norm_x = normalizeX(x)
    norm_x_plus_one = normalizeX(x+1)
    norm_x_minus_one = normalizeX(x-1)

    norm_y = normalizeY(y)
    norm_y_plus_one = normalizeY(y+1)
    norm_y_minus_one = normalizeY(y-1)

    # посмотреть налево
    if playfield[active_playfield, norm_x_minus_one, norm_y] == True:
        neighbour_count +=1

    # посмотреть направо
    if playfield[active_playfield, norm_x_plus_one, norm_y] == True:
        neighbour_count +=1

    # посмотреть вверх
    if playfield[active_playfield, norm_x, norm_y_minus_one] == True:
        neighbour_count +=1

    # посмотреть вниз
    if playfield[active_playfield, norm_x, norm_y_plus_one] == True:
        neighbour_count +=1

    # если у клетки есть 4 или более соседей, клетка умрет.
    # нам не нужно знать, есть ли более 4 соседей, так как это 
    # не меняет поведение.  Для скорости мы можем использовать сокращение в 
    # условном операторе

    #смотреть налево вверх
    if neighbour_count < 4 and playfield[active_playfield, norm_x_minus_one, norm_y_minus_one] == True:
        neighbour_count +=1

    #смотрите влево-вниз
    if neighbour_count < 4 and playfield[active_playfield, norm_x_minus_one, norm_y_plus_one] == True:
        neighbour_count +=1

    #смотреть прямо-вверх
    if neighbour_count < 4 and playfield[active_playfield, norm_x_plus_one, norm_y_minus_one] == True:
        neighbour_count +=1

    #смотрите вправо-вниз
    if neighbour_count < 4 and playfield[active_playfield, norm_x_plus_one, norm_y_plus_one] == True:
        neighbour_count +=1

    return(neighbour_count)

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def normalizeX(x):

    if x >= 0 and x < playfield_x_width:
        return(x)
    elif x >= playfield_x_width:
        return(0)
    elif x < 0:
        return(playfield_x_width-1)

    return

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def normalizeY(y):
    
    if y >=0 and y < playfield_y_height:
        return(y)
    elif y >= playfield_y_height:
        return(0)
    elif y < 0:
        return(playfield_y_height-1)

    return

#------------------------------------------------------------------------------
# pos - это кортеж в форме (x,y)
#------------------------------------------------------------------------------
def normalizeXY( pos ):
    ret_x = normalizeX(pos[0])
    ret_y = normalizeY(pos[1])
    
    return( (ret_x, ret_y) )

#------------------------------------------------------------------------------
# pos - это кортеж в форме (x,y)
#------------------------------------------------------------------------------
def playfield2screen(game_pos):
    screen_x = (game_pos[0]*scale_factor_width)+spirit_center_adj
    screen_y = (game_pos[1]*scale_factor_height)+spirit_center_adj

    return( (screen_x, screen_y) )

#------------------------------------------------------------------------------
# pos - это кортеж в форме (x,y)
#------------------------------------------------------------------------------
def screen2playfield(screen_pos):
    playfield_x = int(screen_pos[0] /  scale_factor_width)
    playfield_y = int(screen_pos[1] / scale_factor_height)

    return( (playfield_x, playfield_y) )

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def change_playfield_cell(pos, cell_state):
    playfield_pos = screen2playfield(pos)
    playfield[active_playfield, playfield_pos[0], playfield_pos[1]] = cell_state

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def showFrameRate():
    fps=int(clock.get_fps())
    img = font_basic_text.render("FPS: "+str(fps), True, WHITE)
    screen.blit(img, (500, (HEIGHT-FOOTER)+10))

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def draw():
    global screen, font

    screen.fill(BLACK)

    if current_game_state == GameState.MENU:
        img = font_title_text.render("Игра жизни Конвея", True, WHITE)
        screen.blit(img, (100, 80))
        img = font_basic_text.render("Нажмите клавишу 'Пробел' для запуска", True, WHITE)
        screen.blit(img, (100, 150))

    elif current_game_state == GameState.CELL_PLACEMENT:
        img = font_basic_text.render("Чтобы рисовать (левая кнопка) и стирать (правая кнопка)", True, WHITE)
        screen.blit(img, (40, (HEIGHT-FOOTER)))
        img = font_basic_text.render("F1: Запуск/остановка    F3: Очистить", True, WHITE)
        screen.blit(img,(100, (HEIGHT-FOOTER)+20))
        for x in range(playfield_x_width):
            for y in range(playfield_y_height):
                if playfield[active_playfield, x, y] == True:
                    xy_screen = playfield2screen( (x, y) )
                    pygame.draw.circle(screen, WHITE, (xy_screen[0], xy_screen[1]), spirit_center_adj)


    elif current_game_state == GameState.PLAYING:
        img = font_basic_text.render("Life Cycle: "+str(life_cycles), True, WHITE)
        screen.blit(img, (10, (HEIGHT-FOOTER)+10))
        for x in range(playfield_x_width):
            for y in range(playfield_y_height):
                if playfield[active_playfield, x, y] == True:
                    xy_screen = playfield2screen( (x, y) )
                    pygame.draw.circle(screen, WHITE, (xy_screen[0], xy_screen[1]), spirit_center_adj)

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def update():
    global cursor_x_position, cursor_y_position
    global current_game_state, last_game_state
    global playfield, active_playfield
    global life_cycles

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        current_game_state = GameState.QUIT

    if current_game_state == GameState.PLAYING:
        if keys[pygame.K_F1]:
            last_game_state = current_game_state
            current_game_state = GameState.F1_PRESSED

        #используя два игровых поля, мы смотрим на активное и строим неактивное.
        next_playfield = active_playfield ^ 1 # XOR переключение между 0 и 1
        
        for x in range(playfield_x_width):
            for y in range(playfield_y_height):
                
                if playfield[active_playfield, x, y]:   # живая клетка
                    neighbours = getCellNeighbourCount( (x,y) )
                    if neighbours < 2 or neighbours > 3:    # он должен умереть от перенаселенности
                        playfield[next_playfield, x, y] = False
                    else:
                        playfield[next_playfield, x, y] = True     
                else:   # мёртвая клетка
                    neighbours = getCellNeighbourCount( (x,y) )
                    if neighbours == 3:    # размножение!
                        playfield[next_playfield, x, y] = True                    
                    else:
                        playfield[next_playfield, x, y] = False

        active_playfield = next_playfield
        life_cycles += 1

    elif current_game_state == GameState.MENU:
        if keys[pygame.K_SPACE]:
            current_game_state = GameState.CELL_PLACEMENT
        
    elif current_game_state == GameState.CELL_PLACEMENT:
        # были ли нажаты какие-либо клавиши?
        if keys[pygame.K_F1]:
            last_game_state = current_game_state
            current_game_state = GameState.F1_PRESSED
        elif keys[pygame.K_F2]:
            randomInitPlayField()
        elif keys[pygame.K_F3]:
            clearPlayField()

        #кнопок мыши для рисования и удаления ячеек
        mbutton_left, mbutton_middle, mbutton_right = pygame.mouse.get_pressed()
        if mbutton_left:
            change_playfield_cell(pygame.mouse.get_pos(), True)
        elif mbutton_right:
            change_playfield_cell(pygame.mouse.get_pos(), False)


    elif current_game_state == GameState.F1_PRESSED: # позволяет пользователю 
        #отпустить кнопку f1 - пуск/стоп
        if not keys[pygame.K_F1]:
            if last_game_state == GameState.PLAYING:
                current_game_state = GameState.CELL_PLACEMENT
            elif last_game_state == GameState.CELL_PLACEMENT:
                current_game_state = GameState.PLAYING

#******************************************************************************                   
# начало применения
#******************************************************************************                   
pygame.init()
pygame.font.init()
font_basic_text = pygame.font.SysFont(None, 24)
font_title_text = pygame.font.SysFont(None, 48)
screen = pygame.display.set_mode(screen_size)

pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()

while current_game_state != GameState.QUIT:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            current_game_state = GameState.QUIT


    update()
    draw()
    #showFrameRate()
    pygame.display.flip()
    clock.tick(60)

pygame.font.quit()
pygame.quit()