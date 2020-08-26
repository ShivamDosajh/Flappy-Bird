import pygame, sys, random

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 450))
    screen.blit(floor_surface, (floor_x_pos + dim[0], 450))

def create_pipe():
    random_pipe_height = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (dim[0]+ 80, random_pipe_height))
    top_pipe = pipe_surface.get_rect(midbottom = (dim[0]+ 80, random_pipe_height - 150))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2.5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom > dim[1]:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            #print('collision')
            return False

    if bird_rect.top < -50 or bird_rect.bottom >= 450:
        hit_sound.play()
        #print('collision')
        return False

    return True

def rotate_bird(bird):
    rotated_bird = pygame.transform.rotozoom(bird, -bird_movement*5, 1)
    return rotated_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (50, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, white)
        score_rect = score_surface.get_rect(center = (dim[0]/2, 50))
        screen.blit(score_surface, score_rect)
    if game_state== 'game_over':
        score_surface = game_font.render('Score: ' + str(int(score)), True, white)
        score_rect = score_surface.get_rect(center=(dim[0] / 2, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render('High Score:  ' +str(int(high_score)), True, white)
        high_score_rect = high_score_surface.get_rect(center=(dim[0] / 2, 420))
        screen.blit(high_score_surface, high_score_rect)


dim = (288,512)
white = (255,255,255)

pygame.mixer.pre_init(channels=1, buffer = 512)
pygame.init()
screen = pygame.display.set_mode(dim)
clock = pygame.time.Clock()
pygame.display.set_caption('Flappy Bird')

icon = pygame.image.load('assets/favicon.ico')
pygame.display.set_icon(icon)

game_font = pygame.font.Font('assets/04B_19.ttf', 20)

bg_surface = pygame.image.load('assets/sprites/background-day.png').convert()

floor_surface = pygame.image.load('assets/sprites/base.png').convert()
floor_x_pos = 0

bird_upflap = pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha()
bird_downflap = pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (50, dim[1]//2))


pipe_surface = pygame.image.load('assets/sprites/pipe-green.png')
pipe_list = []

game_over_surface = pygame.image.load('assets/sprites/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (dim[0]/2, dim[1]/2))

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_height = [200, 250, 300, 350,  400]

#Game Variables
gravity = 0.125
bird_movement = 0

game_active = False
score = 0
high_score = 0
score_sound_countdown = 120

flap_sound = pygame.mixer.Sound('assets/audio/wing.wav')
hit_sound = pygame.mixer.Sound('assets/audio/hit.wav')
score_sound = pygame.mixer.Sound('assets/audio/point.wav')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50, dim[1]//2)
                bird_movement = 0
                bird_movement -=6
                score = 0
                score_sound_countdown = 120
                flap_sound.play()
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
            #print(pipe_list)
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()
    screen.blit(bg_surface, (0,0))
    floor_x_pos -= 0.5

    if floor_x_pos < -dim[0]:
        floor_x_pos = 0
    if score > high_score:
        high_score = score

    if game_active:
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(rotate_bird(bird_surface), bird_rect)

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        game_active = check_collision(pipe_list)
        score += (1/120)
        score_display(game_state='main_game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 120
    else:
        score_display(game_state= 'game_over')
        screen.blit(game_over_surface, game_over_rect)


    draw_floor()

    pygame.display.update()
    clock.tick(120)