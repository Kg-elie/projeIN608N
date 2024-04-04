from math import sin, cos, pi
import pygame


def draw_regular_polygon(surface, color, vertex_count,
                         radius, position, width=0):
    n, r = vertex_count, radius
    x, y = position
    pygame.draw.polygon(surface, color, [
        (x + r * cos(2 * pi * i / n),
         y + r * sin(2 * pi * i / n))
        for i in range(n)
    ], width)


bg_color = (0, 0, 0)
fg_color = (0, 255, 255)

w, h = 640, 360
vertex_count = 3
width = 0

pygame.init()
root = pygame.display.set_mode((w, h))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Use UP / DOWN arrow keys to
            # increase / decrease the vertex count
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                vertex_count += 1
            elif event.key == pygame.K_DOWN:
                vertex_count = max(3, vertex_count - 1)

    root.fill(bg_color)
    draw_regular_polygon(root, fg_color, vertex_count,
                         min(w, h) / 6, (w / 2, h / 2),
                         width)
    pygame.display.flip()
