import pygame, random, datetime, os, sys
from funcoes import limpar_tela, aguardarTempo, mensagem_vozinha, ouvir_comando

pygame.init()
clock = pygame.time.Clock()

# TELA
largura, altura = 1000, 700
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Hollow Knight - Caça às Almas")
fps = pygame.time.Clock()

# CORES
branco = (255, 255, 255)
preto = (0, 0, 0)
amarelo = (255, 255, 0)

fundo = pygame.image.load("Recursos/Personagens/imgs/imgs/fundohollowpixel.png").convert_alpha()
fundo = pygame.transform.scale(fundo, (largura, altura))
print(f"Fundo carregado: {fundo.get_width()}x{fundo.get_height()}")
# POSIÇÃO DO PERSONAGEM
personagem_x = largura // 2 - 50
largura_sprite = 150
altura_sprite = 180
personagem_x = max(0, min(largura - largura_sprite, personagem_x))

imagem_pulsante = pygame.image.load("Recursos/SolPulsante/voidheartpixel_circular_cropped.png").convert_alpha()
imagem_pulsante = pygame.transform.scale(imagem_pulsante, (80, 80))  # ajuste o tamanho conforme necessário
pulsar_valor = 1.0
pulsar_crescendo = True

personagem_y = altura - altura_sprite - 20
# FONTES
fonte = pygame.font.Font("Recursos/Fonte/UnifrakturCook-Bold.ttf", 32)


# SPRITES DE ANIMAÇÃO
def carregar_animacao(caminho_pasta, largura_sprite=50, altura_sprite=50):
    sprites = []
    for arquivo in sorted(os.listdir(caminho_pasta)):
        if arquivo.endswith(".png"):
            caminho = os.path.join(caminho_pasta, arquivo)
            try:
                img = pygame.image.load(caminho).convert_alpha()
                img = pygame.transform.scale(img, (largura_sprite, altura_sprite))
                sprites.append(img)
            except Exception as e:
                print(f"Erro ao carregar {caminho}: {e}")
    print(f"{len(sprites)} frames carregados de {caminho_pasta}")
    return sprites
animacao_direita = carregar_animacao("Recursos/Personagens/hollow_walk", largura_sprite, altura_sprite)
animacao_esquerda = carregar_animacao("Recursos/Personagens/hollow_walk_left", largura_sprite, altura_sprite)

def carregar_animacao_fogo(caminho_pasta, largura=30, altura=30):
    frames = []
    for arquivo in sorted(os.listdir(caminho_pasta)):
        if arquivo.endswith(".png"):
            img = pygame.image.load(os.path.join(caminho_pasta, arquivo)).convert_alpha()
            img = pygame.transform.scale(img, (largura, altura))
            frames.append(img)
    return frames

largura_alma = 80
altura_alma = 80
alma_animada_frames = carregar_animacao_fogo("Recursos/FogoAnimado", largura_alma, altura_alma)

def tela_inicial():
    nome = ""
    ativo = True
    input_ativo = False
    
    while ativo:
        imagem_capa = pygame.image.load("Recursos/Personagens/imgs/imgs/hollowpixelcapa.png").convert()
        imagem_capa = pygame.transform.scale(imagem_capa, (1000, 700))
        tela.blit(imagem_capa, (0, 0))

        # Regras reposicionadas mais à esquerda
        regras = [
            "Use as setas para mover o personagem (somente esquerda ou difeita)",
        ]
        for i, texto in enumerate(regras):
            regra_render = fonte.render(texto, True, branco)
            tela.blit(regra_render, (100, 420 + i * 30))

        input_box = pygame.Rect(largura // 2 - 150, 460, 300, 40)
        cor_input = branco if input_ativo else (180, 180, 180)
        pygame.draw.rect(tela, cor_input, input_box, 2)
        texto_nome = fonte.render(nome, True, branco)
        tela.blit(texto_nome, (input_box.x + 10, input_box.y + 5))

        instrucao = fonte.render("Digite seu nome e clique em Iniciar", True, branco)
        tela.blit(instrucao, (largura // 2 - instrucao.get_width() // 2, 510))

        # Botão Iniciar Jogo ajustado
        start_box = pygame.Rect(largura // 2 - 90, 550, 180, 50)
        pygame.draw.rect(tela, branco, start_box)
        start_text = fonte.render("Iniciar Jogo", True, preto)
        tela.blit(start_text, (start_box.x + 20, start_box.y + 10))

        # Botão Falar Comando ajustado
        botao_voz = pygame.Rect(largura // 2 - 90, 620, 180, 50)
        pygame.draw.rect(tela, branco, botao_voz)
        voz_text = fonte.render("      Voz", True, preto)
        tela.blit(voz_text, (botao_voz.x + 15, botao_voz.y + 10))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(evento.pos):
                    input_ativo = True
                else:
                    input_ativo = False

                if start_box.collidepoint(evento.pos) and nome.strip() != "":
                    mensagem_vozinha(nome)
                    return nome

                if botao_voz.collidepoint(evento.pos):
                    comando = ouvir_comando()
                    if comando:
                        if "iniciar" in comando and nome.strip() != "":
                            mensagem_vozinha(nome)
                            return nome
                        elif "sair" in comando:
                            pygame.quit()
                            quit()
            elif evento.type == pygame.KEYDOWN and input_ativo:
                if evento.key == pygame.K_RETURN:
                    mensagem_vozinha(nome)
                    return nome
                elif evento.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                else:
                    if len(nome) < 20:
                        nome += evento.unicode

        pygame.display.update()
        fps.tick(60)

def desenhar_cena(almas_desviadas, explosoes, explosao_frames):
    global almas

    # Fundo
    tela.blit(fundo, (0, 0))

    # Personagem
    tela.blit(frame_atual, (personagem_x, personagem_y))

    novas_almas = []
    novas_explosoes = []
    novas_desviadas = 0

    # Almas animadas + hitbox
    for alma in almas:
        alma[3] += 1
        if alma[3] >= 4:
            alma[2] = (alma[2] + 1) % len(alma_animada_frames)
            alma[3] = 0

        frame = alma[2]
        if 0 <= frame < len(alma_animada_frames):
            tela.blit(alma_animada_frames[frame], (alma[0], alma[1]))
        else:
            tela.blit(alma_animada_frames[0], (alma[0], alma[1]))

        # Remover alma se atingir a base do personagem
        if alma[1] >= personagem_y + altura_sprite - altura_alma:
            novas_explosoes.append([alma[0], personagem_y + altura_sprite - altura_alma, 0, 0])
            novas_desviadas += 1
        else:
            novas_almas.append(alma)

    almas[:] = novas_almas
    explosoes.extend(novas_explosoes)
    almas_desviadas += novas_desviadas

    # Explosões animadas
    for explosao in explosoes:
        if 0 <= explosao[2] < len(explosao_frames):
            tela.blit(explosao_frames[explosao[2]], (explosao[0], personagem_y + altura_sprite - altura_alma))

    # Pontuação (almas desviadas)
    texto = fonte.render(f"Desviadas: {almas_desviadas}", True, branco)
    tela.blit(texto, (20, 20))

    # Tela de pausa
    if pausado:
        texto_p = fonte.render("PAUSE", True, branco)
        tela.blit(texto_p, (largura // 2 - 50, altura // 2))

    pygame.display.update()

    return almas_desviadas

def jogar():
    global personagem_x, pausado, almas, tamanho_sol, direcao_sol
    global personagem_frame, tempo_animacao, frame_atual, animacao_atual
    global largura_alma, altura_alma, pulsar_crescendo, pulsar_valor
    pausado = False
    almas_desviadas = 0
    velocidade_alma = 4
    velocidade_maxima = 14
    intervalo_entre_almas = 2000
    tempo_inicial = pygame.time.get_ticks()
    tempo_ultimo_aumento = pygame.time.get_ticks()
    max_almas_na_tela = 1

    personagem_x = largura // 2 - largura_sprite // 2
    personagem_y = altura - altura_sprite - 20
    personagem_frame = 0
    tempo_animacao = 0
    frame_atual = animacao_direita[0]
    animacao_atual = animacao_direita

    # Carregar frames de explosão
    explosao_frames = []
    for i in range(6):
        frame = pygame.image.load(f"Recursos/Explosão/explosao_0{i}.png").convert_alpha()
        frame = pygame.transform.scale(frame, (80, 80))
        explosao_frames.append(frame)

    explosoes = []

    almas = []
    for _ in range(max_almas_na_tela):
        x = random.randint(0, largura - largura_alma)
        velocidade_lateral = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
        almas.append([x, -altura_alma, 0, 0, velocidade_lateral])

    rodando = True
    while rodando:
        agora = pygame.time.get_ticks()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if evento.key == pygame.K_SPACE:
                    pausado = not pausado

        if pausado:
            desenhar_cena(almas_desviadas, explosoes, explosao_frames)
            continue

        teclas = pygame.key.get_pressed()
        movendo = False

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            personagem_x -= 6
            animacao_atual = animacao_esquerda
            movendo = True
        elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            personagem_x += 6
            animacao_atual = animacao_direita
            movendo = True

        personagem_x = max(0, min(largura - largura_sprite, personagem_x))

        if movendo:
            tempo_animacao += 1
            if tempo_animacao >= 5:
                personagem_frame = (personagem_frame + 1) % len(animacao_atual)
                tempo_animacao = 0
        else:
            personagem_frame = 0

        frame_atual = animacao_atual[personagem_frame]

        # Dificuldade dinâmica
        if almas_desviadas >= 30:
            max_almas_na_tela = 6
        elif almas_desviadas >= 20:
            max_almas_na_tela = 5
        elif almas_desviadas >= 15:
            max_almas_na_tela = 4
        elif almas_desviadas >= 10:
            max_almas_na_tela = 3

        intervalo_entre_almas = max(500, 2000 - (almas_desviadas * 50))

        if agora - tempo_inicial >= intervalo_entre_almas:
            quantidade_para_gerar = max_almas_na_tela - len(almas)
            for _ in range(quantidade_para_gerar):
                x = random.randint(0, largura - largura_alma)
                velocidade_lateral = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
                almas.append([x, -altura_alma, 0, 0, velocidade_lateral])
            tempo_inicial = agora

        for alma in list(almas):
            velocidade = velocidade_alma + random.randint(-1, 2)
            alma[1] += max(velocidade, 1)
            alma[0] += alma[4]

            if alma[0] < 0 or alma[0] > largura - largura_alma:
                alma[4] *= -1

            if alma[1] > altura:
                explosoes.append([alma[0], altura - altura_alma, 0, 0])
                almas.remove(alma)
                almas_desviadas += 1

                if almas_desviadas % 3 == 0 and velocidade_alma < velocidade_maxima:
                    velocidade_alma += 1

                continue

            ret_alma = pygame.Rect(alma[0] + 25, alma[1] + 50, 30, 25)
            ret_personagem = pygame.Rect(personagem_x + 45, personagem_y + 40, 60, 110)

            if ret_alma.colliderect(ret_personagem):
                explosoes.append([alma[0], alma[1], 0, 0])
                salvar_log(almas_desviadas)
                tela_fim_jogo()

        for explosao in list(explosoes):
            explosao[3] += 1
            if explosao[3] >= 5:
                explosao[2] += 1
                explosao[3] = 0
            if explosao[2] >= len(explosao_frames):
                explosoes.remove(explosao)

        almas_desviadas = desenhar_cena(almas_desviadas, explosoes, explosao_frames)
        if pulsar_crescendo:
            pulsar_valor += 0.01
            if pulsar_valor >= 1.2:
                pulsar_crescendo = False
        else:
            pulsar_valor -= 0.01
            if pulsar_valor <= 0.8:
                pulsar_crescendo = True

        largura_img = int(80 * pulsar_valor)
        altura_img = int(80 * pulsar_valor)
        imagem_pulsada = pygame.transform.scale(imagem_pulsante, (largura_img, altura_img))
        tela.blit(imagem_pulsada, (largura - largura_img - 20, 20))
        pygame.display.update()
        clock.tick(60)

# VARIÁVEIS DO JOGO
almas = []
pontos = 0
pausado = False
tamanho_sol = 30
direcao_sol = 1


def salvar_log(pontos):
    with open("log.dat", "a") as f:
        agora = datetime.datetime.now()
        f.write(f"{pontos} pontos - {agora.strftime('%d/%m/%Y %H:%M:%S')}\n")

def tela_fim_jogo():
    ativo = True
    fonte_titulo = pygame.font.SysFont("comicsans", 50)
    try:
        with open("log.dat", "r") as f:
            linhas = f.readlines()
            ultimos_logs = linhas[-5:] if len(linhas) >= 5 else linhas
    except FileNotFoundError:
        ultimos_logs = ["Nenhum registro encontrado."]

    while ativo:
        tela.fill(preto)
        tela.blit(fundo, (0, 0))

        titulo = fonte_titulo.render("FIM DE JOGO", True, branco)
        tela.blit(titulo, (largura // 2 - titulo.get_width() // 2, 100))

        subtitulo = fonte.render("Últimos 5 registros:", True, branco)
        tela.blit(subtitulo, (largura // 2 - subtitulo.get_width() // 2, 180))

        for i, linha in enumerate(reversed(ultimos_logs)):
            texto_linha = fonte.render(linha.strip(), True, branco)
            tela.blit(texto_linha, (largura // 2 - texto_linha.get_width() // 2, 220 + i * 30))

        botao_sair = pygame.Rect(largura // 2 - 75, 500, 150, 50)
        pygame.draw.rect(tela, branco, botao_sair)
        texto_sair = fonte.render("Sair", True, preto)
        tela.blit(texto_sair, (botao_sair.x + 45, botao_sair.y + 10))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (evento.type == pygame.MOUSEBUTTONDOWN and botao_sair.collidepoint(evento.pos)):
                pygame.quit()
                quit()

        pygame.display.update()
        fps.tick(60)

# INICIAR JOGO
nome_jogador = tela_inicial()
jogar()
pygame.quit()
