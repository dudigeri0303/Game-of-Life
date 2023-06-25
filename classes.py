import pygame

class Display:
    '''
    A képernyőt definiáló osztály, amin a játék mejelenítésre kerül.
    Konstruktor: width --> az ablak szélessége
                 height --> az ablak magassága
                 icon --> az ikon, ami az ablak tetjén megjelenik
                 capotion --> az ablak tetjén lévő felirat 
    '''
    def __init__ (self, width, height, icon, caption):
        self.width = width
        self.height = height
        self.icon = icon
        self.caption = caption

    def make_display(self):
        '''
        Létrehozza az ablakot a pygame beépített függvénnyével.
        '''
        return pygame.display.set_mode((self.width, self.height), pygame.SCALED)
        
    def set_icon(self):
        '''
        Beállítja az ablak ikonját.
        '''
        return pygame.display.set_icon(self.icon)

    def set_caption(self):
        '''
        Beállítja az ablak feliratát
        '''
        return pygame.display.set_caption(self.caption)

class Colors:
    def __init__(self):
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (39, 139, 39)
        self.blue = (0, 0, 255)
        self.grey = (124, 124, 124)
        self.yellow = (255, 255, 0)


class Cell:
    '''
    Egy sejtet (cellát) definiáló osztály. A pályán minden négyzet egy sejt.
    Konstruktorok: x --> A sejteket tartalmazó kétdimenziós listában elfoglalt első index, a pályán ennyiedik sorban van megjelenítve.
                   y --> A sejteket tartalmazó kétdimenziós listában elfoglalt második index, a pályán ennyiedik oszlopban van megjelenítve.
                   color --> A sejt színe. Ezzel a színnel van megrajolva. A sejt 'alive' állapotától függ.
                   alive --> A sejt állapotát jelentő bool típusú változó. Ha True a sejt életben van, ha False akkor halott.
                   neighbours --> A sejt élő szomszédainak a száma.
                   w --> A sejt szélessége képpontban, amivel majd meg lesz rajzolva.
                   h --> A sejt magassága képpontban, amivel majd meg lesz rajzolva.
                   sbc --> Két sejt közti távolság. (space between cells)
                   surface --> A felület (képernyő), ahova a sejt kirajzolásra kerül.
                   neighbour_list --> Egy lista, amiben a sejt szomszédos sejtjeinek az objektumai vannak. A listában lévő elemek száma a sejt pályán lévő helyétől függ.

    '''
    def __init__(self, x, y, color, alive, neighbours, w, h, sbc, surface, neighbour_list):
        self.x = x
        self.y = y
        self.color = color
        self.alive = alive
        self.neighbours = neighbours
        self.width = w
        self.height = h
        self.surface = surface
        self.sbc = sbc
        self.neighbour_list = neighbour_list

    def __str__(self):
        '''
        Egy sejt objektum értékeit tudjuk ezzel printelni.
        '''
        return f'{self.x} {self.y} {self.color} {self.alive} {self.neighbours} {self.width} {self.height} {self.sbc} {self. surface} {self.neighbour_list}'

    def draw_cell(self):
        '''
        Egy sejt kirajzolsára használt függvény. 
        A sejt megrajzolsásának pontos  x koordíináját úgy kapjuk meg, ha a a sejtek közti távolságnak és a szélességnek az összegét megszorozzuk az oszlop sorszámmal és végül hozzáadjuk a sejtek közti távolságot.
        A sejt megrajzolsásának pontos  y koordíináját úgy kapjuk meg, ha a a sejtek közti távolságnak és a magasságnak az összegét megszorozzuk a sor sorszámmal és végül hozzáadjuk a sejtek közti távolságot.
        A négyzetnek (ami a sejtet jeletni) a szélessége és a  magassága már a konstruktorban definiálva van.
        '''
        pygame.draw.rect(self.surface, self.color,[(self.sbc + self.width) * self.y + self.sbc, (self.sbc + self.height) * self.x + self.sbc, self.width, self.height])



class Button:
    '''
    Egy gombot definiáló soztály. Ezek gombok vannak használva a menükben, hogy rájuk kattintva különböző funkciókat lehessen elérni.
    Konstruktorok: x --> A gomb kirajzolásának x koordinátája.
                   y --> A gomb kirajzolásának y koordinátája.
                   color --> A gomb színe.
                   txt --> A gomb felirata.
                   w --> A gomb szélessége
                   h --> A gomb magassága.
                   border --> A gomb keretének a színe.
                   txt_off_x --> A gomb feliratának szélességi eltolás.
                   txt_off_y --> A gomb feliratának magassági eltolás.
                   surface --> A gomb megjelenítésének a felülete.
                   click --> Bool típusú változó, az egérkattintást vizsgálja.
                   pos --> Az egér helyének koordinátáit tárolja

    '''
    def __init__(self, x, y, color, txt, w, h, border, txt_off_x, txt_off_y, surface, click, pos):
        self.x = x
        self.y = y
        self.color = color
        self.txt = txt
        self.w = w
        self.h = h
        self.border = border
        self.txt_off_x = txt_off_x
        self.txt_off_y = txt_off_y
        self.surface = surface
        self.click = click
        self.pos = pos

    def draw_button(self):
        '''
        Megrajzol egy gombot az konstruktorban definiált felületre, helyre (koordinátákra), méretben (szélesség, magasság)
        '''
        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.w, self.h))
        pygame.draw.rect(self.surface, self.border, (self.x, self.y, self.w, self.h) , 10 )
        self.surface.blit(self.txt, (self.x + self.txt_off_x, self.y + self.txt_off_y))
    
    def check_button_click(self):
        '''
        True logikai értékkel tér vissza, ha az egér koordinátái a gombon belülre esnek és a kattintást jelentő változó igaz. (így tudunk egy gombra kattintani és annak a funkcióját elérni.) 
        '''
        if self.pos[0] > self.x and self.pos[0] < self.x + self.w and self.pos[1] > self.y and self.pos[1] < self.y + self.h and self.click is True:
            return True

    def check_mouse_above_button(self):
        if self.pos[0] > self.x and self.pos[0] < self.x + self.w and self.pos[1] > self.y and self.pos[1] < self.y + self.h:
            return True


class Colorchooser:
    '''
    A főmenüben lévő színválasztót definiáló osztály.
    Konstruktorok: list --> A négy színt jelentő gombokat tartalmazó lista.
                   color --> A kiválasztott szín értékét tárolja.
    '''
    def __init__ (self, list, color):
        self.list = list
        self.color = color

    def make_color_chooser(self):
        '''
        Végigmegy a szín gombokat tartalmazó listán és kirajzolja azokat.
        '''
        for i in range(len(self.list)):
            self.list[i].draw_button()

    def choose_color(self, c0, c1, c2, c3):
        '''
        Az adott színü gombra kattintva megváltoztatja a szín értékét, és visszatér vele.
        '''
        if self.list[0].check_button_click() is True:
            self.color = c0
        elif self.list[1].check_button_click() is True:
            self.color = c1
        elif self.list[2].check_button_click() is True:
            self.color = c2
        elif self.list[3].check_button_click() is True:
            self.color = c3
        return self.color

    def draw_cicrcle_around_color(self, color, surface, c0, c1, c2, c3):
        '''
        Egy fekete kört rajzol a kiválasztott színü gomb köré.
        '''
        if self.color == c0:
            pygame.draw.circle(surface, color, (425, 425), 45, 5)
        elif self.color == c1:
            pygame.draw.circle(surface, color, (500, 425), 45, 5)
        elif self.color == c2:
            pygame.draw.circle(surface, color, (575, 425), 45, 5)
        elif self.color == c3:
            pygame.draw.circle(surface, color, (650, 425), 45, 5)

class Sizechanger:
    def __init__(self, surface, string, font, button, colors):
        self.surface = surface
        self.string = string
        self.font = font
        self.colors = colors
        self.txt = self.font.render(self.string, False, self.colors.black)
        self.button = button
        

    def make_sizechanger(self):
        self.button = Button(500, 525, self.colors.white, self.txt, 225, 100, self.colors.black, 30, 5, self.surface, False, (0, 0))


class Counter:
    '''
    Egy számlálót definiáló osztly.
    Konstruktorok: name --> A számláló neve. Az értéke előtt jelenik meg a kirajzoláskor, hogy tudjuk mit jelent az adott szám.
                   x --> A számláló kirajzolásának x koordinátája.
                   y --> A számláló kirajzolásának y koordinátája.
                   color --> A szín, amivel kiírjuk a szánlálót.
                   value --> Ez tárolja a számlálni való értéket.
                   font --> A betütípus, amivel kiírjuk a számlálót.
                   surface --> A felület, ahova kiírjuk a számlálót.
    '''
    def __init__(self, name, x, y, color,  value, font, surface):
        self.name = name
        self.x = x
        self.y = y
        self.color = color
        self.value = value
        self.font = font
        self.txt = font.render(f'{name}: {str(value)}', False, color)
        self.surface = surface

    def __str__(self):
        return f'{self.txt}'

    def draw_counter(self):
        '''
        Megjeleníti (kiírja) a számlálót a képernyőre.
        '''
        self.surface.blit(self.txt, (self.x, self.y))



class Starting_position:
    '''
    A kezdőpozíciókat definiáló osztály. Ezek mind txt fájlban vannak tárolva és megnyitáskor onnan vannak kiolvasva.
    Konstruktorok: file --> A kezdőállapotot tartalmazó txt fájl neve.
                   size --> A pály mérete, erre azért van szükség, mert külömböző kezdőállapotokat máshol kell megjeleníteni (középen, szélen, stb). Ez alapján vannak eltolva a pályán.
                   list --> A sejteket tartalmazó lista, amin a meghatározott indexeken lévő sejtek .alive értékét True-ra kell állítani, hogy 'életre keljen'.
    '''
    def __init__(self, file, size, list):
        self.file = file
        self.size = size
        self.list = list

    def open_start_pos_topleft(self):
        '''
        Ez a függvény tölti be a kezdőállapotot. Megnyitja a kezdőállapotot tartalmazó fájlt, és soronként végigmegy rajta. Minden sorban két index van, egy x és egy y. 
        Ezeket inté konvertálva a sejteket tartalmazó lista adott index- elem .alive értékét True-ra változtatja. Az alap típús a pálya bal felső sarkától kezdve nyitva meg a poziciót.
        '''
        with open(self.file) as forrasfajl:
            for sor in forrasfajl:
                sor = sor.strip().split(',')
                sor = [int(sor[0]), int(sor[1])]
                try:
                    self.list[sor[0]][sor[1]].alive = True
                except IndexError:
                    pass

    def open_start_pos_middle(self):
        '''
        A pály mértetétől függő mértékben úgy tolja el a megynitás kezdetét, hogy a pozició a pálya közepén legyen.
        '''
        with open(self.file) as forrasfajl:
            for sor in forrasfajl:
                sor = sor.strip().split(',')
                sor = [int(sor[0]), int(sor[1])]
                try:
                    self.list[int(sor[0]+(self.size/2))][int(sor[1]+(self.size/2))].alive = True
                except IndexError:
                    pass
        
    def open_start_pos_spaceship(self):
        '''
        A spaceship típusó kezdőállapotokat tölti be úgy, hogy a minta a pálya szélén/ alján legyen.
        '''
        with open (self.file) as forrasfajl:
            for sor in forrasfajl:
                sor = sor.strip().split(',')
                sor = [int(sor[0]), int(sor[1])]
                try:
                    self.list[sor[0]][sor[1]].alive = True
                except IndexError:
                    pass

    def open_start_pos_spacefiller(self):
        '''
        A teret kitöltő mintát nyitja meg. A pály mértetétől függő mértékben úgy tolja el a megynitás kezdetét, hogy a pozició a pálya közepén legyen.
        Azért kell még egy ilyen függvény, mert ennek a kezdőpoziciónak a mérete nagy, így csak 100 méretü vagy annál nagyobb pályán lehet menyitni.
        '''
        with open (self.file) as forrasfajl:
            for sor in forrasfajl:
                sor = sor.strip().split(',')
                sor = [int(sor[0]), int(sor[1])]
                try:
                    self.list[int(sor[0]+self.size/2)][int(sor[1]+self.size/2)].alive = True
                except IndexError:
                    pass

    def save_own_position(self):
        with open(self.file, 'w') as celfajl:
            for list in self.list:
                for cell in list:
                    if cell.alive == True:
                        indexes = [cell.x, cell.y]
                        print(f'{indexes[0]}, {indexes[1]}', file=celfajl)
   





 







    