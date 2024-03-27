import pygame
import random
import time

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 1000, 800  
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Pygame Game")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 128)  

# Fuente para el texto
font = pygame.font.Font(None, 36)

# Tiempo del juego (en segundos)
game_time = 60  # 1 minuto
start_time = time.time()

# Texto de la tabla flotante
def draw_info_table(eliminated, time_left):
    info_surface = font.render(f"Eliminados: {eliminated} | Tiempo: {time_left:.1f}s", True, BLACK)
    info_rect = info_surface.get_rect(center=(WIDTH // 2, 50))
    screen.blit(info_surface, info_rect)

# Jugador (triángulo)
player_size = 30  
player_pos = [WIDTH // 2, HEIGHT // 2]
player_speed = 5
player_points = [
    (0, -player_size),
    (player_size, player_size),
    (-player_size, player_size)
]

# Enemigos (cuadrados)
enemy_size = 20  
num_enemies = 15
enemies = []
for _ in range(num_enemies):
    enemy_x = random.randint(0, WIDTH - enemy_size)
    enemy_y = random.randint(0, HEIGHT - enemy_size)
    enemies.append([enemy_x, enemy_y])

# Game Loop
running = True
eliminated_enemies = 0

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
    if keys[pygame.K_UP]:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += player_speed

    # Mantener al jugador dentro de los límites de la pantalla
    player_pos[0] = max(0, min(player_pos[0], WIDTH - player_size))
    player_pos[1] = max(0, min(player_pos[1], HEIGHT - player_size))

    # Verificar colisiones con enemigos
    for enemy in enemies[:]:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_size, enemy_size)
        player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
        if player_rect.colliderect(enemy_rect):
            enemies.remove(enemy)
            eliminated_enemies += 1

    # Dibujar al jugador (triángulo)
    pygame.draw.polygon(screen, RED, [(player_pos[0] + x, player_pos[1] + y) for x, y in player_points])

    # Dibujar enemigos restantes
    for enemy in enemies:
        pygame.draw.rect(screen, BLUE, (enemy[0], enemy[1], enemy_size, enemy_size))

    # Calcular tiempo restante
    current_time = time.time()
    time_left = max(0, game_time - (current_time - start_time))

    # Dibujar tabla de información
    draw_info_table(eliminated_enemies, time_left)

    pygame.display.update()

    # Terminar el juego si se eliminan todos los enemigos o se acaba el tiempo
    if eliminated_enemies == num_enemies or time_left <= 0:
        running = False

# Mostrar resultado final por 5 segundos
result_surface = font.render(f"Juego Terminado. Eliminados: {eliminated_enemies}", True, BLACK)
result_rect = result_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
screen.blit(result_surface, result_rect)
pygame.display.update()
pygame.time.delay(3000)  # 7 segundos de espera

pygame.quit()
