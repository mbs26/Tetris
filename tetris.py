import pygame
from pygame.locals import*
import random
import sys

screen_x=13
screen_y=25

def load_image(dir,ALPHA):
    try:
        image=pygame.image.load(dir)
    except:
        print('No se ha podido cargar el fichero')
        sys.exit(1)
    if ALPHA:
        image=image.convert_alpha()
    else:
        image=image.convert()
    return image

class bloque:
    def __init__(self):
        self.posx=4
        self.posy=0

        self.pieza_1=[ [[1,1,1,1]] , [[1],[1],[1],[1]] ] # orientacion de la pieza: 0 o 1 (este caso)
        self.pieza_2=[ [[1,0,0],[1,1,1]] , [[1,1],[1,0],[1,0]] , [[1,1,1],[0,0,1]], [[0,1],[0,1],[1,1]] ]
        self.pieza_3=[ [[0,0,1],[1,1,1]] , [[1,0],[1,0],[1,1]] , [[1,1,1],[1,0,0]], [[1,1],[0,1],[0,1]] ]
        self.pieza_4=[ [[1,1],[1,1]] ]
        self.pieza_5=[ [[0,1,1],[1,1,0]] , [[1,0],[1,1],[0,1]] ]
        self.pieza_6=[ [[1,1,0],[0,1,1]] , [[0,1],[1,1],[1,0]] ]
        self.pieza_7=[ [[0,1,0],[1,1,1]] , [[1,0],[1,1],[1,0]] , [[1,1,1],[0,1,0]] , [[0,1],[1,1],[0,1]] ]

        self.piezas=[self.pieza_1,self.pieza_2,self.pieza_3,self.pieza_4,self.pieza_5,self.pieza_6,self.pieza_7]

        self.orient=0 # se inicializa con la orientacion 0
        self.actual=random.randint(0,len(self.piezas)-1) # elegimos la pieza inicial
        self.ori=self.piezas[self.actual][self.orient%len(self.piezas[self.actual])]

        self.siguiente=random.randint(0,len(self.piezas)-1)

    def paso(self,tablero):
        for x in range(len(self.ori)):
            for y in range(len(self.ori[x])):
                if self.posx+x>=screen_x or self.posy+1+y>=screen_y:
                    return False
                elif tablero.tablero[self.posx+x][self.posy+1+y]!=-1 and self.ori[x][y]==1:
                    return False
        else:
            self.posy+=1
            return True

    def dir(self,tablero,a):
        for x in range(len(self.ori)):
            for y in range(len(self.ori[x])):
                if self.posx+x+a>=screen_x or self.posy+y>=screen_y or self.posx+x+a<0:
                    return False
                elif tablero.tablero[self.posx+x+a][self.posy+y]!=-1 and self.ori[x][y]==1:
                    return False
        else:
            self.posx+=a
            return True

    def cambiar_ori(self,tablero):
        nueva_ori=self.piezas[self.actual][(self.orient+1)%len(self.piezas[self.actual])]
        posx_nueva=self.posx if (self.posx+len(nueva_ori))<=screen_x else self.posx-len(nueva_ori)+1
        for x in range(len(nueva_ori)):
            for y in range(len(nueva_ori[x])):
                if posx_nueva+x>=screen_x or self.posy+y>=screen_y or posx_nueva+x<0:
                    return False
                elif tablero.tablero[posx_nueva+x][self.posy+y]!=-1 and nueva_ori[x][y]==1:
                    return False
        else:
            self.posx=posx_nueva
            self.ori=nueva_ori
            self.orient+=1
            return True

    def nueva(self,tablero):
        self.posx=4
        self.posy=0

        self.orient=0 # se inicializa con la orientacion 0
        self.actual=self.siguiente # elegimos la pieza inicial
        self.ori=self.piezas[self.actual][self.orient%len(self.piezas[self.actual])]

        for x in range(len(self.ori)):
            for y in range(len(self.ori[x])):
                if self.posx+x>=screen_x or self.posy+y>=screen_y or self.posx+x<0:
                    return False
                elif tablero.tablero[self.posx+x][self.posy+y]!=-1 and self.ori[x][y]==1:
                    return False
        else:
            self.siguiente=random.randint(0,len(self.piezas)-1)
            return True

class tablero:
    def __init__(self):
        self.colores=[load_image('azul_claro.png',0),load_image('azul.png',0),
                        load_image('naranja.png',0),load_image('amarillo.png',0),
                        load_image('verde.png',0),load_image('morado.png',0),
                        load_image('rojo.png',0),load_image('negro.png',0)]

        self.tablero=[]
        for x in range(screen_x):
            self.tablero.append([-1 for y in range(screen_y)]) # el color -1 es el ultimo de la lista de colores, negro

    def comprobar_lineas(self):
        eliminar=[]
        for y in range(len(self.tablero[0])):
            count=0
            for x in range(len(self.tablero)):
                if self.tablero[x][y]!=-1:
                    count+=1
            if count==len(self.tablero):
                eliminar.append(y)
        for el in eliminar:
            for x in range(len(self.tablero)):
                 self.tablero[x].pop(el)
                 self.tablero[x].insert(0,-1)
        return len(eliminar)
    def reset(self):
        for x in range(screen_x):
            for y in range(screen_y):
                self.tablero[x][y]=-1

class boton:
    def __init__(self,posx,posy,ancho,alto):
        self.posx=posx
        self.posy=posy
        self.ancho=ancho
        self.alto=alto
    def encima(self,raton):
        if (self.posx+self.ancho)>raton[0] and self.posx<raton[0] and (self.posy+self.alto)>raton[1] and self.posy<raton[1]:
            return True
        else:
            return False

def main():
    pygame.init()
    screen=pygame.display.set_mode((20*screen_x,20*screen_y+100))
    pygame.display.set_caption('Tetris')
    pygame.display.set_icon(load_image('icon.png',1))

    pygame.key.set_repeat(100,30)

    myfont=pygame.font.SysFont('Arial',17)
    gris=load_image('gris.png',0)

    board=tablero()
    pieza=bloque()
    reset=boton(0,20*screen_y,20*screen_x,100)

    clock=0
    puntuacion=0

    metas=[20,50,100,150,200,300,400,600,1000,2000,3000,4000,5000,6000,7000,8000,9000,10000,11000]
    velocidades=[30,27,25,22,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5]

    nivel=0

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                if event.key==K_UP:
                    pieza.cambiar_ori(board)
                elif event.key==K_DOWN:
                    pieza.paso(board)
                elif event.key==K_RIGHT:
                    pieza.dir(board,1)
                elif event.key==K_LEFT:
                    pieza.dir(board,-1)
                elif event.key==K_ESCAPE:
                    pause=True
                    while pause:
                        for event in pygame.event.get():
                            if event.type==pygame.QUIT:
                                sys.exit()
                            elif event.type==pygame.MOUSEBUTTONDOWN and reset.encima(pygame.mouse.get_pos()):
                                pause=False
                        pygame.time.delay(50)
            break

        for x in range(len(board.tablero)):
            for y in range(len(board.tablero[x])):
                screen.blit(board.colores[board.tablero[x][y]],(20*x,20*y))
        for x in range(len(pieza.ori)):
            for y in range(len(pieza.ori[x])):
                if pieza.ori[x][y]==1:
                    screen.blit(board.colores[pieza.actual],(20*(pieza.posx+x),20*(pieza.posy+y)))
        for x in range(len(board.tablero)):
            for y in range(5):
                screen.blit(gris,(20*x,20*(y+screen_y)))
        screen.blit(myfont.render('Puntuación: {0}'.format(puntuacion) ,False,(0,0,0)),(5,20*screen_y))
        screen.blit(myfont.render('{0}'.format(velocidades[nivel]) ,False,(0,0,0)),(5,20*screen_y+50))
        for x in range(len(pieza.piezas[pieza.siguiente][0])):
            for y in range(len(pieza.piezas[pieza.siguiente][0][x])):
                if pieza.piezas[pieza.siguiente][0][x][y]==1:
                    screen.blit(board.colores[pieza.siguiente],(20*(screen_x-3+x)+10,20*(screen_y+y)+10))
        pygame.display.flip()

        if clock>velocidades[nivel]:
            clock=0
            if not pieza.paso(board):
                for x in range(len(pieza.ori)):
                    for y in range(len(pieza.ori[x])):
                        if pieza.ori[x][y]==1:
                            board.tablero[pieza.posx+x][pieza.posy+y]=pieza.actual
                if not pieza.nueva(board):
                    myfont2=pygame.font.SysFont('Arial',25)
                    screen.blit(myfont2.render('Game Over'.format(puntuacion) ,False,(255,0,0)),(10,20*screen_y+50))
                    pygame.display.flip()
                    resetting=False
                    while not resetting:
                        for event in pygame.event.get():
                            if event.type==pygame.QUIT:
                                sys.exit()
                            elif event.type==pygame.MOUSEBUTTONDOWN and reset.encima(pygame.mouse.get_pos()):
                                puntuacion=0
                                board.reset()
                                nivel=0
                                resetting=True
                        pygame.time.delay(50)
                pygame.time.delay(250)
            puntuacion+=board.comprobar_lineas()*screen_x

        if puntuacion>metas[nivel]:
            nivel+=1

        pygame.time.delay(10)
        clock+=1

if __name__=='__main__':
    main()
