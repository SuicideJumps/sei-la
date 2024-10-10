import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()

pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.load('leappad3-menu-music.mp3')
pygame.mixer.music.play(-1)
barulho_colisao = pygame.mixer.Sound('subway-surfers-coin-collect.wav')
barulho_colisao.set_volume(0.5)

largura = 640
altura = 480
x_cobra = largura / 2
y_cobra = altura / 2
velocidade = 20
points = 0
comprimento_inicial = 5

x_maca = randint(40, 600)
y_maca = randint(40, 400)

x_cobra_amarela = randint(40, 600)
y_cobra_amarela = randint(40, 400)
velocidade_amarela = 5
direcao_amarela = randint(1, 4)

fonte = pygame.font.SysFont('arial', 20, True, True)

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Training to Make Game')

relogio = pygame.time.Clock()

lista_cobra = [[x_cobra, y_cobra]]


def aumenta_cobra(lista_cobra):
    for XeY in lista_cobra:
        pygame.draw.rect(tela, (0, 100, 100), (XeY[0], XeY[1], 20, 20))


def game_over():
    font_game_over = pygame.font.SysFont('arial', 15, True, True)
    mensagem_game_over = 'Game Over! Pressione R para recomeçar ou Q para sair'
    texto_formatado = font_game_over.render(mensagem_game_over, True, (0, 0, 0))
    ret_texto = texto_formatado.get_rect(center=(largura // 2, altura // 2))

    while True:
        tela.fill((0, 60, 0))
        tela.blit(texto_formatado, ret_texto)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    return True
                if event.key == K_q:
                    pygame.quit()
                    exit()


def move_cobra_amarela():
    global x_cobra_amarela, y_cobra_amarela, direcao_amarela
    movimentos = [1, 2, 3, 4]
    if direcao_amarela == 1:
        x_cobra_amarela -= velocidade_amarela
    elif direcao_amarela == 2:
        x_cobra_amarela += velocidade_amarela
    elif direcao_amarela == 3:
        y_cobra_amarela -= velocidade_amarela
    elif direcao_amarela == 4:
        y_cobra_amarela += velocidade_amarela

    if x_cobra_amarela < 0 or x_cobra_amarela + 20 > largura or y_cobra_amarela < 0 or y_cobra_amarela + 20 > altura:
        direcao_amarela = randint(1, 4)
    else:
        if randint(0, 9) == 0:
            direcao_amarela = randint(1, 4)


direcao = 'RIGHT'
jogando = True

while True:
    while jogando:
        relogio.tick(20)
        tela.fill((0, 0, 0))

        mensagem = f'Points: {points}'
        texto_formatado = fonte.render(mensagem, True, (0, 0, 0))
        tela.blit(texto_formatado, (450, 40))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_a and direcao != 'RIGHT':
                    direcao = 'LEFT'
                elif event.key == K_d and direcao != 'LEFT':
                    direcao = 'RIGHT'
                elif event.key == K_w and direcao != 'DOWN':
                    direcao = 'UP'
                elif event.key == K_s and direcao != 'UP':
                    direcao = 'DOWN'

        if direcao == 'LEFT':
            x_cobra -= velocidade
        if direcao == 'RIGHT':
            x_cobra += velocidade
        if direcao == 'UP':
            y_cobra -= velocidade
        if direcao == 'DOWN':
            y_cobra += velocidade

        cobra = pygame.draw.rect(tela, (0, 100, 100), (x_cobra, y_cobra, 20, 20))
        maca = pygame.draw.rect(tela, (255, 0, 0), (x_maca, y_maca, 20, 20))
        cobra_amarela = pygame.draw.rect(tela, (255, 255, 0), (x_cobra_amarela, y_cobra_amarela, 20, 20))

        if cobra.colliderect(maca):
            x_maca = randint(40, 600)
            y_maca = randint(40, 400)
            points += 1
            velocidade += 0.5
            barulho_colisao.play()

        if cobra.colliderect(cobra_amarela):
            jogando = False

        lista_cabeca = [x_cobra, y_cobra]
        lista_cobra.append(lista_cabeca)
        if len(lista_cobra) > points + comprimento_inicial:
            del lista_cobra[0]

        move_cobra_amarela()

        # Verifica se a cobra bateu nas paredes
        if x_cobra < 0 or x_cobra >= largura or y_cobra < 0 or y_cobra >= altura:
            jogando = False

        # Verifica se a cobra bateu nela mesma
        if lista_cobra.count(lista_cabeca) > 1:
            jogando = False

        aumenta_cobra(lista_cobra)
        pygame.display.update()

    if not jogando:
        if game_over():
            x_cobra = largura / 2
            y_cobra = altura / 2
            points = 0
            velocidade = 20
            lista_cobra = [[x_cobra, y_cobra]]
            direcao = 'RIGHT'
            x_maca = randint(40, 600)
            y_maca = randint(40, 400)
            x_cobra_amarela = randint(40, 600)
            y_cobra_amarela = randint(40, 400)
            direcao_amarela = randint(1, 4)
            jogando = True


