import pygame
import sys
from pygame.locals import*
import Button
pygame.init()

# game window
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 440
LOWER_MARGIN = 100
SIDE_MARGIN = 300

# screen
screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption("Level Editor")

# time
clock = pygame.time.Clock()
FPS = 60

# game variables
ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 11
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 5

# load images
pine1_img = pygame.image.load("Sprites/Background/pine1.png").convert_alpha()
pine2_img = pygame.image.load("Sprites/Background/pine2.png").convert_alpha()
mountain_img = pygame.image.load("Sprites/Background/mountain2.png").convert_alpha()
sky_img = pygame.image.load("Sprites/Background/sky.png").convert_alpha()
cloud_img = pygame.image.load("Sprites/Background/cloud.png").convert_alpha()

# tiles
tile_list = []
for i in range(TILE_TYPES):
    tile = pygame.image.load(f"Sprites/Tile/Ground/ground_{i+1}.png").convert_alpha()
    tile = pygame.transform.scale(tile, (TILE_SIZE, TILE_SIZE))
    tile_list.append(tile)

# create world tile list
world_data = [[-1 for j in range(MAX_COLS+1)]for i in range(ROWS+1)]

# create ground
for i in range(0, MAX_COLS):
    world_data[ROWS][i] = 1

# background
def draw_bg():
    screen.fill(pygame.Color("darkslateblue"))

    width = sky_img.get_width()
    for i in range(6):
        screen.blit(sky_img, ((i * width) + scroll * 0.5, 0))
        screen.blit(cloud_img, ((i * width) + scroll * 0.6, 30))
        screen.blit(mountain_img, ((i * width) + scroll * 0.7, SCREEN_HEIGHT - mountain_img.get_height() - 200))
        screen.blit(pine1_img, ((i * width) + scroll * 0.8, SCREEN_HEIGHT - pine1_img.get_height() - 112))
        screen.blit(pine2_img, ((i * width) + scroll * 0.9, SCREEN_HEIGHT - pine2_img.get_height()))
    pygame.draw.rect(screen, pygame.Color("darkslateblue"), (0, SCREEN_HEIGHT - 8, SCREEN_WIDTH + SIDE_MARGIN, LOWER_MARGIN + 100))


# draw grid
def draw_grid():
    for i in range(MAX_COLS + 1):
        pygame.draw.line(screen, pygame.Color("white"), (i * TILE_SIZE + scroll,0), (i * TILE_SIZE + scroll, SCREEN_HEIGHT - 8))
        for j in range(ROWS + 1):
            pygame.draw.line(screen, pygame.Color("white"), (0, j * TILE_SIZE), (SCREEN_WIDTH - 6, j * TILE_SIZE))

# draw world data
def draw_world():
    for y,row in enumerate(world_data):
        for x,tile in enumerate(row):
            if tile >= 0:
                screen.blit(tile_list[tile], (x * TILE_SIZE + scroll, y * TILE_SIZE))


# create buttons/ button list
button_list = []
button_col = 0
button_row = 0
for i in range(len(tile_list)):
    tile_button = Button.Button(SCREEN_WIDTH + (90 * button_col) + 40, (75 * button_row) + 50, tile_list[i], 1.5)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0

run = True
while run:

    clock.tick(FPS)

    draw_bg()
    draw_grid()
    draw_world()

    # draw tile panel and tiles
    pygame.draw.rect(screen, pygame.Color("darkslateblue"), (SCREEN_WIDTH-5, 0, SIDE_MARGIN+5, SCREEN_HEIGHT + 100))

    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count

    # highlight selected tile
    pygame.draw.rect(screen, pygame.Color("red"), button_list[current_tile].rect, 3)

    # scroll the map
    right_end = -((MAX_COLS * TILE_SIZE) - SCREEN_WIDTH)
    if scroll > 0:
        scroll = 0
    if scroll < right_end:
        scroll = right_end
    if scroll_left and scroll < 0:
        scroll += scroll_speed
    if scroll_right and scroll > right_end:
        scroll -= scroll_speed
    print(scroll)

    # add new tiles to screen
    mouse_pos = pygame.mouse.get_pos()
    x = (mouse_pos[0] - scroll) // TILE_SIZE
    y = mouse_pos[1] // TILE_SIZE

    # check that the mouse is within tiling area
    if mouse_pos[0] < SCREEN_WIDTH - 5 and mouse_pos[1] < SCREEN_HEIGHT:
        if pygame.mouse.get_pressed()[0]:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2]:
            world_data[y][x] = -1

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # keyboard presses
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                scroll_left = True
            if event.key == K_RIGHT:
                scroll_right = True
            if event.key == K_LSHIFT:
                scroll_speed = 20


        if event.type == KEYUP:
            if event.key == K_LEFT:
                scroll_left = False
            if event.key == K_RIGHT:
                scroll_right = False
            if event.key == K_LSHIFT:
                scroll_speed = 5

    pygame.display.update()

