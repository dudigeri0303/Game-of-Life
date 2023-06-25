import classes as classes

class Gameloop:
    '''
    A játékteret definiáló osztály. Tartalmazza a játéktér és a szimulácoó megjelenítéséhez, kezeléséhez szükséges függvényeket.
    Konstruktor: surface--> A felület, amin a játéktér megvan jelenítve.
                 bgcolor--> A játéktér háttérszíne.
                 game--> A Simulation osztályú objektum, ami magát a mejelenítendő, kezelendő játékot jelenti.
                 running_logic--> A játéktér loop-jának a futását kezelő bool változó.
                 cellist--> A sejt objektumokat tartalmazó lista (CELL_LIST)
                 counterlist--> A számláló objektumokat tartalmazó lista (COUNTER_LIST)
                 pos--> Az egér koordinátáit tartalmazó tuple változó
                 helploop--> A Helpmenu objektum, amit a játéktérről lehet megynitni
                 click--> A kattintást vizsgáló bool változó
                 ww--> A játéktér szélessége, az egérkattintáshoz szükséges, hogy ne legyen a pályán kívüli kattintás érzékelve (WINDOW_WIDTH)
                 mapsize--> A szimuláció mérete (MAPSIZE)
           
    '''
    def __init__(self, surface, bgcolor, game, running_logic, celllist, counterlist, pos, helploop, click, ww, mapsize, colors):
        self.surface = surface
        self.bgcolor = bgcolor
        self.game = game
        self.running_logic = running_logic
        self.cellist = celllist
        self.counterlist = counterlist
        self.pos = pos
        self.helploop = helploop
        self.click = click
        self.ww = ww
        self.mapsize = mapsize
        self.colors = colors

    def write_txt(self, text, pos):
        '''
        Kiií egy szoveget a képernyőre.
        Argumentum: text --> Maga a szöveg
                    pos --> A szöveg koordinátái
                    display --> A megjelenítésre használt felület/képernyő
        '''
        self.surface.blit(text, pos)

    def render_counters(self):
        for i in range(len(self.counterlist)):
            self.counterlist[i].draw_counter()

    def write_txt_on_game_loop(self):
        '''
        A játék közben a jobb alsó sarokba kiírja a H:Help segítséget.
        '''
        help_font = classes.pygame.font.SysFont('Comic Sans MS', 20)
        help_txt_v2 = help_font.render('Press H for Help Menu', False, self.colors.yellow)
        self.write_txt(help_txt_v2, (540, 840))

    def get_fps(self, clock):
        help_font = classes.pygame.font.SysFont('Comic Sans MS', 20)
        fps = str(int(clock.get_fps()))
        fps_txt = help_font.render(f'FPS:{fps}', False, self.colors.white)
        self.write_txt(fps_txt , (400, 840 ))

    def draw_lines(self):
        '''
        A játéktér aljára rajzolja ki a számlálókat elválasztó vonalakat.
        '''
        classes.pygame.draw.line(self.surface, self.colors.yellow, (0, 800), (800, 800), 2)
        classes.pygame.draw.line(self.surface, self.colors.yellow, (0, 840), (800, 840))
        classes.pygame.draw.line(self.surface, self.colors.yellow, (0, 872), (800, 872), 3)
        classes.pygame.draw.line(self.surface, self.colors.yellow, (0, 800), (0, 872), 2)
        classes.pygame.draw.line(self.surface, self.colors.yellow, (266, 800), (266, 840))
        classes.pygame.draw.line(self.surface, self.colors.yellow, (380, 840), (380, 875))
        classes.pygame.draw.line(self.surface, self.colors.yellow, (532, 800), (532, 875) )   
        classes.pygame.draw.line(self.surface, self.colors.yellow, (797, 800), (797, 875), 3)

    def game_loop_render(self, clock):
        '''
        A játéktéren megjelenítendő vonalak, számlálók, szövegek kirazjolását egybefoglaló függvény.
        '''
        self.draw_lines()
        self.write_txt_on_game_loop()
        self.render_counters()
        self.get_fps(clock)
       
       

    def event_handler(self, list):
        '''
        A játétéren kezeli az eventeket. Ezek szükségesek a szimuláció irányításához és a kezdőállapotok megynitásához.
        '''
        for event in classes.pygame.event.get():     
            if event.type == classes.pygame.QUIT:
                self.running_logic = False
                return

            #kezdő állapot kijelölése egérrel
            elif event.type == classes.pygame.MOUSEBUTTONDOWN and event.button == 1: #A bal egérgombbal
                self.game.check_click_left(self.ww, self.pos)
            elif event.type == classes.pygame.MOUSEBUTTONDOWN and event.button == 3:
                self.click = True
            elif event.type == classes.pygame.MOUSEBUTTONUP and event.button == 3:
                self.click = False
                
            #A szimuláció irányítása billentyükkel.
            elif event.type == classes.pygame.KEYDOWN:
                if event.key == classes.pygame.K_ESCAPE: #kilépés
                    self.running_logic = False
                    return
                if event.key  == classes.pygame.K_SPACE: #indítás
                    self.game.run = True
                if event.key == classes.pygame.K_s: #megállítás
                    self.game.run = False
                if event.key == classes.pygame.K_RIGHT: #léptető futtatás
                    self.game.run = False
                    self.game.run_by_step = True
                if event.key == classes.pygame.K_r: #random kezdőállapot
                    if self.game.run is False:
                        self.game.random_generator()
                if event.key == classes.pygame.K_DOWN: #lassítás
                    self.game.speed += 100
                if event.key == classes.pygame.K_UP: #gyorsítás
                    if self.game.speed >= 0:
                        self.game.speed -= 100
                if event.key == classes.pygame.K_h:  #segítség menü megnyitása
                    self.game.run = False
                    self.helploop.running_logic = True
                    return self.helploop.help_menu()
                if event.key == classes.pygame.K_c:  #új szimuláció kezdése
                    self.game.run = False    
                    self.game.reset_the_court()

                #proba
                if event.key == classes.pygame.K_a:
                    for i in range(len(self.game.c_list)):
                        for k in range(len(self.game.c_list)):
                            if i == self.game.size // 2 or k == self.game.size // 2:
                                self.game.c_list[i][k].alive = True

                #Előre meghatározott Kezdőállapotok betöltése
                if event.key == classes.pygame.K_0:
                    list[0].open_start_pos_spacefiller()    
                if event.key == classes.pygame.K_1:
                    list[1].open_start_pos_topleft()
                if event.key == classes.pygame.K_2:
                    list[2].open_start_pos_middle()
                if event.key == classes.pygame.K_3:
                    list[3].open_start_pos_middle() 
                if event.key == classes.pygame.K_4:
                    list[4].open_start_pos_middle() 
                if event.key == classes.pygame.K_5:
                    list[5].open_start_pos_middle()
                if event.key == classes.pygame.K_6:
                    list[6].open_start_pos_middle()
                if event.key == classes.pygame.K_7:
                    list[7].open_start_pos_topleft()
                if event.key == classes.pygame.K_8:
                    list[8].open_start_pos_topleft()
                if event.key == classes.pygame.K_9:
                    list[9].open_start_pos_middle()

                #saját kezdő
                if event.key == classes.pygame.K_p:
                    own_starting = list[10]
                    own_starting.save_own_position()
                if event.key == classes.pygame.K_o:
                    list[10].open_start_pos_topleft()



    def game_loop(self):
        '''
        A játéktér loop-ja, amiben az osztály függvényei megvannak hívva. A félkészben ez volt a 'gameloop' nevű függvény.
        '''

        clock = classes.pygame.time.Clock()

        #A kezdőállapotokat tartalmazó lista
        start_pos_list =[classes.Starting_position('netmaker_spacefiller.txt', self.mapsize, self.cellist),
                        classes.Starting_position('glider.txt', self.mapsize, self.cellist) ,
                        classes.Starting_position('start_pos2.txt', self.mapsize, self.cellist),
                        classes.Starting_position('penta_decathlon.txt', self.mapsize, self.cellist),
                        classes.Starting_position('pulsar.txt', self.mapsize, self.cellist),
                        classes.Starting_position('copperhead_spaceship.txt', self.mapsize, self.cellist),
                        classes.Starting_position('5x5.txt', self.mapsize, self.cellist),
                        classes.Starting_position('noname.txt', self.mapsize, self.cellist),
                        classes.Starting_position('glider_gun.txt', self.mapsize, self.cellist),
                        classes.Starting_position('hammerhead.txt', self.mapsize, self.cellist),
                        classes.Starting_position('sajat.txt', self.mapsize, self.cellist)]

        #GAMELOOP
        while self.running_logic is True:
            self.surface.fill(self.bgcolor)
            self.pos = classes.pygame.mouse.get_pos()

            #Eventek
            self.event_handler(start_pos_list)
           
            #jobb egérgombos kijelölés
            if self.click is True:
                self.game.check_click_right(self.click, self.ww, self.pos)
            
            #Indtás
            if self.game.run is True:
                self.game.run_simulation()
                classes.pygame.time.wait(self.game.speed)
            
            #Léptető futás
            if self.game.run_by_step is True:
                self.game.run_simulation()
                #pygame.time.wait(self.game.speed)
                self.game.run_by_step = False

            #Simulation objektumra meghívott függvények
            self.game.get_neighbours_values()  
            self.game.count_cells()
            self.game.blit_cells()
            
            #Vonalak
            self.game_loop_render(clock)

            clock.tick(60)
            if self.running_logic is False:
                return
                
            classes.pygame.display.flip()
  