import classes as classes


class Mainmenu:
    '''
    A  főmenüt definiáló osztály. Tartalmazza menü megjelenítéséhez, kezeléséhez szükséges függvényeket.
    Konstruktor: surface--> A felület, amin a menü megvan jelenítve.
                 bgpic--> A menü háttérképe, ami paint-ben van elkészítve (png)
                 game--> A Simulation osztályú objektum, ami magát a mejelenítendő, kezelendő játékot jelenti.
                 running_logic--> A menü loop-jának a futását kezelő bool változó.
                 gameloop--> A Gameloop objektum, ahova a start-ra kattintva el lehet jutni.
                 pos--> Az egér koordinátáit tartalmazó tuple változó
                 helploop-->A Helpmenu objektum, amit a főmenüből lehet megnyitni
                 click--> A kattintást vizsgáló bool változó
                 cellcolor--> Az élő sejtek színét jelentő változó (CELL_COLOR)
                 mapsize--> A szimuláció mérete (MAPSIZE)
                 cellwidth--> A sejt objektumok szélessége(WIDTH)
                 cellheight--> A sejt objektumok magassága(HEIGHT)
                 sbc--> A kirajzolásnál a két sejt közti távolság (SPACE_BETWEEN_CELLS)
                 size_string--> A pályaméretet jelentő sztring, amit inputtal lehet voltoztatni             
    '''
    def __init__ (self, surface, bgpic, game, running_logic, gameloop, helploop, pos, click, cellcolor, mapsize, cellwidth, cellheight, sbc, size_string):
        self.surface = surface
        self.bgpic = bgpic
        self.game = game
        self.running_logic = running_logic
        self.gameloop = gameloop
        self.helploop = helploop
        self.pos = pos
        self.click = click
        self.cellcolor = cellcolor
        self.mapsize = mapsize
        self.cellwidth = cellwidth
        self.cellheight = cellheight
        self.sbc = sbc
        self.size_string = size_string
        self.colors = classes.Colors()


    def write_txt(self, text, pos):
        '''
        Kiií egy szoveget a képernyőre.
        Argumentum: text --> Maga a szöveg
                    pos --> A szöveg koordinátái
        '''
        self.surface.blit(text, pos)

    def main_menu_render(self):
        '''
        Kiírja a főmenübe az összes ott megjelenítendő szöveget.
        '''
        menu_font = classes.pygame.font.SysFont('Comic Sans MS', 60)
        small_menu_font = classes.pygame.font.SysFont('Comic Sans MS', 15)
        color_txt = menu_font.render('Cell Color', False, self.colors.black)
        size_txt = menu_font.render('Size of the map', False, self.colors.black)
        size_help_txt = small_menu_font.render('Type in a number to change the size of the map (min: 40, max: 400)', False, self.colors.black)

        
        self.write_txt(color_txt, (100, 375))
        self.write_txt(size_txt, (0, 525))
        self.write_txt(size_help_txt, (0, 600))

    def event_handler(self):
        '''
        A főmenüben kezeli az eventeket.
        '''
        for event in classes.pygame.event.get():     
            if event.type == classes.pygame.QUIT: #Bezárás
                self.running_logic = False
                return

            #Egér event
            elif event.type == classes.pygame.MOUSEBUTTONDOWN:
                self.click = True
            elif event.type == classes.pygame.MOUSEBUTTONUP:
                self.click = False

            #Billentyü event.
            elif event.type == classes.pygame.KEYDOWN:
                if event.key == classes.pygame.K_ESCAPE: #Bezárás
                    self.running_logic = False
                    return
                if event.key == classes.pygame.K_BACKSPACE: #A size inputból törli az uolsó elemet
                    self.size_string = self.size_string[:-1]
                else:
                    if len(str(self.size_string)) <= 4:
                        self.size_string += event.unicode #A size input szövegéhez hozzáf-zi a begépelt számot.

    def make_handle_start_button(self, sizeinput, button):
        '''
        Létrehozza és kezeli a Start gombot (Button típusú objektum)
        '''

        button.pos = self.pos
        button.click = self.click

        #A gomb kirajzolása
        if button.check_mouse_above_button() is True:
            button.color = self.colors.grey
        else:
            button.color = self.colors.black
        
        button.draw_button()

        if button.check_button_click() is True:  #A start gombra kattintottunk elindul a játék.
            if sizeinput.string != '':
                try:  #A pálya méretének megállapítása, ha az input egy szám.
                    self.mapsize = int(sizeinput.string)
                    if self.mapsize <= 400 and self.mapsize > 39:  #A megadott pályméret beállítása
                        self.mapsize = int(sizeinput.string)
                        self.cellwidth = 800/self.mapsize-1
                        self.cellheight = 800/self.mapsize-1
                    elif self.mapsize < 40:  #Ha túl kicsi --> min méret
                        self.mapsize = 40
                        self.cellwidth = 800/self.mapsize-1
                        self.cellheight = 800/self.mapsize-1
                    else:  #Ha túl nagy --> max méret
                        self.mapsize = 400 
                        self.cellwidth = 800/self.mapsize-1
                        self.cellheight = 800/self.mapsize-1
                except ValueError: #Ha az input nem szám, akkor 80 méretü lesz a pálya
                    self.mapsize = 80
                    self.cellwidth = 800/self.mapsize-1
                    self.cellheight = 800/self.mapsize-1
            #A simulation objektum szükséges, új értékeinek a megváltoztatás, a Játéktér megynitása
            self.game.size = self.mapsize
            self.game.width = self.cellwidth
            self.game.height = self.cellheight
            self.game.sbc = self.sbc
            self.game.make_lists(self.cellheight, self.cellwidth, self.sbc, self.surface)
            self.game.cellcolor = self.cellcolor
            self.game.make_neighbour_list()

            self.running_logic = False
            self.gameloop.mapsize = self.mapsize
            #self.gameloop.running_logic = True

            return self.gameloop.game_loop() #Belépés a game_loop-ba

    def make_handle_help_button(self, button):
        '''
        Létrehozza és kezeli a Help gombot (Button típusú objektum).
        '''

        button.pos = self.pos
        button.click = self.click

        #A gomb kirajzolása
        if button.check_mouse_above_button() is True:
            button.color = self.colors.grey
        else:
            button.color = self.colors.black

        button.draw_button()
        
        #Belépés a segítség menübe kattintás esetén
        if button.check_button_click() is True:
            self.helploop.running_logic = True
            return self.helploop.help_menu()


    def main_menu(self):
        '''
        Ez a főmenü. Megjeleníti az ott lévő színválasztót, pályméret választót, gombokat szövegeket és
        kezeli a külömböző eventeket. Innen lehet elindítani a játékot. Innen is el lehet érni a segítség menüt.
        Argumentum: surface --> A főmenü megjelenítésére szolgáló felület.
                    runnung_logic --> A main menu loop futását meghatározó bool változó
                    game --> A Simulation típusú objektum, ami magát szimulációt/játékot jelenti. Ezt fogja tovább adni a game loop-nak.
        '''        
        #FONT ADATOK
        menu_font = classes.pygame.font.SysFont('Comic Sans MS', 60)
        #print(pygame.display.get_window_size())

        # A menüben lévő szovegek/ feliratok
        start_txt = menu_font.render('Start', False, self.colors.white)
        help_txt = menu_font.render('Help', False, self.colors.white)
        null_txt = menu_font.render('', False, self.colors.white )

        #Start Button
        start_button = classes.Button(0, 200, self.colors.black, start_txt, 400, 125, self.colors.yellow, 100, 25, self.surface, self.click, self.pos)

        ##Help Button
        help_button = classes.Button(400, 200, self.colors.black, help_txt, 400, 125, self.colors.yellow, 100, 25, self.surface, self.click, self.pos)

        #Color buttons
        color_button_list = [classes.Button(400, 400, self.colors.red, null_txt, 50, 50, self.colors.red, 0, 0, self.surface, self.click, self.pos),
                             classes.Button(475, 400, self.colors.blue, null_txt, 50, 50, self.colors.blue, 0, 0, self.surface, self.click, self.pos),
                             classes.Button(550, 400, self.colors.black, null_txt, 50, 50, self.colors.black, 0, 0, self.surface, self.click, self.pos),
                             classes.Button(625, 400, self.colors.green, null_txt, 50, 50, self.colors.green, 0, 0, self.surface, self.click, self.pos)]

        COLOR_CHOOSER = classes.Colorchooser(color_button_list, self.cellcolor)
        
        #MainMenu LOOP
        while self.running_logic is True:
            #Háttér
            self.surface.blit(self.bgpic, (0, 0))
            #Egér koordináták
            self.pos = classes.pygame.mouse.get_pos()

            #Eventek
            self.event_handler()
    

            #Render MinMenu TXT on SCREEN
            self.main_menu_render()

            #Sizeinput
            SIZE_INPUT = classes.Sizechanger(self.surface, self.size_string, menu_font, None, self.colors)
            if SIZE_INPUT.string == '':
                SIZE_INPUT = classes.Sizechanger(self.surface, '80', menu_font, None, self.colors)
            SIZE_INPUT.make_sizechanger() 
            SIZE_INPUT.button.draw_button()

            #Start Button
            self.make_handle_start_button(SIZE_INPUT, start_button)


            #Make And Handle Help Button
            self.make_handle_help_button(help_button)
            

            ##Color chooser
            for i in range(len(color_button_list)):
                color_button_list[i].pos = self.pos
                color_button_list[i].click = self.click
            
            COLOR_CHOOSER.make_color_chooser()
            COLOR_CHOOSER.choose_color(self.colors.red, self.colors.blue, self.colors.black, self.colors.green)
            self.cellcolor = COLOR_CHOOSER.color
            COLOR_CHOOSER.draw_cicrcle_around_color(self.colors.black, self.surface, self.colors.red, self.colors.blue, self.colors.black, self.colors.green)

            if self.running_logic is False:
                return

            classes.pygame.display.update() 