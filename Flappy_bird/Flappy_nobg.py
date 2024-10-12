import pygame, sys, random

def draw_ground(ground_x_pos):
  screen.blit(ground_surface, (ground_x_pos, 620))
  screen.blit(ground_surface, (ground_x_pos + 672, 620))
  screen.blit(ground_surface, (ground_x_pos + 336, 620)) 
def create_pipe():
    pipe_gap = 300
    rand_pipe_height = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700, rand_pipe_height))
    top_pipe = pipe_surface.get_rect(midbottom = (700, rand_pipe_height - pipe_gap))
    return bottom_pipe, top_pipe
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 1
    return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 720: #touching the bottom
             screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)
def check_crash(pipes):
    if bird_rect.top <= -100 or bird_rect.bottom >= 620:
        return False
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    return True
def score_display():
    global score
    score= int(score)
    if game_active:
        score_surface = game_font.render( str(score), True, (0,0,0))
        score_rect = score_surface.get_rect(center=(50,50))
        screen.blit(score_surface, score_rect)
    else:
        update_high_score()
       
def update_high_score():
    global score
    f = open("highScore.txt", "r")
    saved_score = int(f.read(-1))
    f.close()
    high_score_surface = game_font.render(f'High Score:  {str(saved_score)}', True, (0,0,0))
    score_rect = high_score_surface.get_rect(center=(150,50))
    screen.blit(high_score_surface, score_rect)
    if score > saved_score:
        f = open("highScore.txt", "w")
        score = int(score)
        f.write(str(score))
        f.close()
    
#INITIALIZATION
pygame.init()
pygame.display.set_caption("Pygame")
screen = pygame.display.set_mode([576,720])
clock = pygame.time.Clock()
game_active = False
game_font = pygame.font.Font('Assets/04B_19.TTF', 30)


#START / END
start_surface = pygame.image.load("Assets/message.png")
start_rect = start_surface.get_rect(center = screen.get_rect().center)
end_surface = pygame.image.load("Assets/gameover.png")
end_rect = end_surface.get_rect(center = screen.get_rect().center)
global score
score = 0
#BIRD
bird_surface = pygame.image.load("Assets/bluebird-midflap.png")
bird_rect = bird_surface.get_rect(center=(100, 450))
bird_pos_y = 200

#GROUND
ground_surface = pygame.image.load("Assets/base.png")
ground_x_pos = 0

#PIPES
pipe_surface = pygame.image.load("Assets/pipe-green.png")
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 500, 600 ] # set max heights
scored_pipes = []

while True:
    #CLEAR SCREEN
    screen.fill((255,255,255))
    
    if game_active:
        #BIRD
        bird_pos_y += 0.1
        bird_rect.centery = bird_pos_y
        screen.blit(bird_surface, bird_rect)
        game_active = check_crash(pipe_list)
        
        #PIPES
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
    else:
        #screen.blit(end_surface, (200, 300))
        screen.fill((255,255,255))
        screen.blit(start_surface, start_rect)

    #GROUND
    ground_x_pos -= 1
    draw_ground(ground_x_pos)
    if ground_x_pos <= -332:
        ground_x_pos= 0  

    for pipes in pipe_list:
        if pipes.centerx <= bird_rect.centerx and not pipes in scored_pipes:
            score += 0.5
            scored_pipes.append(pipes)
    score_display()
    for event in pygame.event.get():

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if  event.type == pygame.QUIT:
            pygame.quit()
            sys.exit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list = []
                scored_pipes = []
                score = 0
                bird_pos_y = 200

    pygame.display.update()
    clock.tick(120)
