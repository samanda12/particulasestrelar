
import pygame
import random
import math
import imageio.v2 as imageio
import numpy as np

from PIL import Image
from pathlib import Path

pygame.init()


LARGURA = 1000
ALTURA = 750

FPS = 30
DURACAO = 15
TOTAL_FRAMES = FPS * DURACAO

FUNDO = (3, 3, 14)

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Projeto Estrelar - Anne")

relogio = pygame.time.Clock()


pasta = Path(__file__).resolve().parent


imagem = Image.open(
    pasta / "fotoanne.png"
).convert("RGBA")

imagem.thumbnail((540, 620))

offset_x = (LARGURA - imagem.width) // 2
offset_y = (ALTURA - imagem.height) // 2


particulas = []

PASSO = 4

for y in range(0, imagem.height, PASSO):
    for x in range(0, imagem.width, PASSO):

        r, g, b, a = imagem.getpixel((x, y))

        if a > 100:
            particulas.append({
                "x": random.uniform(0, LARGURA),
                "y": random.uniform(0, ALTURA),
                "dx": x + offset_x,
                "dy": y + offset_y,
                "cor": (r, g, b),
                "fase": random.uniform(0, math.tau),
                "vel": random.uniform(0.7, 1.3)
            })

print("Particulas:", len(particulas))


estrelas = []

for i in range(160):
    estrelas.append({
        "x": random.randint(0, LARGURA - 1),
        "y": random.randint(0, ALTURA - 1),
        "fase": random.uniform(0, math.tau),
        "tamanho": random.choice([1, 1, 2])
    })

ESCALA = 4

brilho = pygame.Surface(
    (LARGURA // ESCALA, ALTURA // ESCALA),
    pygame.SRCALPHA
)

fonte = pygame.font.SysFont("consolas", 18)
fonte_final = pygame.font.SysFont(
    "georgia", 32, bold=True
)


def explodir():

    centro_x = LARGURA / 2
    centro_y = ALTURA / 2

    for p in particulas:

        angulo = math.atan2(
            p["dy"] - centro_y,
            p["dx"] - centro_x
        )

        angulo += random.uniform(-0.8, 0.8)
        distancia = random.uniform(180, 650)

        p["x"] = p["dx"] + math.cos(angulo) * distancia
        p["y"] = p["dy"] + math.sin(angulo) * distancia



arquivo_video = pasta / "Projeto_Estrelar_Anne.mp4"

gravador = imageio.get_writer(
    str(arquivo_video),
    fps=FPS,
    codec="libx264",
    quality=8,
    macro_block_size=2
)

executando = True

try:

    for frame_atual in range(TOTAL_FRAMES):

      
        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                executando = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    executando = False

        if not executando:
            break

        tempo = frame_atual / FPS

        if frame_atual == 7 * FPS:
            explodir()

        tela.fill(FUNDO)
        brilho.fill((0, 0, 0, 0))
        
    for estrela in estrelas:

            intensidade = int(
                100 + 100 * abs(
                    math.sin(
                        tempo * 2 + estrela["fase"]
                    )
                )
            )

            cor = (
                intensidade,
                intensidade,
                min(255, intensidade + 30)
            )

            pygame.draw.circle(
                tela,
                cor,
                (estrela["x"], estrela["y"]),
                estrela["tamanho"]
            )

        
        for p in particulas:

            flutuar_x = math.sin(
                tempo * p["vel"] + p["fase"]
            ) * 1.8

            flutuar_y = math.cos(
                tempo * p["vel"] + p["fase"]
            ) * 1.8

            destino_x = p["dx"] + flutuar_x
            destino_y = p["dy"] + flutuar_y

            p["x"] += (destino_x - p["x"]) * 0.055
            p["y"] += (destino_y - p["y"]) * 0.055

            px = int(p["x"])
            py = int(p["y"])

            if not (
                0 <= px < LARGURA
                and 0 <= py < ALTURA
            ):
                continue

            r, g, b = p["cor"]

            cor_luz = (
                min(255, int(r * 1.15)),
                min(255, int(g * 1.15)),
                min(255, int(b * 1.20))
            )

            pygame.draw.circle(
                tela,
                cor_luz,
                (px, py),
                2
            )

            bx = px // ESCALA
            by = py // ESCALA

            pygame.draw.circle(
                brilho,
                (r, g, b, 35),
                (bx, by),
                2
            )


        brilho_grande = pygame.transform.smoothscale(
            brilho,
            (LARGURA, ALTURA)
        )

        tela.blit(
            brilho_grande,
            (0, 0),
            special_flags=pygame.BLEND_RGBA_ADD
        )

        
        pygame.display.flip()

        
        pixels = pygame.surfarray.array3d(tela)

        quadro = np.transpose(
            pixels, (1, 0, 2)
        )

        gravador.append_data(quadro)

       
        if frame_atual % FPS == 0:
            print(
                f"Gravando: {frame_atual // FPS}s"
            )

        relogio.tick(FPS)

finally:

    gravador.close()
    pygame.quit()

print("Gravacao encerrada!")
print("Arquivo:", arquivo_video)
