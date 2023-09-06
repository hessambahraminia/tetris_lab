import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 600
GRID_SIZE = 30
GRID_WIDTH, GRID_HEIGHT = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

SHAPES_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (128, 128, 128)]

# Initialize game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# Initialize clock
clock = pygame.time.Clock()

# Initialize game variables
grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
current_shape = None
current_color = None
shape_x, shape_y = 0, 0
score = 0
game_over = False

def draw_grid():
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[y][x]:
                pygame.draw.rect(screen, grid[y][x], (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def draw_shape():
    for row in range(len(current_shape)):
        for col in range(len(current_shape[row])):
            if current_shape[row][col]:
                x = shape_x + col
                y = shape_y + row
                pygame.draw.rect(screen, current_color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def new_shape():
    global current_shape, current_color, shape_x, shape_y, game_over
    shape = random.choice(SHAPES)
    current_shape = shape
    current_color = random.choice(SHAPES_COLORS)
    shape_x = GRID_WIDTH // 2 - len(shape[0]) // 2
    shape_y = 0
    if check_collision(current_shape, shape_x, shape_y):
        game_over = True

def check_collision(shape, x, y):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col]:
                if x + col < 0 or x + col >= GRID_WIDTH or y + row >= GRID_HEIGHT or grid[y + row][x + col]:
                    return True
    return False

def place_shape():
    global grid, current_shape, current_color, shape_x, shape_y, score
    for row in range(len(current_shape)):
        for col in range(len(current_shape[row])):
            if current_shape[row][col]:
                grid[shape_y + row][shape_x + col] = current_color

    # Check for completed rows
    completed_rows = []
    for row in range(GRID_HEIGHT):
        if all(grid[row]):
            completed_rows.append(row)

    # Clear completed rows and shift above rows down
    for row in completed_rows:
        grid.pop(row)
        grid.insert(0, [0] * GRID_WIDTH)
        score += 100

    new_shape()

new_shape()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if not check_collision(current_shape, shape_x - 1, shape_y):
                    shape_x -= 1
            elif event.key == pygame.K_RIGHT:
                if not check_collision(current_shape, shape_x + 1, shape_y):
                    shape_x += 1
            elif event.key == pygame.K_DOWN:
                if not check_collision(current_shape, shape_x, shape_y + 1):
                    shape_y += 1
            elif event.key == pygame.K_SPACE:  # Rotate using space
                rotated_shape = [list(row) for row in zip(*current_shape[::-1])]
                if not check_collision(rotated_shape, shape_x, shape_y):
                    current_shape = rotated_shape

    if not game_over:
        # Move the shape down automatically
        if not check_collision(current_shape, shape_x, shape_y + 1):
            shape_y += 1
        else:
            place_shape()

    # Clear the screen
    screen.fill(BLACK)

    # Draw the game elements
    draw_grid()
    draw_shape()

    if game_over:
        # Display "Game Over" text
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(5)  # Set speed to 5

# Quit the game
pygame.quit()
