# pylint: disable=no-member

import pygame
import random

pygame.init()

# Configuraciones de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Shooter")

# Cargar imágenes
spaceship_image = pygame.image.load("assets/nave.png")
enemy_image = pygame.image.load("assets/enemigo.png")
bullet_image = pygame.image.load("assets/bala.png")
background_image = pygame.image.load("assets/fondo.png")

screen_width = 800  # Ancho de la ventana del juego
screen_height = 600  # Alto de la ventana del juego
background_image = pygame.transform.scale(
    background_image, (screen_width, screen_height))

# Posiciones iniciales
spaceship_position = [screen_width // 2, screen_height - 100]
bullets = []
enemies = []
enemy_spawn_time = 150
game_over = False

# Función de Game Over


def game_over_menu():
    font = pygame.font.SysFont("Arial", 30)
    text = font.render(
        "Perdiste! Presiona R para reiniciar o Q para salir", True, (255, 0, 0))
    screen.blit(text, (250, 300))
    pygame.display.flip()


# Bucle del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Crear una nueva bala
                bullets.append(
                    [spaceship_position[0] + 25, spaceship_position[1]])

    if game_over:
        game_over_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reiniciar
                    # Reiniciar posición de la nave
                    spaceship_position = [
                        screen_width // 2, screen_height - 100]
                    bullets.clear()  # Limpiar las balas
                    enemies.clear()  # Limpiar los enemigos
                    game_over = False  # Ocultar la pantalla de Game Over
                    enemy_spawn_time = 150  # Reiniciar el tiempo de aparición de enemigos
                elif event.key == pygame.K_q:  # Cerrar
                    running = False
        continue

    # Limpiar la pantalla
    screen.fill((0, 0, 0))  # Fondo negro o puedes usar tu imagen de fondo
    screen.blit(background_image, (0, 0))

    # Mover la nave (disminuir la velocidad)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and spaceship_position[0] > 0:
        spaceship_position[0] -= 3  # Reduce la velocidad de la nave
    if keys[pygame.K_RIGHT] and spaceship_position[0] < screen_width - 50:
        spaceship_position[0] += 3  # Reduce la velocidad de la nave

    # Mover las balas
    for bullet in bullets[:]:
        bullet[1] -= 5
        if bullet[1] < 0:
            bullets.remove(bullet)

    # Detectar colisiones entre balas y enemigos
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet[0] < enemy[0] + 50 and bullet[0] + 20 > enemy[0] and bullet[1] < enemy[1] + 50 and bullet[1] + 20 > enemy[1]:
                enemies.remove(enemy)  # Eliminar el enemigo
                bullets.remove(bullet)  # Eliminar la bala
                break

    # Generar enemigos con un intervalo más largo
    if enemy_spawn_time <= 0:
        if len(enemies) < 10:  # Limitar la cantidad de enemigos en la pantalla
            enemies.append([random.randint(0, screen_width - 50), 0])
        enemy_spawn_time = 150
    else:
        enemy_spawn_time -= 1

    # Mover enemigos más despacio
    for enemy in enemies[:]:
        enemy[1] += 0.2  # Disminuye la velocidad de caída de los enemigos
        if enemy[1] > screen_height:
            enemies.remove(enemy)

    # Detectar colisiones entre la nave y los enemigos
    for enemy in enemies[:]:
        if spaceship_position[0] < enemy[0] + 50 and spaceship_position[0] + 50 > enemy[0] and spaceship_position[1] < enemy[1] + 50 and spaceship_position[1] + 50 > enemy[1]:
            game_over = True
            break

    # Dibujar la nave, las balas y los enemigos
    screen.blit(spaceship_image, spaceship_position)
    for bullet in bullets:
        screen.blit(bullet_image, bullet)
    for enemy in enemies:
        screen.blit(enemy_image, enemy)

    pygame.display.flip()  # Actualizar la pantalla

pygame.quit()
