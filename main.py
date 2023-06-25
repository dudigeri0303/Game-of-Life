
from help_menu_class import Helpmenu
from main_menu_class import Mainmenu
from game_loop_class import Gameloop
from simulation_class import Simulation
import classes as classes


def main():
    '''
    A main függvény. Ezt meghívva indul el a játék. Először csak a főmenübe jutunk el, onnan tudjuk elérni magát a játékot.
    Itt van inicializáva a pygame, itt vannak létrehozva a változók, listák Itt van létrehozva a Simulation, és a Display, Mainmenu, Helpmenu, Gameloop objektum.
    Ezt meghívva indul el a program.
    '''
    #Pygame incializálása
    classes.pygame.init()
    classes.pygame.display.init()
    classes.pygame.font.init()

    #pygame.mouse.set_cursor(*pygame.cursors.tri_left)

    #Egérpozició
    mouse_position = classes.pygame.mouse.get_pos()

    #Kattintás
    click = False

    #Színeket definiáló osztály
    COLORS = classes.Colors()

    #Képernyő létrehozása
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 875
    ICON = classes.pygame.image.load("pulse-line.png")
    CAPTION = "Game of Life"
    SURFACE = classes.Display(WINDOW_WIDTH, WINDOW_HEIGHT, ICON, CAPTION )
    SURFACE.set_icon()
    SURFACE.set_caption()
    SCREEN = SURFACE.make_display()

    #Főmenü futásának bool változója
    main_menu_running = True
    game_running = True
    help_menu_running = True

    #FROM VARIABLES
    #Hátterek
    BACKGROUND_COLOR = COLORS.black
    MENU_BG_COLOR = COLORS.white
    MAIN_MENU_BG = classes.pygame.image.load('bg_v3.png')

    #Élő sejtek színe
    CELL_COLOR = COLORS.blue

    #Sejtek és számlálók listája
    CELL_LIST = []
    COUNTER_LIST = []

    #A pálya mérete
    MAPSIZE = 80

    #Egy sejt méretei
    WIDTH = 9
    HEIGHT = 9
    SPACE_BETWEEN_CELLS = 1

    #szimuláció létrehozása
    GAME_OF_LIFE = Simulation(CELL_LIST, COUNTER_LIST, MAPSIZE, COLORS, CELL_COLOR, WIDTH, HEIGHT, SPACE_BETWEEN_CELLS, False, False, 100, False)

    #Segítség menü
    HELPMENU = Helpmenu(SCREEN, MENU_BG_COLOR, help_menu_running, GAME_OF_LIFE, click, mouse_position, None, None, COLORS)

    #Játéktér
    GAMELOOP = Gameloop(SCREEN, BACKGROUND_COLOR, GAME_OF_LIFE, game_running, CELL_LIST, COUNTER_LIST, mouse_position, HELPMENU, click, WINDOW_WIDTH, MAPSIZE, COLORS)

    #Főmeü
    MAINMENU = Mainmenu(SCREEN, MAIN_MENU_BG, GAME_OF_LIFE, main_menu_running, GAMELOOP, HELPMENU, mouse_position, click, CELL_COLOR, MAPSIZE, WIDTH, HEIGHT, SPACE_BETWEEN_CELLS, '')

    HELPMENU.back_close_mm = MAINMENU  
    HELPMENU.back_close_gl = GAMELOOP
    

    #Főmenü megynitása
    MAINMENU.main_menu()

    #Pygame bezárása.
    classes.pygame.quit()



