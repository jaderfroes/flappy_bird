import pygame  # https://www.pygame.org/docs/
from pygame.locals import *  # inclue só as constanstes do pygame

# Info da tela 
SCREEN_WIDTH = 400  # tupla (WIDTH, HEIGHT)
SCREEN_HEIGHT = 700
SPEED = 10
GRAVITY = 1

class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # construtor internas da classe sprite

        # convert_alpha detecta o contorno do png do passaro para detecções
        self.images = [pygame.image.load('sprites/redbird-upflap.png').convert_alpha(),
                       pygame.image.load('sprites/redbird-midflap.png').convert_alpha(),
                       pygame.image.load('sprites/redbird-downflap.png').convert_alpha()]  # lista de sprites 
        self.current_image = 0
        self.image = pygame.image.load('sprites/redbird-upflap.png').convert_alpha()  # imagem mostrada
        self.rect = self.image.get_rect() # bordas do passaro - tupla de 4 elementos
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

    def bump(self):
        self.speed = -SPEED


pygame.init()  # inicializa os módulos importados
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # cria a tela

BACKGROUND = pygame.image.load('sprites/background-night.png')  # carrega a imagem
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))  # adequa ao tamanho da screen definida

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

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
    # coloca o background na tela - param 2 posicao do canto esq da imagem na tela
    bird_group.update()
    bird_group.draw(screen)  # desenha todos elementos do grupo
    pygame.display.update()  # faz update das acoes ocorridas no laco
