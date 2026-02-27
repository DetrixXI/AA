import pygame as pg
import os
import random as rnd
import copy
import tkinter as tk
import time
import traceback
import sys

black = (0,0,0)
white = (100,100,100)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

colors_for_blocks = [blue, red, green, white]

def test():
    print(123)
        
class GameState: #cостояние игры
    def __init__(self):
        self.running = True
        self.pause = False
        self.end = False
        self.fps = 30
        self.counter = 0
        self.font = pg.font.SysFont("TimesNewRoman", 20)

    def handle_events(self, events): #обработка состояния выхода и паузы
        for e in events:
            if e.type == pg.QUIT:
                self.running = False
            elif e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                self.pause = not self.pause
      
def main():

    traceback.print_stack(file=sys.stdout)
    pg.init()
    print(num_of_func)
    print(123123)
    pg.display.set_caption("дробилка")
    ###ОБЩАЯ ИНФО
    #экран/часы/состояние
    width = 300
    width_of_part_of_info = 150
    height = 600
    screen = pg.display.set_mode((width + width_of_part_of_info, height))
    temp_surf = screen
    clock = pg.time.Clock()
    game_state = GameState()
    Flag = True

    #ячейки и строки/столбцы
    strings = 21 
    columns = 11
    cell_width = width / (columns - 1)
    cell_height = height / (strings- 1)


    
    #фигруы териса ([x, y] всего их 7)
    L_fig = [[0,2], [0,1], [0, 0], [1,0]]
    O_fig = [[0,1], [1, 1], [0, 0], [1, 0]]
    S_fig = [[1, 1], [2, 1], [0, 0], [1, 0]]
    T_fig = [[0, 1], [1, 1], [2, 1], [1, 0]]
    Z_fig = [[0, 1], [1, 1], [1, 0], [2, 0]]
    J_fig = [[0, 0], [1, 0], [1, 1], [1, 2]]
    I_fig = [[0 , 0], [0, 1], [0, 2], [0, 3]]

    next_figure_form = 0
    
    figures_temp = (L_fig, O_fig, S_fig, T_fig, Z_fig, J_fig, I_fig)
    figures = []
    for i in range(7):
        figures.append([])
        for j in range(4):
            figures[i].append(pg.Rect(figures_temp[i][j][0] * cell_width + cell_width, figures_temp[i][j][1] * cell_height, cell_width, cell_height))
        figures[i] = tuple(figures[i])
    #фигурес [4 ректа по очереди]

    figures = tuple(figures)          
    falling_figure = copy.deepcopy(figures[6])#не забыть вернуть рандом
    next_figure_form = rnd.randint(0, 6)
    next_figure_color = [rnd.randint(0,255), rnd.randint(0,255), rnd.randint(0,255)]
    block = pg.Rect(0, 0, cell_width, cell_height)
    

    
    
    #ИГРОВАЯ ПОВ_ТЬ
    grid = []
    for i in range(columns): 
        grid.append([])
        for j in range(strings):
            grid[i].append([0]) #т.е. пусто


 
    for i in range(columns): #каждая ячейка поверхности получает свой п.у.
        for j in range(strings):
            grid[i][j].append(pg.Rect(i * cell_width, j * cell_height, cell_width, cell_height)) # Рект(х, у, ширина, высота)
            grid[i][j].append(white)
    #заполенная стека на выходе
    # грид - [есть/нет, Рект, цвет]
            



    flag_is_fall = False
    speed = 1
    temp_text = pg.font.SysFont("TimesNewRoman", 16).render("",True, red) #чтобы текст сохранялся
    flag_pause = False
    flag_end = False
    x, y =0, 0
    ###ИГРОВОЙ ЦИКЛ
    while game_state.running:
        #обработка выхода
        
        events = pg.event.get() #все события за тик списком
        game_state.handle_events(events)
                
        x = 0
        y = 1
        reverse = False


        text = temp_text
         
        #если игра не на пауз
        if (not game_state.pause and not game_state.end):
            ###ОБРАБОТКА ВХОДЯЩЕГО ПОТОКА
            flag_pause = False
              
            for e in events: #обработка нажатия клавищ
                if e.type == pg.KEYDOWN and (e.key == pg.K_UP or e.key == pg.K_w):                 
                   text = pg.font.SysFont("TimesNewRoman", 16).render("ВВЕРХ",True, red)
                   reverse = True

                   
                elif e.type == pg.KEYDOWN and (e.key == pg.K_DOWN or e.key == pg.K_s):               
                   text = pg.font.SysFont("TimesNewRoman", 16).render("ВНИЗ",True, red)

                   
                   
                elif e.type == pg.KEYUP and (e.key == pg.K_RIGHT or e.key == pg.K_d):                
                   text = pg.font.SysFont("TimesNewRoman", 16).render("ВПРАВО",True, red)
                   x += 1

                   
                elif e.type == pg.KEYUP and (e.key == pg.K_LEFT or e.key == pg.K_a):            
                   text = pg.font.SysFont("TimesNewRoman", 16).render("ВЛЕВО",True, red)
                   x -= 1


                key = pg.key.get_pressed() 
                if key[pg.K_s] == 1 or key[pg.K_DOWN]:#обработка ЗАЖАТИЯ dybp
                    speed = 50*game_state.fps

            ###ИГРОВАЯ ЛОГИКА
                
            for i in range(4):#ограничения по врпаво\влево по движ
                column_coord = int(falling_figure[i].x // cell_width)
                string_coord = int(falling_figure[i].y // cell_height)
                    
                if x != 0 and (not (0 <= falling_figure[i].x + x * cell_width <= (len(grid) - 2)* cell_width) or (
                    (x == 1 and grid[column_coord + 1][string_coord][0] == 1) or (x == -1 and grid[column_coord - 1][string_coord][0] == 1))):#проверка перед сдвигом вправо/влево              
                    x = 0
                    break
                
            for i in range(4):#ограничение вниз падение+удаление рядов, если надо 
                column_coord = int(falling_figure[i].x // cell_width)
                string_coord = int(falling_figure[i].y // cell_height)
                if (falling_figure[i].y + cell_height >= height) or (grid[column_coord][string_coord + 1][0] == 1):
                    y = 0
                    for i  in range(4):
                        column_coord = int(falling_figure[i].x // cell_width)
                        string_coord = int(falling_figure[i].y // cell_height)
                        grid[column_coord][string_coord][0] = 1
                        grid[column_coord][string_coord][-1] = next_figure_color

                    row = strings - 1
                    while row >= 0: #само удаление рядов
                        for k in range(columns - 1):
                            if grid[k][row][0] != 1:
                                row -= 1
                                break
                        else:
                            for j in range(row, -1, -1):
                                for k in range(columns - 1):
                                    grid[k][j][0] = grid[k][j - 1][0]
                                    grid[k][j][2] = grid[k][j - 1][2]
                            game_state.counter += (columns - 1)

                    if any([grid[i][0][0] for i in range(columns - 1)]):
                        game_state.end = True
                     
            
                    block.x = 0
                    block.y = 0
                    falling_figure = copy.deepcopy(figures[next_figure_form])#rnd.randint(0, 6)
                    next_figure_color = [rnd.randint(0,255), rnd.randint(0,255), rnd.randint(0,255)]
                    next_figure_form = rnd.randint(0, 6) #предопределение фигуры некст
                    break
            
                

            if reverse:#поворот, фаллинг фигура = 4 ректа по очереди (!!доделать поворот вокруг центра геометрического!!)
                center_x = falling_figure[1].x
                center_y = falling_figure[1].y
                temp_coords = []
                flag_reverse_possibility = True
                for i in range(4):
                    if not (0 <= (falling_figure[i].y - center_y) * (-1) + center_x < width) or (grid[int(((falling_figure[i].y - center_y) * (-1) + center_x) // cell_width)][int(((falling_figure[i].x - center_x) + center_y) // cell_height)][0] == 1):
                        flag_reverse_possibility = False
                        break
                    temp_coords.append([(falling_figure[i].y - center_y) * (-1) + center_x, (falling_figure[i].x - center_x) + center_y])
                if flag_reverse_possibility:
                    for i in range(4):
                        falling_figure[i].x, falling_figure[i].y = temp_coords[i]
                              
            for i in range(len(falling_figure)): #движение по икс
                falling_figure[i].x += x * cell_width

            speed += game_state.fps #движение по игрек
            if speed > 15*game_state.fps:
            #съехал вниз
                speed = 0
                for i in range(len(falling_figure)):
                    falling_figure[i].y += y * cell_height


                
                temp_text = text

            

            ###ОТРИСОВКА
            screen.fill(black) #чистим экран
            for i in range(columns):#рисуем сетку
                for j in range(strings):                  
                    if grid[i][j][0] == 1:                        
                        pg.draw.rect(screen, grid[i][j][-1] , pg.Rect(i * cell_width, j * cell_height, cell_width, cell_height))
                    else:
                        pg.draw.rect(screen, grid[i][j][-1] , pg.Rect(i * cell_width, j * cell_height, cell_width, cell_height), 1)
                    

            for i in range(len(falling_figure)):#рисуем фигуру 
                block.x = falling_figure[i].x
                block.y = falling_figure[i].y
                pg.draw.rect(screen, next_figure_color, block)



            #часть с инфо
            pg.draw.rect(screen, black, pg.Rect(width, 0, width_of_part_of_info, height))
            #screen.blit(text, (width + 50, 0))
            screen.blit(game_state.font.render(f"Cчет: {game_state.counter}", True, red), (width + 10, 0))
            next_figure = copy.deepcopy(figures[next_figure_form])
            screen.blit(pg.font.SysFont("TimesNewRoman", 16).render(f"Следующая фигура", True, red), (width + 10, cell_height))
            for i in range(4):
                block.x = next_figure[i].x + width
                block.y = next_figure[i].y + cell_height*2
                pg.draw.rect(screen, next_figure_color, block)

        

        if game_state.end:#если игра окончена
            if not flag_end:
                pg.draw.rect(screen, black, pg.Rect(0, 150, 600, 65))
                text = game_state.font.render(f"ИГРА ОКОНЧЕНА, ВАШ СЧЕТ {game_state.counter}", True, red)
                screen.blit(text, (50,150))
                text = game_state.font.render(f"НАЖМИТЕ ЭКСЕЙП ЧТОБЫ ВЫЙТ", True, red)
                screen.blit(text, (100,170))
                text = game_state.font.render(f"НАЖМИТЕ R ЧТОБЫ РЕСТАРТ", True, red)
                screen.blit(text, (100,190))
            flag_end = True
            for e in events: #обработка нажатия клавищ
                if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                    game_state.running = False
                    pg.quit()
                if e.type == pg.KEYDOWN and e.key == pg.K_r:
                    num_of_func[0] += 1
                    main() #ПЕРЕДЕЛАТТЬ!!!!!!!!!!!!!!!!!

                    print('ХОЧУ РЕСТАРТ')
            if not game_state.running:
                break
                    
        if game_state.pause and not flag_pause:#если игра на ПАУЗЕ
            flag_pause = True          
            text = game_state.font.render("ПАУЗА", True, red)
            screen.blit(text, (150, 0))



        #экран обнволяется, часы тикают
        pg.display.flip()
        clock.tick(game_state.fps)
    pg.quit()

num_of_func = [0]
main()


"""
for event in :
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False
                    """
