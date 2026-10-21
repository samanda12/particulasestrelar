
import pygame
import random
import math
import numpy as np
import imageio.v2 as imageio

from PIL import Image
from pathlib import Path

pygame.init()


LARGURA, ALTURA = 1000, 750
FPS = 30
DURACAO = 15
TOTAL_FRAMES = FPS * DURACAO

FUNDO = (2, 7, 15)
VERDE = (0, 255, 145)
ROSA = (0, 210, 255)

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Anne - Cyber Dev")

relogio = pygame.time.Clock()
pasta = Path(__file__).resolve().parent

fonte_codigo = pygame.font.SysFont(
    "consolas", 12, bold=True
)

fonte_fundo = pygame.font.SysFont(
    "consolas", 15
)

fonte_titulo = pygame.font.SysFont(
    "consolas", 30, bold=True
)


imagem = Image.open(
    pasta / "fotoanne.png"
).convert("RGBA")

imagem.thumbnail((490, 560))

offset_x = (LARGURA - imagem.width) // 2
offset_y = (ALTURA - imagem.height) // 2


simbolos = "01{}[]<>/#@$"

particulas = []
PASSO = 6

for y in range(0, imagem.height, PASSO):
    for x in range(0, imagem.width, PASSO):

        r, g, b, a = imagem.getpixel((x, y))

        if a > 100:
            luminosidade = (r + g + b) / 3

            # Preserva contraste da imagem
            intensidade = int(
                100 + luminosidade * 0.6
            )

            intensidade = min(255, intensidade)

            cor = (
                0,
                intensidade,
                min(255, intensidade + 35)
            )

            caractere = random.choice(simbolos)

            superficie = fonte_codigo.render(
                caractere, True, cor
            )

            particulas.append({
                "x": random.uniform(0, LARGURA),
                "y": random.uniform(0, ALTURA),
                "dx": x + offset_x,
                "dy": y + offset_y,
                "fase": random.uniform(0, math.tau),
                "vel": random.uniform(0.7, 1.3),
                "imagem": superficie
            })

print("Caracteres criados:", len(particulas))


colunas = []

for x in range(0, LARGURA, 22):
    colunas.append({
        "x": x,
        "y": random.uniform(-ALTURA, ALTURA),
        "vel": random.uniform(45, 125),
        "simbolo": random.choice("01<>")
    })


def explodir():
    for p in particulas:
        angulo = random.uniform(0, math.tau)
        distancia = random.uniform(150, 550)

        p["x"] = p["dx"] + math.cos(angulo) * distancia
        p["y"] = p["dy"] + math.sin(angulo) * distancia



saida = pasta / "Anne_Cyber_Dev.mp4"

gravador = imageio.get_writer(
    str(saida),
    fps=FPS,
    codec="libx264",
    quality=8,
    macro_block_size=2
)

try:
    for frame in range(TOTAL_FRAMES):

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                raise KeyboardInterrupt

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    raise KeyboardInterrupt

        tempo = frame / FPS

        
        if frame == 7 * FPS:
            explodir()

        tela.fill(FUNDO)

       
        for coluna in colunas:
            coluna["y"] += coluna["vel"] / FPS

            if coluna["y"] > ALTURA + 40:
                coluna["y"] = random.uniform(-300, -20)
                coluna["simbolo"] = random.choice("01<>")

            texto = fonte_fundo.render(
                coluna["simbolo"],
                True,
                (0, 65, 55)
            )

            tela.blit(
                texto,
                (coluna["x"], int(coluna["y"]))
            )

        
        for p in particulas:

            flutuar_x = math.sin(
              
                tempo * p["vel"] + p["fase"]
            ) * 1.5

            flutuar_y = math.cos(
                tempo * p["vel"] + p["fase"]
            ) * 1.5

            destino_x = p["dx"] + flutuar_x
            destino_y = p["dy"] + flutuar_y

            p["x"] += (destino_x - p["x"]) * 0.06
            p["y"] += (destino_y - p["y"]) * 0.06

            tela.blit(
                p["imagem"],
                (int(p["x"]), int(p["y"]))
            )

       
        terminal = fonte_fundo.render(
            ">>> rendering anne.py ...",
            True,
            VERDE
        )

        tela.blit(terminal, (25, 25))

        status = fonte_fundo.render(
            f"FRAME {frame:04d} | PYTHON | CYBER DEV",
            True,
            (0, 150, 170)
        )

        tela.blit(status, (25, 50))

        if tempo >= 11:

            mensagem = fonte_titulo.render(
                "LITTLE STAR",
                True,
                ROSA
            )

            posicao = mensagem.get_rect(
                center=(LARGURA // 2, ALTURA - 65)
            )

            tela.blit(mensagem, posicao)

        pygame.display.flip()

        pixels = pygame.surfarray.array3d(tela)

        quadro = np.transpose(
            pixels, (1, 0, 2)
        )

        gravador.append_data(quadro)

        if frame % FPS == 0:
            print(f"Gravando: {frame // FPS}s")

        relogio.tick(FPS)

except KeyboardInterrupt:
    print("Gravacao interrompida.")

finally:
    gravador.close()
    pygame.quit()

print("Arquivo de video:", saida)
