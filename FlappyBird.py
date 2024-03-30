# (Modified) Original Code by 'Clear Code' @YouTube 

import pygame, sys, random

# pygame.mixer.pre_init(frequency= 44100, size = 16, channels = 1, buffer = 512)
pygame.init()

# Display Surface
screen = pygame.display.set_mode((600, 690))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF',40)

def draw_floor():
    screen.blit(floor_surface,(floor_x_position,600))
    screen.blit(floor_surface,(floor_x_position + 600,600))

def create_pipe():
    random_pipe_position = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_position))
    top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_position - 300))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 690:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 600:
        return False

    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-bird_movement*3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (300, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {(int(score))}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (300, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {(int(high_score))}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (300, 550))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

# Surfaces
bg_surface = pygame.image.load('background-day.png').convert()
bg_surface = pygame.transform.scale(bg_surface,(600, 690))

floor_surface = pygame.image.load('base.png').convert()
floor_surface = pygame.transform.scale(floor_surface,(600, 200))
floor_x_position = 0

bird_upflap = pygame.transform.scale(pygame.image.load('bluebird-upflap.png').convert_alpha(),(40,30))
bird_midflap = pygame.transform.scale(pygame.image.load('bluebird-midflap.png').convert_alpha(),(40,30))
bird_downflap = pygame.transform.scale(pygame.image.load('bluebird-downflap.png').convert_alpha(),(40,30))
bird_frames = [bird_upflap, bird_midflap, bird_downflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, 345))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 180)

pipe_surface = pygame.image.load('pipe-green.png')
pipe_surface = pygame.transform.scale(pipe_surface,(70,400))
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [300,500,700]

game_over_surface = pygame.transform.scale(pygame.image.load('gameover.png').convert_alpha(),(300, 90))
game_over_rect = game_over_surface.get_rect(center = (300, 345))

flap_sound = pygame.mixer.Sound('FlappyBirdSound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('FlappyBirdSound/sfx_die.wav')
score_sound = pygame.mixer.Sound('FlappyBirdSound/sfx_point.wav')
score_sound_countdown = 100

# Game Variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

# Game Loop
while True:
        for event in pygame.event.get():

        # To close out of the game
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bird_movement = 0
                    bird_movement -= 8
                    flap_sound.play()
                if event.key == pygame.K_SPACE and game_active == False:
                    game_active = True
                    pipe_list.clear()
                    bird_rect.center = (100, 345)
                    bird_movement = 0
                    score = 0

            if event.type == SPAWNPIPE:
                pipe_list.extend(create_pipe())
            
            if event.type == BIRDFLAP:
                if bird_index < 2:
                    bird_index += 1
                else:
                    bird_index = 0

                bird_surface, bird_rect = bird_animation()

        # Upload bg_surface
        screen.blit(bg_surface,(0,0))

        if game_active:
            # Bird
            bird_movement += gravity
            rotated_bird = rotate_bird(bird_surface)
            bird_rect.centery += bird_movement
            screen.blit(rotated_bird, bird_rect)
            game_active = check_collision(pipe_list)

            #Pipes 
            pipe_list = move_pipes(pipe_list)
            draw_pipes(pipe_list)

            # Score
            score += 0.01
            score_display('main_game')
            score_sound_countdown -= 1
            if score_sound_countdown <= 0:
                score_sound.play()
                score_sound_countdown = 100

        else:
            screen.blit(game_over_surface, game_over_rect)
            high_score = update_score(score, high_score)
            score_display('game_over')
            
        # Floor
        floor_x_position -= 1
        draw_floor()
        if floor_x_position <= -600:
            floor_x_position = 0
        screen.blit(floor_surface,(floor_x_position,600))

        pygame.display.update()
        clock.tick(120) # FPS
