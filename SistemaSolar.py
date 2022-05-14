#!/usr/bin/env python3


import sys
import pygame
import math
import os.path

class SistemaSolar(object):
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()

        self.fuente=pygame.font.SysFont("Arial", 12, False, False)
        self.blanco=(255,255,255)
        self.superficie_texto=self.fuente.render("Created by OGG, with PyGame and icons of Dan Wiersema", True, self.blanco)

        #Dimensiones de la pantalla
        self.ancho=1024
        self.alto=768

        self.superficie_tierra=4*3.14*6370
        #Posicion del ultimo planeta
        #Last planet position
        self.num_planetas=9

        #Iconos creados por DAN WIERSEMA
        #ICONS CREATED BY DAN WIERSEMA
        #http://www.danwiersema.com
        self.iconos=["Mercury.png", "Venus.png", "Earth.png", "Mars.png", "Jupiter.png",
                "Saturn.png", "Neptune.png", "Uranus.png", "Pluto.png"]

        self.nombre=["Mercurio", "Venus", "Tierra", "Marte", "Jupiter", "Saturno", "Neptuno", "Urano", "Pluton"]
        #Distancias al sol de los planetas en millones de km
        self.distancias_sol=[57.9, 108.2, 149.6, 227.9, 778.3, 1427, 2871, 4497, 5913]

        #Periodo de rotacion de los planetas en dias terrestres
        #Rotation period of the planets measured in Earth days
        self.periodo_rotacion=[87.96, 224.68, 365, 687, 11.862*365, 29.456*365, 84*365, 164*365, 247.7*365 ]

        #Masas de los planetas
        self.constante_masa=5.98e24
        self.masas=[0.06, 0.82, 1, 0.11, 318, 95.1, 14.6, 17.2, 0.002]


        self.imagen=[]
        self.rectangulo=[]
        self.angulo_planeta=[]
        self.incr_angulo=[]
        self.escala_velocidad=2
        self.distancias_tierra=[]
        #Todos los planetas empiezan en el mismo angulo
        #Cargamos las imagenes y los rectangulos de los planetas
        for i in range (0,  self.num_planetas):
            self.angulo_planeta.insert(i, 0.0)
            
            self.distancias_tierra.insert(i, abs(self.distancias_sol[i]-self.distancias_sol[2]))
            self.masas[i]=self.masas[i]*self.constante_masa


            self.centro=[self.ancho/2, self.alto/2]

            self.tam=(self.ancho, self.alto)

            #Color de la pantalla de fondo
            self.negro=(0,0,0)

            self.pantalla=pygame.display.set_mode(self.tam)


            #Posicion del sol
            self.sol=pygame.image.load("sol_1.png")
            self.rect_sol=self.sol.get_rect()
            self.rect_sol.centerx=self.ancho/2
            self.rect_sol.centery=self.alto/2


            #Cuidado, las distancias reales son enormes. Se dividen por esta escala
            #para que quepan en pantalla
            self.escala=9.5

            #Situamos el sol en pantalla
            self.pantalla.blit(self.sol, self.rect_sol)

            self.centro_x=self.ancho/2
            self.centro_y=self.alto/2
            #Todos los planetas van situados con respecto al sol
            self.offset_x_sol=self.centro_x
            self.offset_y_sol=self.centro_y

            self.numero_frame=0

            self.grabar=False

            self.superficie_pantalla=pygame.display.get_surface()
            self.blanco=(255,255,255)
            self.centro_pantalla=(int(self.centro_x), int(self.centro_y))
            #Cantidad de tiempo que pasa entre evento "Tecla pulsada"
            pygame.key.set_repeat(5)
            #Es necesario tener calculados inicialmente los angulos básicos
            self.actualizar_incrementos_angulo()
            self.cargar_imagenes_planetas()

    def cargar_imagenes_planetas(self):
        escala_imagen=self.escala*2048
        for i in range (0,  self.num_planetas):
            
            ruta=os.path.join("img", self.iconos[i])
            superficie_sin_escalar=pygame.image.load(ruta)
            superficie=pygame.transform.smoothscale(superficie_sin_escalar, (escala_imagen/512, escala_imagen/512))
            self.imagen.insert(i, superficie)
            self.rectangulo.insert(i, self.imagen[i].get_rect())

    #Regula la velocidad angular de los distintos cuerpos
    def actualizar_incrementos_angulo(self):
        for i in range (0,  self.num_planetas):
            self.incr_angulo.insert(i, self.escala_velocidad*math.pi*2 / self.periodo_rotacion[i])

    #Dada la distancia, nos devuelve las x y las y del planeta
    def get_xy(self, distancia,angulo):
        x=distancia* math.cos(angulo)
        y=distancia* math.sin(angulo)
        return (x,y)


    #Calcula la fuerza de atraccion
    def fuerza_atraccion(self, masa1, masa2, distancia):
        return (6.67e-11*masa1*masa2)/(distancia*distancia)

    #Distancia entre dos rectangulos
    def distancia (self, rect1, rect2):
        x1=rect1.centerx
        y1=rect1.centery
        
        x2=rect2.centerx
        y2=rect2.centery
        
        x_abs=abs(x1-x2)*abs(x1-x2)
        y_abs=abs(y1-y2)*abs(y1-y2)
        distancia=math.sqrt(x_abs+y_abs)
        return distancia

    def on_tecla_pulsada(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.key.key_code("S"):
                self.rect_sol.centery+=1
                self.offset_y_sol=self.offset_y_sol+1
                self.centro_y=self.centro_y+1
                self.centro_pantalla=(int(self.centro_x), int(self.centro_y))
                return
            if evento.key == pygame.key.key_code("W"):
                self.rect_sol.centery-=1
                self.offset_y_sol=self.offset_y_sol-1
                self.centro_y=self.centro_y-1
                self.centro_pantalla=(int(self.centro_x), int(self.centro_y))
                return
            if evento.key == pygame.key.key_code("A"):
                self.rect_sol.centerx-=1
                self.offset_x_sol=self.offset_x_sol-1
                self.centro_x=self.centro_x-1
                self.centro_pantalla=(int(self.centro_x), int(self.centro_y))
                return
            if evento.key == pygame.key.key_code("D"):
                self.rect_sol.centerx+=1
                self.offset_x_sol=self.offset_x_sol+1
                self.centro_x=self.centro_x+1
                self.centro_pantalla=(int(self.centro_x), int(self.centro_y))
                return
            if evento.key == pygame.K_DOWN:
                if self.escala>15.5:
                    return
                self.escala+=0.05
            if evento.key == pygame.K_UP:
                if self.escala<0.1:
                    return
                self.escala-=0.05
            if evento.key == pygame.K_LEFT:
                if self.escala_velocidad<0.1:
                    return 
                self.escala_velocidad-=0.05
                self.actualizar_incrementos_angulo()
                return
            if evento.key == pygame.K_RIGHT:
                if self.escala_velocidad>4:
                    return 
                self.escala_velocidad+=0.05
                self.actualizar_incrementos_angulo()
                return

    
    def animar(self):

        while 1:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    self.on_tecla_pulsada(evento)
                
            
            if self.angulo_planeta[8]>=6.28:
                sys.exit()
            self.pantalla.fill(self.negro)
            self.pantalla.blit (self.sol, self.rect_sol)
            
            self.fuerza_total=0
            #Resituamos los planetas y actualizamos sus angulos
            for i in range(0, self.num_planetas):
                (x_planeta, y_planeta)=self.get_xy(self.distancias_sol[i] / self.escala, self.angulo_planeta[i])
                self.rectangulo[i].centerx = x_planeta + self.offset_x_sol
                self.rectangulo[i].centery = y_planeta + self.offset_y_sol
                pygame.draw.circle(self.superficie_pantalla, self.blanco, self.centro_pantalla, int(self.distancias_sol[i]/self.escala),1)
                self.pantalla.blit (self.imagen[i], self.rectangulo[i])
                
                self.angulo_planeta[i]=self.angulo_planeta[i]+self.incr_angulo[i]
                if i!=2:
                    distancia_a_la_tierra=self.distancia(self.rectangulo[i],self.rectangulo[2])
                    fuerza_aux=self.fuerza_atraccion(self.masas[i], self.masas[2], distancia_a_la_tierra)
                    self.fuerza_total=self.fuerza_total+fuerza_aux
                if self.angulo_planeta[i]>6.28:
                    self.angulo_planeta[i]=0
                    
                
                #cad_fuerza=str(fuerza_total)
                #superficie_fuerza=fuente.render(cad_fuerza, True, blanco)
                #superficie_pantalla.blit(superficie_fuerza, (5, 20))
                #superficie_pantalla.blit(superficie_texto, (5, 5))
                if self.grabar==True:
                    #Preparamos el numero de frame    
                    cad_numero_frame=str(numero_frame)
                    cad_numero_alineado=cad_numero_frame.rjust(9, "0")
                
                    #Cargamos la pantalla
                    
                    pygame.image.save(self.superficie_pantalla, ".\\frames\\"+cad_numero_alineado+".jpg")
                    #Y despues de salvada se pasa al siguiente frame
                    numero_frame=numero_frame+1
            pygame.display.flip()
            
if __name__=="__main__":
    sistema=SistemaSolar()
    sistema.animar()