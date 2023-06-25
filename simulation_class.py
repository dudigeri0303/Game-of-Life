import random
import classes as classes

class Simulation:
    '''
    Magát a szimulációt/játékot definiáló osztály. Minden, a szimuláció állapotának a kiszámítására, megjelenítésére, és a szimuláció
    irányításához szükséges függvényt tartalmaz.
    Konstruktorok: c_list --> A CELL_LIST nevú lista, ami az össze sejt objektumot tartalmazza.
                   CT_LIST --> A számlálókat tartalmazó COUNTER_LIST
                   size --> A szimuláció mérete, az egy sorban és oszlopban elhelyezkedő sejtek száma. 
    '''
    def __init__(self, c_list, ct_list, size, colors, cellcolor, width, height, sbc, run, run_by_step, speed, cell_on_screen):
        self.c_list = c_list
        self.ct_list = ct_list
        self.size = size
        self.colors = colors
        self.cellcolor = cellcolor
        self.width = width
        self.height = height
        self.sbc = sbc 
        self.run = run
        self.run_by_step = run_by_step
        self.speed = speed
        self.cell_on_screen = cell_on_screen

    def __str__(self):
        return f'{self.size} {len(self.c_list)}'
     

    def make_lists(self, w, h, sbc, screen):
        '''
        Feltölti a két listát. A CELL_LIST-et a pálya méretétől föggően, 2 dimenziós listaként tele pakolja alap állapotú, halott sejtekkel. Az indexeket 
        (amikkel a sejtek koordinátái ki vannak számolva, és ami alapján tudunk rájuk hivtakozni) a két for ciklus értékei jelentik. Ezek a pálya méretétől függően futnak le. 
        A COUNTER_LIST-be bele rakja a 3 számlálót, amik az életben lévő, született és meghalt sejtek számát számlálják. Kezdetben ezek mind 0 értéküek 
        '''
        font = classes.pygame.font.SysFont('Comic Sans MS', 30) #A számlálók betütípusa
        for i in range(self.size):
            self.c_list.append([])
            for k in range(self.size):
                cell = classes.Cell(i, k, self.colors.white, False, 0, w, h, sbc ,screen, []) # Egy alap állapotú sejt
                self.c_list[i].append(cell)

        self.ct_list.append(classes.Counter('Alive', 30, 800, self.colors.white, 0, font, screen ))  
        self.ct_list.append(classes.Counter('Bornt', 270, 800, self.colors.white, 0, font, screen ))
        self.ct_list.append(classes.Counter('Died', 535, 800, self.colors.white, 0, font, screen ))
        self.ct_list.append(classes.Counter('Generations', 30, 832, self.colors.white, 0, font, screen ))

        return self.c_list, self.ct_list


    def make_neighbour_list(self):
        '''
        Minden sejt neighbour_list értékeére (ami kezdetben egy üres lista) egy, a szomszédos sejteket tároló listát állít. A sejtek a 
        pályán lévő pozíciójuktól függően külömbosző számú szomszéddal rendelkeznek. A sarkoknak 3 szomszédja van, a széleknek 5 
        és a középen lévőknek pedig 8. A sok if az adott sejt pályán lévő helyének a meghatározásához kell.
        '''
        for i in range(self.size):
            for k in range(self.size):
                if i > 0 and i < self.size-1:
                    if k > 0 and k < self.size-1: #Közép.
                        self.c_list[i][k].neighbour_list = [ self.c_list[i-1][k-1], self.c_list[i-1][k], self.c_list[i-1][k+1], self.c_list[i][k-1], self.c_list[i][k+1], self.c_list[i+1][k-1], self.c_list[i+1][k], self.c_list[i+1][k+1] ] 
                    if k == 0: #Bal szél.
                        self.c_list[i][k].neighbour_list = [ self.c_list[i-1][k], self.c_list[i-1][k+1], self.c_list[i][k+1], self.c_list[i+1][k], self.c_list[i+1][k+1] ]
                    if k == self.size -1: #Jobb szél.
                        self.c_list[i][k].neighbour_list = [ self.c_list[i-1][k-1], self.c_list[i-1][k], self.c_list[i][k-1], self.c_list[i+1][k-1], self.c_list[i+1][k] ]
                if i == 0:
                    if k>0 and k < self.size -1: # Felső szél
                        self.c_list[i][k].neighbour_list = [ self.c_list[i][k-1], self.c_list[i][k+1], self.c_list[i+1][k-1], self.c_list[i+1][k], self.c_list[i+1][k+1] ]
                    if k == 0: #Bal felső sarok
                        self.c_list[i][k].neighbour_list = [ self.c_list[i][k+1], self.c_list[i+1][k], self.c_list[i+1][k+1] ]
                    if k == self.size - 1: #Jobb felső sarok
                        self.c_list[i][k].neighbour_list = [ self.c_list[i][k-1], self.c_list[i+1][k-1], self.c_list[i+1][k] ]
                if i == self.size - 1:
                    if k>0 and k< self.size -1: #Alsó szél 
                        self.c_list[i][k].neighbour_list = [ self.c_list[i-1][k-1], self.c_list[i-1][k], self.c_list[i-1][k+1], self.c_list[i][k-1], self.c_list[i][k+1] ]
                    if k == 0: #Bal alsó sarok
                        self.c_list[i][k].neighbour_list = [ self.c_list[i-1][k], self.c_list[i-1][k+1], self.c_list[i][k+1] ]
                    if k == self.size -1: #Jobb alsó sarok
                        self.c_list[i][k].neighbour_list = [ self.c_list[i-1][k-1], self.c_list[i-1][k], self.c_list[i][k-1] ]

    def blit_cells(self):
        '''
        Végig megy a CELL_LIST-en és minden sejt objektumra meghívja a .draw_cell függvény, így kirajzolja azokat a pályára.
        '''
        for i in range(self.size):
            for k in range(self.size):
                c = self.c_list[i][k]
                if c.alive is False:
                    c.color = self.colors.white
                elif c.alive is True:
                    c.color = self.cellcolor
                c.draw_cell()

    def get_neighbours_values(self):
        '''
        Létrehoz egy számlálót és végigmegy a CELL_LIST-en és minden sejt .neighbour_list listáján is. Ha az adott szomszéd .alive értéke True, akkor a számlálót megnöveli 1-gyel.
        Végül az adott sejt .neighbour, élő szomszédos sejtek számát tartalmazó értékét a számláló értékére állítja be, így tartva nyomon, az adott körben minden sejt élő szomszédainak
        a számát. 
        '''
        osszeg = 0
        for i in range(self.size):
            for k in range(self.size):
                for j in range(len(self.c_list[i][k].neighbour_list)):
                    if self.c_list[i][k].neighbour_list[j].alive == True:
                        osszeg += 1 
                self.c_list[i][k].neighbours = osszeg
                osszeg = 0  

    def run_simulation(self):
        '''
        Ez a függvény határozza a pályán lévő sejtek következő generációját a játék szabályai alapján (Ezek a specifikációban vannak leírva).
        Végigmegy a CELL_LIST minden elemén, és az élő szomszédok száma alapja meghatározza, hogy a sejt ha él túlél, meghal, vagy ha halott, akkor életre kel-e. 
        Ezen kívül, még a született és meghalt sejteket számlálók értékét is változtatják az adott esemény szerint.
        '''
        self.cell_on_screen = False
        
        for i in range(self.size):
            for k in range(self.size):
                if self.c_list[i][k].alive == True:  #A sejt életben van
                    if self.c_list[i][k].neighbours == 2 or self.c_list[i][k].neighbours == 3:  #2 vagy 3 élő szomszédja van --> túlél.
                        self.c_list[i][k].alive = True
                    if self.c_list[i][k].neighbours > 3:  #Több mint 3 élő szomszédja van --> meghal. 
                        self.c_list[i][k].alive = False
                        self.ct_list[2].value += 1  #A halott sejteket számát 1-gyel növeli
                        self.ct_list[2].txt = self.ct_list[2].font.render(f'{self.ct_list[2].name}: {str(self.ct_list[2].value)}', False, self.ct_list[2].color)  #A számláéó feliratát beállítja az új érték szerint.
                    if self.c_list[i][k].neighbours == 1 or self.c_list[i][k].neighbours == 0:  #1 vagy 0 élő szomszédja van --> meghal
                        self.c_list[i][k].alive = False
                        self.ct_list[2].value += 1  #A halott sejteket számát 1-gyel növeli
                        self.ct_list[2].txt = self.ct_list[2].font.render(f'{self.ct_list[2].name}: {str(self.ct_list[2].value)}', False, self.ct_list[2].color)  #A számláéó feliratát beállítja az új érték szerint.
                if self.c_list[i][k].alive is False:  #A sejt halott.
                    if self.c_list[i][k].neighbours == 3: #Pontosan 3 élő szomszédja van --> életre kel
                        self.c_list[i][k].alive = True
                        self.ct_list[1].value += 1  #A született sejteket számát 1-gyel növeli
                        self.ct_list[1].txt = self.ct_list[1].font.render(f'{self.ct_list[1].name}: {str(self.ct_list[1].value)}', False, self.ct_list[1].color)  #A számláéó feliratát beállítja az új érték szerint.
        
        for list in self.c_list:
            for cell in list:
                if cell.alive == True:
                    self.cell_on_screen = True
                    break
        
        if self.cell_on_screen is True:
            self.ct_list[3].value += 1
            self.ct_list[3].txt = self.ct_list[3].font.render(f'{self.ct_list[3].name}: {str(self.ct_list[3].value)}', False, self.ct_list[3].color)
        

    def random_generator(self):
        '''
        Véletlenszerú kezdőállapotot állít elő. Végigmegy a CELL_LIST összes elemén, és a .alive értékét random módon True-ra vagy Falase-ra állítja.
        Az életben lévő sejtek számlálóját 1-gyel nagyobbra állítja, ha az addot sejt épp léetben van.
        '''
        choice_list = [True, False]
        for i in range(self.size):
            for k in range(self.size):
                self.c_list[i][k].alive = random.choice(choice_list)
                if self.c_list[i][k].alive == True:
                    self.ct_list[1].value += 1
                    self.ct_list[1].txt = self.ct_list[1].font.render(f'{self.ct_list[1].name}: {str(self.ct_list[1].value)}', False, self.ct_list[1].color)

    def reset_the_court(self):
        '''
        Nulláza pálya és a számlálók állását. Végimegy a CELL_LIST összes elemén, és a .alive értékét False-ra állítja, így a pályán az összes sejt ahlott lesz.
        Így lehet új szimulációt kezdeni.
        '''
        for i in range(self.size):
            for k in range(self.size):
                self.c_list[i][k].alive = False

        self.ct_list[1].value = 0
        self.ct_list[1].txt = self.ct_list[1].font.render(f'{self.ct_list[1].name}: {str(self.ct_list[1].value)}', False, self.ct_list[1].color)
        self.ct_list[2].value = 0
        self.ct_list[2].txt = self.ct_list[2].font.render(f'{self.ct_list[2].name}: {str(self.ct_list[2].value)}', False, self.ct_list[2].color)
        self.ct_list[3].value = 0
        self.ct_list[3].txt = self.ct_list[1].font.render(f'{self.ct_list[3].name}: {str(self.ct_list[3].value)}', False, self.ct_list[3].color)

    def check_click_left(self, ww, pos):
        '''
        A bal egérgombbal való kezdőállapot kijelölését teszi lehetővé.Egy kattintással egy sejtet lehet életre kelteni.
        Az adott sejt indexeit a az egér x/y koordinátájannak és a szélesség/magasság egész osztásával kapjuk meg.
        '''
        x = pos[0] // (self.width + self.sbc)
        y = pos[1] // (self.height + self.sbc)
        if pos[1] <= ww:
            #print(self.c_list[int(y)][int(x)])
            self.c_list[int(y)][int(x)].alive = True

    def check_click_right(self, click, ww, pos):
        '''
        A jobb egérgombbal való kezdőállapot kijelölését teszi lehetővé.A jobb egérgombot nyomva tartva egyszerre sok sejtet lehet életre keltni.
        Az adott sejt indexeit a az egér x/y koordinátájannak és a szélesség/magasság egész osztásával kapjuk meg.
        '''
        if click is True:
            x = pos[0] // (self.width + self.sbc)
            y = pos[1] // (self.height + self.sbc)
            if pos[1] < ww:
                self.c_list[int(y)][int(x)].alive = True
            

    def count_cells(self):
        '''
        Megszámolja a pályán lévő élő sejtek számát a CELL_LIST elemeinek a .alive értékével (True=élő, False=halott).
        Az élő sejtek számát számon tartó számláló értékét erre a számra állítja be.
        '''
        a = 0
        for i in range(self.size):
            for k in range(self.size):
                if self.c_list[i][k].alive == True:
                    a += 1
        self.ct_list[0].value = a
        self.ct_list[0].txt = self.ct_list[0].font.render(f'{self.ct_list[0].name}: {str(self.ct_list[0].value)}', False, self.ct_list[0].color)