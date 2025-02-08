import pygame
import time
import random

# Inicializa o pygame
pygame.init()

# Carregar sons
comer_som = pygame.mixer.Sound("comer.wav")
game_over_som = pygame.mixer.Sound("game_over.wav")

# Definições de cores
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
yellow = (255, 255, 0)
purple = (128, 0, 128)
orange = (255, 165, 0)
pink = (255, 192, 203)  # Cor para o power-up de invencibilidade

# Configurações da tela
width = 800
height = 800
block_size = 10
speed = 15
default_speed = speed  # Define a velocidade padrão

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Jogo da Cobra")

clock = pygame.time.Clock()
font = pygame.font.SysFont("bahnschrift", 25)
menu_font = pygame.font.SysFont("bahnschrift", 50)

# Skins para a cobra (cores diferentes)
skins = [
    {"name": "Preta", "color": black},
    {"name": "Vermelha", "color": red},
    {"name": "Verde", "color": green},
    {"name": "Azul", "color": blue},
    {"name": "Roxa", "color": purple},
    {"name": "Laranja", "color": orange}
]
current_skin_index = 0  # Índice da skin atual

def draw_snake(block_size, snake_list, skin_color):
    for block in snake_list:
        pygame.draw.rect(screen, skin_color, [block[0], block[1], block_size, block_size])

def show_score(score):
    value = font.render(f"Score: {score}", True, red)
    screen.blit(value, [10, 10])

def show_power_up_timers(power_up_start_time, power_up_duration):
    current_time = pygame.time.get_ticks()
    y_offset = 40  # Posição vertical inicial para os textos dos power-ups
    for power, start_time in power_up_start_time.items():
        if start_time > 0:
            time_left = max(0, power_up_duration - (current_time - start_time)) // 1000  # Tempo restante em segundos
            timer_text = font.render(f"{power}: {time_left}s", True, red)
            screen.blit(timer_text, [10, y_offset])
            y_offset += 30  # Ajusta a posição vertical para o próximo power-up

def spawn_power_up():
    # Escolhe um power-up aleatório para aparecer
    power_up_types = ["Turbo Boost 🚀", "Crescimento Duplo 🌟", "Encolhimento 🌀", "Invencibilidade 🛡️"]
    chosen_power = random.choice(power_up_types)
    power_up_x = round(random.randrange(0, width - block_size) / 10.0) * 10.0
    power_up_y = round(random.randrange(0, height - block_size) / 10.0) * 10.0
    return {chosen_power: [power_up_x, power_up_y]}

def draw_menu(selected_skin_index):
    screen.fill(white)
    title = menu_font.render("Selecione a Skin da Cobra", True, black)
    screen.blit(title, [width / 2 - title.get_width() / 2, 100])
    
    for i, skin in enumerate(skins):
        color = skin["color"]
        name = skin["name"]
        text = menu_font.render(name, True, color)
        x = width / 2 - text.get_width() / 2
        y = 200 + i * 60
        if i == selected_skin_index:
            pygame.draw.rect(screen, black, [x - 10, y - 10, text.get_width() + 20, text.get_height() + 20], 3)
        screen.blit(text, [x, y])
    
    instruction = font.render("Pressione ENTER para iniciar o jogo", True, black)
    screen.blit(instruction, [width / 2 - instruction.get_width() / 2, height - 100])
    pygame.display.update()

def game_loop():
    global speed, current_skin_index
    
    game_over = False
    game_close = False
    
    x = width / 2
    y = height / 2
    dx = 0
    dy = 0
    
    snake_list = []
    snake_length = 1
    
    food_x = round(random.randrange(0, width - block_size) / 10.0) * 10.0
    food_y = round(random.randrange(0, height - block_size) / 10.0) * 10.0
    
    # Power-ups
    power_ups = {}  # Inicialmente sem power-ups
    power_up_colors = {
        "Turbo Boost 🚀": yellow,
        "Crescimento Duplo 🌟": purple,
        "Encolhimento 🌀": orange,
        "Invencibilidade 🛡️": pink
    }
    
    power_up_start_time = {
        "Turbo Boost 🚀": 0,
        "Crescimento Duplo 🌟": 0,
        "Encolhimento 🌀": 0,
        "Invencibilidade 🛡️": 0
    }
    
    power_up_duration = 10000  # Duração dos power-ups em milissegundos (10 segundos)
    invincible = False  # Estado de invencibilidade
    fruits_eaten_since_last_power_up = 0  # Contador de frutas comidas
    power_up_spawn_interval = 3  # Número de frutas comidas para spawnar um power-up
    
    while not game_over:
        while game_close:
            screen.fill(white)
            message = font.render("Você perdeu! Pressione Q para sair ou R para reiniciar", True, red)
            screen.blit(message, [width / 6, height / 3])
            pygame.display.update()
            
            pygame.mixer.Sound.play(game_over_som)
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        game_loop()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -block_size
                    dy = 0
                elif event.key == pygame.K_RIGHT:
                    dx = block_size
                    dy = 0
                elif event.key == pygame.K_UP:
                    dy = -block_size
                    dx = 0
                elif event.key == pygame.K_DOWN:
                    dy = block_size
                    dx = 0
        
        x += dx
        y += dy
        screen.fill(blue)
        pygame.draw.rect(screen, green, [food_x, food_y, block_size, block_size])
        
        snake_head = [x, y]
        snake_list.append(snake_head)
        
        if len(snake_list) > snake_length:
            del snake_list[0]
        
        # Verifica se a cobra bateu nela mesma (a menos que esteja invencível)
        if not invincible:
            for segment in snake_list[:-1]:
                if segment == snake_head:
                    game_close = True
        
        draw_snake(block_size, snake_list, skins[current_skin_index]["color"])  # Desenha a cobra com a skin atual
        show_score(snake_length - 1)
        show_power_up_timers(power_up_start_time, power_up_duration)  # Mostra o tempo restante dos power-ups
        
        # Desenha os power-ups na tela
        for power, pos in power_ups.items():
            if pos:
                pygame.draw.rect(screen, power_up_colors[power], [pos[0], pos[1], block_size, block_size])
        
        pygame.display.update()
        
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, width - block_size) / 10.0) * 10.0
            food_y = round(random.randrange(0, height - block_size) / 10.0) * 10.0
            if power_up_start_time["Crescimento Duplo 🌟"] > 0:  # Verifica se o power-up de crescimento duplo está ativo
                snake_length += 2
            else:
                snake_length += 1
            pygame.mixer.Sound.play(comer_som)
            
            # Contador de frutas comidas
            fruits_eaten_since_last_power_up += 1
            if fruits_eaten_since_last_power_up >= power_up_spawn_interval:
                power_ups.update(spawn_power_up())  # Spawna um novo power-up
                fruits_eaten_since_last_power_up = 0  # Reseta o contador
        
        # Verifica se o power-up foi coletado
        for power, pos in power_ups.items():
            if pos:
                if x == pos[0] and y == pos[1]:
                    power_ups[power] = None  # Remove o power-up coletado
                    if power == "Turbo Boost 🚀":
                        speed += 5
                        power_up_start_time["Turbo Boost 🚀"] = pygame.time.get_ticks()  # Reinicia o tempo
                    elif power == "Crescimento Duplo 🌟":
                        power_up_start_time["Crescimento Duplo 🌟"] = pygame.time.get_ticks()
                    elif power == "Encolhimento 🌀":
                        snake_length = max(1, snake_length - 2)
                        power_up_start_time["Encolhimento 🌀"] = pygame.time.get_ticks()
                    elif power == "Invencibilidade 🛡️":
                        invincible = True
                        power_up_start_time["Invencibilidade 🛡️"] = pygame.time.get_ticks()
        
        # Verifica se algum power-up expirou
        current_time = pygame.time.get_ticks()
        for power in power_up_start_time:
            if power_up_start_time[power] > 0 and current_time - power_up_start_time[power] > power_up_duration:
                if power == "Turbo Boost 🚀":
                    speed = default_speed  # Retorna à velocidade padrão
                elif power == "Invencibilidade 🛡️":
                    invincible = False  # Desativa a invencibilidade
                power_up_start_time[power] = 0  # Reseta o tempo do power-up
        
        # Verifica se a cobra bateu na parede, mas não termina o jogo
        if x >= width or x < 0 or y >= height or y < 0:
            # Faz a cobra aparecer do outro lado da tela
            if x >= width:
                x = 0
            elif x < 0:
                x = width - block_size
            if y >= height:
                y = 0
            elif y < 0:
                y = height - block_size
        
        clock.tick(speed)
    
    pygame.quit()
    quit()

def main_menu():
    global current_skin_index
    in_menu = True
    while in_menu:
        draw_menu(current_skin_index)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  # Seleciona a skin anterior
                    current_skin_index = (current_skin_index - 1) % len(skins)
                elif event.key == pygame.K_DOWN:  # Seleciona a próxima skin
                    current_skin_index = (current_skin_index + 1) % len(skins)
                elif event.key == pygame.K_RETURN:  # Inicia o jogo
                    in_menu = False
                    game_loop()

main_menu()