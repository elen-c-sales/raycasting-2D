# /// script
# dependencies = [
#   "pygame",
# ]
# ///

import asyncio
import pygame
import math

# --- CONFIGURAÇÕES ---
WIDTH, HEIGHT = 900, 800
BG_COLOR = (5, 5, 8)
FLOOR_COLOR = (20, 20, 25)
LIGHT_COLOR = (255, 230, 200, 180) 
WALL_COLOR = (80, 80, 150) 
DOOR_COLOR_CLOSED = (101, 67, 33) # Marrom Madeira
DOOR_COLOR_OPEN = (50, 50, 50)    # Cinza escuro
TEXT_COLOR = (255, 255, 255)

# Raycasting & Movimento
FOV_DEG = 65
RAY_COUNT = 180
MAX_DIST = 700
MOVEMENT_THRESHOLD = 3.0
SMOOTH_SPEED = 0.15
WALL_THICKNESS = 5 # Nova configuração para espessura

# --- CLASSE PARA AS PORTAS ---
class Door:
    def __init__(self, x1, y1, x2, y2):
        self.start = pygame.Vector2(x1, y1)
        self.end = pygame.Vector2(x2, y2)
        self.is_open = False
        self.center = (self.start + self.end) / 2
        
    def get_obstacle(self):
        if not self.is_open:
            return [self.start, self.end]
        return None

    def draw(self, surface):
        if self.is_open:
            # Desenha batente fino
            pygame.draw.line(surface, DOOR_COLOR_OPEN, self.start, self.end, 2)
        else:
            # Desenha porta fechada grossa (mesma espessura da parede)
            pygame.draw.line(surface, DOOR_COLOR_CLOSED, self.start, self.end, WALL_THICKNESS)

# --- MAPA DEFINITIVO (Paredes recortadas + Aberturas permanentes) ---
walls = []

# 1. Estrutura Externa
walls.append([(100, 50), (400, 50)])   # Topo Esq
walls.append([(500, 50), (800, 50)])   # Topo Dir
walls.append([(100, 750), (480, 750)]) # Base Esq
walls.append([(520, 750), (800, 750)]) # Base Dir
walls.append([(100, 50), (100, 750)])  # Lateral Esq
walls.append([(800, 50), (800, 750)])  # Lateral Dir

# 2. Divisórias Horizontais
walls.append([(100, 250), (400, 250)]) # Salão Baile Esq
walls.append([(500, 250), (800, 250)]) # Salão Baile Dir
walls.append([(100, 450), (300, 450)]) # Cozinha Base
walls.append([(600, 450), (800, 450)]) # Corredor Central Base

# LINHA DO HALL (y=600) - AQUI ESTÁ A MUDANÇA DAS ABERTURAS
# Removemos as portas que ficavam entre 350-400 e 500-550.
# Agora são apenas buracos vazios entre os segmentos de parede.
walls.append([(100, 600), (250, 600)]) # Segmento 1
walls.append([(300, 600), (350, 600)]) # Segmento 2
# (Buraco 350-400: Abertura permanente Hall Esq)
# (Buraco 400-500: Parede do Vazio Central)
# (Buraco 500-550: Abertura permanente Hall Dir)
walls.append([(550, 600), (600, 600)]) # Segmento 3
walls.append([(650, 600), (800, 600)]) # Segmento 4

# 3. Paredes Verticais Internas
walls.append([(300, 250), (300, 500)]) # Vertical Esq Cima
walls.append([(300, 550), (300, 600)]) # Vertical Esq Baixo
walls.append([(600, 250), (600, 500)]) # Vertical Dir Cima
walls.append([(600, 550), (600, 600)]) # Vertical Dir Baixo

# 4. Vazio Central e Quartos
walls.append([(450, 450), (550, 450)]) # Vazio Topo
walls.append([(450, 600), (550, 600)]) # Vazio Base
walls.append([(450, 450), (450, 600)]) # Vazio Esq
walls.append([(550, 450), (550, 600)]) # Vazio Dir
walls.append([(250, 600), (250, 650)]) # Banheiro Cima
walls.append([(250, 700), (250, 750)]) # Banheiro Baixo
walls.append([(650, 600), (650, 650)]) # Escritório Cima
walls.append([(650, 700), (650, 750)]) # Escritório Baixo

# 5. Obstáculos (Mesa e Estantes)
walls.extend([
    [(150, 480), (250, 480)], [(150, 570), (250, 570)],
    [(150, 480), (150, 570)], [(250, 480), (250, 570)],
])
for x in range(630, 780, 40):
    walls.append([(x, 470), (x, 580)])

# --- OBJETOS PORTAS (Removidas as do Hall) ---
door_objects = [
    Door(480, 750, 520, 750), # Saída Rua
    Door(250, 650, 250, 700), # Banheiro
    Door(650, 650, 650, 700), # Escritório
    # REMOVIDAS AS DUAS PORTAS DO HALL AQUI
    Door(250, 600, 300, 600), # Jantar -> Sala
    Door(600, 600, 650, 600), # Biblio -> Sala
    Door(300, 500, 300, 550), # Jantar -> Cozinha
    Door(600, 500, 600, 550), # Biblio -> Corredor
    Door(400, 250, 500, 250), # Salão Baile
    Door(400, 50, 500, 50)    # Estufa
]

# --- FUNÇÕES ---

def lerp_angle(start, end, amount):
    diff = (end - start + math.pi) % (2 * math.pi) - math.pi
    return start + diff * amount

def cast_ray(origin, angle, obstacles):
    closest_point = None
    min_dist = MAX_DIST
    x1, y1 = origin
    x2 = x1 + math.cos(angle) * MAX_DIST
    y2 = y1 + math.sin(angle) * MAX_DIST

    for wall in obstacles:
        x3, y3 = wall[0]
        x4, y4 = wall[1]
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den == 0: continue
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
        if 0 < t < 1 and 0 < u < 1:
            pt_x = x1 + t * (x2 - x1)
            pt_y = y1 + t * (y2 - y1)
            dist = math.hypot(pt_x - x1, pt_y - y1)
            if dist < min_dist:
                min_dist = dist
                closest_point = (pt_x, pt_y)
    return closest_point if closest_point else (x2, y2)

def check_collision(pos, obstacles):
    player_radius = 6
    for wall in obstacles:
        x1, y1 = wall[0]
        x2, y2 = wall[1]
        dx, dy = x2 - x1, y2 - y1
        if dx == 0 and dy == 0: continue
        t = ((pos.x - x1) * dx + (pos.y - y1) * dy) / (dx*dx + dy*dy)
        t = max(0, min(1, t))
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy
        dist_sq = (pos.x - closest_x)**2 + (pos.y - closest_y)**2
        if dist_sq < player_radius**2:
            return True
    return False

async def main():
    print("Initializing Pygame...")
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Raycasting - Survival Horror")
    clock = pygame.time.Clock()
    
    # Use default font for better web compatibility
    font = pygame.font.Font(None, 24)
    print("Game initialized successfully!")
    
    player_pos = pygame.Vector2(500, 680)
    last_mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    current_angle = -math.pi / 2
    target_angle = -math.pi / 2
    speed = 3.5

    running = True
    while running:
        
        current_obstacles = list(walls)
        for door in door_objects:
            obs = door.get_obstacle()
            if obs:
                current_obstacles.append(obs)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    for door in door_objects:
                        if player_pos.distance_to(door.center) < 55:
                            door.is_open = not door.is_open

        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        if (mouse_pos - last_mouse_pos).length() > MOVEMENT_THRESHOLD:
            target_angle = math.atan2(mouse_pos.y - last_mouse_pos.y, mouse_pos.x - last_mouse_pos.x)
            last_mouse_pos = mouse_pos
        current_angle = lerp_angle(current_angle, target_angle, SMOOTH_SPEED)

        keys = pygame.key.get_pressed()
        move_vec = pygame.Vector2(0, 0)
        forward = pygame.Vector2(math.cos(current_angle), math.sin(current_angle))
        right = pygame.Vector2(math.cos(current_angle + math.pi/2), math.sin(current_angle + math.pi/2))

        if keys[pygame.K_w] or keys[pygame.K_UP]: move_vec += forward
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: move_vec -= forward
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: move_vec += right
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: move_vec -= right

        if move_vec.length() > 0:
            move_vec = move_vec.normalize() * speed
            if not check_collision(player_pos + pygame.Vector2(move_vec.x, 0), current_obstacles):
                player_pos.x += move_vec.x
            if not check_collision(player_pos + pygame.Vector2(0, move_vec.y), current_obstacles):
                player_pos.y += move_vec.y

        # --- DRAW ---
        screen.fill(BG_COLOR)
        
        # Raycasting
        light_points = [(player_pos.x, player_pos.y)]
        fov_rad = math.radians(FOV_DEG)
        start_ray = current_angle - fov_rad / 2
        step = fov_rad / RAY_COUNT
        
        for i in range(RAY_COUNT + 1):
            ang = start_ray + (i * step)
            hit = cast_ray((player_pos.x, player_pos.y), ang, current_obstacles)
            light_points.append(hit)
        light_points.append((player_pos.x, player_pos.y))
        
        light_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        if len(light_points) > 2:
            pygame.draw.polygon(light_surf, LIGHT_COLOR, light_points)
        screen.blit(light_surf, (0,0))
        
        # Desenha Paredes Fixas (MAIS GROSSAS AGORA)
        for wall in walls:
            pygame.draw.line(screen, WALL_COLOR, wall[0], wall[1], WALL_THICKNESS)
            
        # Desenha Portas
        door_nearby = False
        for door in door_objects:
            door.draw(screen)
            if player_pos.distance_to(door.center) < 55:
                door_nearby = True

        # Player
        pygame.draw.circle(screen, (200, 200, 200), (int(player_pos.x), int(player_pos.y)), 6)

        # UI
        if door_nearby:
            text_surf = font.render("[ENTER] Interagir", True, TEXT_COLOR)
            screen.blit(text_surf, (player_pos.x + 15, player_pos.y - 30))

        pygame.display.flip()
        clock.tick(60)
        
        # CRITICAL: yield control to browser
        await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
