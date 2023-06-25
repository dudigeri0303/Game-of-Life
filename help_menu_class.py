import classes as classes

class Helpmenu:
    '''
    A segítség menüt definiáló osztály. Tartalmazza menü megjelenítéséhez, kezeléséhez szükséges függvényeket.
    Konstruktor: surface--> A felület, amin a menü megvan jelenítve.
                 bgcolor--> A menü háttérszíne.
                 running_logic--> A menü loop-jának a futását kezelő bool változó.
                 game--> A Simulation osztályú objektum, ami magát a mejelenítendő, kezelendő játékot jelenti.
                 click--> A kattintást vizsgáló bool változó
                 pos--> Az egér koordinátáit tartalmazó tuple változó
                 back_close--> Az az objektum, ahonnan a menü meglett hívva aminek a.running_logic értékét False-ra kell állítani a menübe lépéskor.                 
    '''
    def __init__ (self, surface, bgcolor, running_logic, game, click, pos, back_close_mm, bakc_close_gl, colors):
        self.surface = surface
        self.bgcolor = bgcolor
        self.running_logic = running_logic
        self.game = game
        self.click = click
        self.pos = pos
        self.back_close_mm = back_close_mm
        self.back_close_gl = bakc_close_gl
        self.colors = colors


    def write_txt(self, txt, pos):
        '''
        Kiií egy szoveget a képernyőre.
        Argumentum: text --> Maga a szöveg
                    pos --> A szöveg koordinátái
        '''
        self.surface.blit(txt, pos)

    def help_menu_redner(self):
        '''
        Kiírja a segítség menübe az irányításhoz szükségez eligazítást, és az előre meghatározott keudőállapotok sorszámát, kis képét amiről tudjuk, hogy melyik milyen.
        '''
        menu_font = classes.pygame.font.SysFont('Comic Sans MS', 60)
        start_pos_txt = menu_font.render('Starting positions:', False, self.colors.black)
        control_txt = menu_font.render('Controls:', False, self.colors.black)

        #Font
        help_font = classes.pygame.font.SysFont('Comic Sans MS', 20)
        #Szövegek listája
        help_txt_list = [help_font.render('Esc: Quit', False, self.colors.black), 
                        help_font.render('Space: Start the simulation', False, self.colors.black),
                        help_font.render('S: Stop the simulation', False, self.colors.black),
                        help_font.render('R: Random starting positon', False, self.colors.black),  
                        help_font.render('C: Clear and restart the simulation', False, self.colors.black),
                        help_font.render('H: Open Help-Menu', False, self.colors.black),
                        help_font.render('Right-Arrow: Run by step', False, self.colors.black),
                        help_font.render('Up-Arrow: Faster simulation', False, self.colors.black),
                        help_font.render('Down-Arrow: Slower sumilation', False, self.colors.black),
                        help_font.render('P: Save your own starting position', False, self.colors.black),
                        help_font.render('O: Open your own starting position', False, self.colors.black)]

        start_txt_list = [menu_font.render('1:', False, self.colors.black),
                        menu_font.render('2:', False, self.colors.black),
                        menu_font.render('3:', False, self.colors.black),
                        menu_font.render('4:', False, self.colors.black),
                        menu_font.render('5:', False, self.colors.black),
                        menu_font.render('6:', False, self.colors.black),
                        menu_font.render('7:', False, self.colors.black),
                        menu_font.render('8:', False, self.colors.black),
                        menu_font.render('9:', False, self.colors.black)]

        #Kezdőállapotok képei
        glider_pic = classes.pygame.image.load('gliderv2.png')
        startpos_pic = classes.pygame.image.load('startposv2.png')
        penta_pic = classes.pygame.image.load('pentadecathlonv2.png')
        pulsar_pic = classes.pygame.image.load('pulsarv4.png')
        copperhead_pic = classes.pygame.image.load('copperheadv2.png')
        five_pic = classes.pygame.image.load('5x5v2.png')
        cloveleaf_pic = classes.pygame.image.load('noname.png')
        cellgun_pic = classes.pygame.image.load('cellgunv2.png')
        hammerhead_pic = classes.pygame.image.load('hammerhead.png')
        netmaker_pic = classes.pygame.image.load('netmaker.png')


        #Az irányításhoz szegitség
        self.write_txt(control_txt, (20, 0))
        h_x = 30
        h_y = 80
        for i in range(0, 9):
            self.write_txt(help_txt_list[i],(h_x, h_y))
            h_y += 30

        h_x = 430
        h_y = 80
        for i in range(9, 11):
            self.write_txt(help_txt_list[i], (h_x, h_y))
            h_y += 30

        #A kezdőpozíciok megjelenítése.
        self.write_txt(start_pos_txt, (20, 350))

        s_x = 75
        s_y = 450
        for i in range(0, 4):
            self.write_txt(start_txt_list[i], (s_x, s_y))
            s_y += 100

        s_x = 325
        s_y = 450
        for i in range(4, 8):
            self.write_txt(start_txt_list[i], (s_x, s_y))
            s_y += 100

        self.write_txt(menu_font.render('9:', False, self.colors.black), (575, 450))
        self.write_txt(menu_font.render('0:', False, self.colors.black), (575, 550))

        self.surface.blit(glider_pic, (150, 450))
        self.surface.blit(startpos_pic, (150, 550))
        self.surface.blit(penta_pic, (150, 650))
        self.surface.blit(pulsar_pic, (150, 750))
        self.surface.blit(copperhead_pic, (400, 450))
        self.surface.blit(five_pic, (400, 550))
        self.surface.blit(cloveleaf_pic, (400, 650))
        self.surface.blit(cellgun_pic, (400, 750 ))
        self.surface.blit(hammerhead_pic, (650, 450))
        self.surface.blit(netmaker_pic, (650, 550))


    def event_handler(self):
        for event in classes.pygame.event.get():     
            if event.type == classes.pygame.QUIT:
                self.running_logic = False
                self.back_close_mm.running_logic = False
                self.back_close_gl.running_logic = False
                return
            
            elif event.type == classes.pygame.MOUSEBUTTONDOWN:
                self.click = True
            elif event.type == classes.pygame.MOUSEBUTTONUP:
                self.click = False

            elif event.type == classes.pygame.KEYDOWN:
                if event.key == classes.pygame.K_ESCAPE:
                    self.running_logic = False
                    self.back_close_mm.running_logic = False
                    self.back_close_gl.running_logic = False
                    return

    def make_handle_bakcbutton(self, button):
         #BackButton
        button.pos = self.pos
        button.click = self.click

        #Make And Handle BackButton
        if button.check_mouse_above_button() is True :
            button.color = self.colors.grey
        else:
            button.color = self.colors.black

        button.draw_button()

        #Visszaképés a főmenübe, ha a vissza gombra kattintunk.
        if button.check_button_click() is True:
            self.click = False
            self.running_logic = False
            return


    def help_menu(self):
        '''
        Ez a főmenüből elérhető segítség menü. Itt vannnak megjelenítve az irányításhoz szükséges instrukciók, és a 
        kezdőállapotok kis képei, betöltésükhoöz szükséges billenytük számai.
        Argumentum: surface --> A segítség menü megjelenítésére szolgáló felület.
                    runnung_logic --> A help_menu loop futását meghatározó bool változó
                    game --> A Simulation típusú objektum, ami magát szimulációt/játékot jelenti.
        '''
        #FontAdatok
        menu_font = classes.pygame.font.SysFont('Comic Sans MS', 60)
        back_txt = menu_font.render('Back', False, self.colors.white)

        back_button = classes.Button(575, 775, self.colors.black, back_txt, 225, 100, self.colors.yellow, 50, 10, self.surface, self.click, self.pos)
        
        #HelpMenu LOOP
        while self.running_logic is True:
            self.surface.fill(self.bgcolor)
            self.pos = classes.pygame.mouse.get_pos()
        
            #Eventek
            self.event_handler()
            
            #Render HelpMenu Txt on SCREEN
            self.help_menu_redner()

            #Backbutton
            self.make_handle_bakcbutton(back_button)

            
            if self.running_logic is False:
                return

            classes.pygame.display.flip()
