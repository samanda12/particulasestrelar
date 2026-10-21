
import pygame
import random
from PIL import Image
from pathlib import Path


pygame.init()

LARGURA = 900
ALTURA = 700

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Projeto Estrelar - Anne")

relogio = pygame.time.Clock()


pasta = Path(__file__).resolve().parent
caminho = pasta / "fotoanne.png"

imagem = Image.open(caminho).convert("RGBA")
imagem.thumbnail((520, 580))

particulas = []

offset_x = (LARGURA - imagem.width) // 2
offset_y = (ALTURA - imagem.height) // 2


for y in range(0, imagem.height, 3):
    for x in range(0, imagem.width, 3):

        r, g, b, a = imagem.getpixel((x, y))

        if a > 100:
            particulas.append({
                "x": random.uniform(0, LARGURA),
                "y": random.uniform(0, ALTURA),
                "destino_x": x + offset_x,
                "destino_y": y + offset_y,
                "cor": (r, g, b)
            })

print("Particulas criadas:", len(particulas))

executando = True

while executando:

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            executando = False

        # Aperte ESPACO para reiniciar o efeito
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                for p in particulas:
                    p["x"] = random.uniform(0, LARGURA)
                    p["y"] = random.uniform(0, ALTURA)

   
    tela.fill((3, 3, 12))

    for p in particulas:


        p["x"] += (p["destino_x"] - p["x"]) * 0.04
        p["y"] += (p["destino_y"] - p["y"]) * 0.04

        pygame.draw.circle(
            tela,
            p["cor"],
            (int(p["x"]), int(p["y"])),
            1
        )

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
