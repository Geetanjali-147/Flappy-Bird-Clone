import pygame
import random

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 800
BIRD_X = 50
BIRD_Y = 250
GRAVITY = 0.3
FLAP_STRENGTH = -8
PIPE_WIDTH = 70
PIPE_GAP = 250
PIPE_SPEED = 3
WHITE = (255, 255, 255)

# Setup Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

# Load Assets
bird_img = pygame.transform.scale(
    pygame.image.load("images.png").convert_alpha(), (60, 50)
)

# Game Variables
bird_y = BIRD_Y
bird_velocity = 0
pipes = [(WIDTH, random.randint(150, 400))]  # (pipe_x, pipe_height)
score = 0

# Function for Game Over Screen
def game_over_screen(score):
    font = pygame.font.Font(None, 50)
    text = font.render(f"Game Over! Final Score: {score}", True, (255, 0, 0))
    screen.fill(WHITE)
    screen.blit(text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
    pygame.display.update()

    # Wait until user presses a key or quits
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False  # Exit game over screen

# Game Loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:  # Detect mouse click
            bird_velocity = FLAP_STRENGTH  # Make the bird flap

    # Bird Movement
    bird_velocity += GRAVITY
    bird_y += bird_velocity

    # Pipe Movement
    for i in range(len(pipes)):
        pipes[i] = (pipes[i][0] - PIPE_SPEED, pipes[i][1])

    # Generate New Pipes
    if pipes[-1][0] < WIDTH - 200:
        pipes.append((WIDTH, random.randint(150, 400)))

    # Remove Off-Screen Pipes and Update Score
    if pipes[0][0] < -PIPE_WIDTH:
        pipes.pop(0)
        score += 1

    # Draw Bird
    screen.blit(bird_img, (BIRD_X, bird_y))
    bird_rect = pygame.Rect(BIRD_X, bird_y, 60, 50)  # Bird bounding box

    # Draw Pipes and Check Collision
    for pipe_x, pipe_height in pipes:
        # Pipe rectangles
        top_pipe = pygame.Rect(pipe_x, 0, PIPE_WIDTH, pipe_height)
        bottom_pipe = pygame.Rect(pipe_x, pipe_height + PIPE_GAP, PIPE_WIDTH, HEIGHT)

        # Draw pipes
        pygame.draw.rect(screen, (0, 255, 0), top_pipe)       # Top pipe
        pygame.draw.rect(screen, (0, 255, 0), bottom_pipe)    # Bottom pipe

        # Collision check
        if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe):
            game_over_screen(score)  # Show Game Over screen
            running = False

    # Screen boundary collision
    if bird_y < 0 or bird_y + 50 > HEIGHT:
        game_over_screen(score)  # Show Game Over screen
        running = False

    # Display Score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(20)

pygame.quit()
