# pylint: disable=no-member

import pygame
from funciones import mostrar_menu, mover_enemigos, manejar_disparos, verificar_colisiones

# Inicializar PyGame
pygame.init()

# Dimensiones de la ventana
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Invasores Espaciales")

# Colores
NEGRO = (0, 0, 0)

# Cargar imágenes
nave_img = pygame.image.load("assets/nave.png")
enemigo_img = pygame.image.load("assets/enemigo.png")
bala_img = pygame.image.load("assets/bala.png")
fondo_img = pygame.image.load("assets/fondo.png")

# Clase del jugador


class Nave:
    def __init__(self):
        self.x = ANCHO // 2
        self.y = ALTO - 70
        self.velocidad = 5
        self.balas = []

    def mover(self, teclas):
        if teclas[pygame.K_LEFT] and self.x > 0:
            self.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.x < ANCHO - nave_img.get_width():
            self.x += self.velocidad

    def disparar(self):
        nueva_bala = {"x": self.x + 20, "y": self.y - 20, "vel": 7}
        self.balas.append(nueva_bala)

    def dibujar(self, ventana):
        ventana.blit(nave_img, (self.x, self.y))
        for bala in self.balas:
            ventana.blit(bala_img, (bala["x"], bala["y"]))

# Ciclo principal


def main():
    reloj = pygame.time.Clock()
    nave = Nave()
    enemigos = []
    puntuacion = 0

    corriendo = True
    while corriendo:
        reloj.tick(60)
        VENTANA.blit(fondo_img, (0, 0))

        # Manejar eventos
        teclas = pygame.key.get_pressed()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                nave.disparar()

        nave.mover(teclas)
        manejar_disparos(nave.balas)
        mover_enemigos(enemigos, enemigo_img)
        puntuacion += verificar_colisiones(nave.balas, enemigos)

        # Dibujar elementos
        nave.dibujar(VENTANA)
        for enemigo in enemigos:
            VENTANA.blit(enemigo_img, (enemigo["x"], enemigo["y"]))

        # Verificar fin del juego
        if any(enemigo["y"] > ALTO for enemigo in enemigos):
            print("¡Juego terminado! Puntuación:", puntuacion)
            corriendo = False

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    mostrar_menu(VENTANA)
    main()
