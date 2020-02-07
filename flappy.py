import pygame  # https://www.pygame.org/docs/
from pygame.locals import *  # inclue só as constanstes do pygame
import random

# Info da tela 
SCREEN_WIDTH = 400  # tupla (WIDTH, HEIGHT)
SCREEN_HEIGHT = 700
SPEED = 10
GRAVITY = 1

GAME_SPEED = 10

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

PIPE_WIDTH = 100
PIPE_HEIGHT = 500
PIPE_GAP = 200 # Espacos entre os canos


class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # construtor interno da classe sprite

        # convert_alpha detecta o contorno do png do passaro para detecções
        self.images = [pygame.image.load('sprites/redbird-upflap.png').convert_alpha(),
                       pygame.image.load('sprites/redbird-midflap.png').convert_alpha(),
                       pygame.image.load('sprites/redbird-downflap.png').convert_alpha()]  # lista de sprites 
        self.current_image = 0
        self.image = pygame.image.load('sprites/redbird-upflap.png').convert_alpha()  # imagem mostrada
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()  # bordas do passaro - tupla de 4 el
        self.rect[0] = SCREEN_WIDTH / 2  # x do canto superior esq do passaro
        self.rect[1] = SCREEN_HEIGHT / 2  # y do passaro

        self.speed = SPEED

        print(self.rect)

    def update(self):
        self.current_image = (self.current_image + 1) % len(self.images)
        self.image = self.images[self.current_image]
        self.speed += GRAVITY
        # Update height
        self.rect[1] += self.speed  # queda do passaro

    def bump(self):  # salto para cima
        self.speed = -SPEED

class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        '''@param self, flag para identificar superior e inferior, posicao do cano, tamanho do cano'''
        pygame.sprite.Sprite.__init__(self)  # init

        self.image = pygame.image.load('sprites/pipe-green.png')
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True) # inverte o sprite
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED

class Ground(pygame.sprite.Sprite):
    ''' classe que especifica o chão do jogo'''

    def __init__(self, x_pos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("sprites/base.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()  # retangulo
        self.rect[0] = x_pos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self):
        self.rect[0] -= GAME_SPEED


def is_off_screen(sprite):
    '''verifica se o sprite esta fora da tela'''
    return sprite.rect[0] < (-sprite.rect[2])  # rect[2] - largura do sprite

def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)

    return (pipe, pipe_inverted)


pygame.init()  # inicializa os módulos importados
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # cria a tela

BACKGROUND = pygame.image.load('sprites/background-night.png')  # carrega a img
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))  # adequa ao tamanho da screen definida

# grupo do passaro
bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

# grupo do chao
ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(i * GROUND_WIDTH)
    ground_group.add(ground)

# grupo do cano
pipe_group = pygame.sprite.Group()
for i in range(2):  # só 2 grupos
    pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
    pipe_group.add(pipes[0])  # cano de baixo e de cima
    pipe_group.add(pipes[1])

clock = pygame.time.Clock()

while True:  # laço principal
    clock.tick(30)  # fps 
    for event in pygame.event.get():  # eventos do usuário
        if event.type == QUIT:  # se usuario sai 
            pygame.quit()

        if event.type == KEYDOWN:  # tecla pressionada
            if event.key == K_SPACE:
                bird.bump()

    screen.blit(BACKGROUND, (0, 0))  

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])
        new_ground = Ground(GROUND_WIDTH - 20) # 20 para não ficar espaço entre os sprites
        ground_group.add(new_ground)

    if is_off_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0]) # remove o de baixo
        pipe_group.remove(pipe_group.sprites()[0]) # remove o de cima(que era o 0 atual)

        pipes = get_random_pipes(SCREEN_WIDTH * 2)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])
        
    # coloca o background na tela - param 2 posicao do canto esq da imagem na tela
    bird_group.update()
    ground_group.update()
    pipe_group.update()

    bird_group.draw(screen)  # desenha todos elementos do grupo
    pipe_group.draw(screen)
    ground_group.draw(screen)
    

    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
       pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        # Game Over
        break

    pygame.display.update()  # faz update das acoes ocorridas no laco
