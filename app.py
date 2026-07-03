import pygame
import random

# אתחול המשחק
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Special Ops vs Monsters")

# צבעים
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 100, 255)

# משתני משחק
game_state = "MENU" # MENU או PLAYING
bullets = []
monsters = [{"x": 1000, "y": random.randint(50, 550)}]

def draw_menu():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    text = font.render("START GAME (Click Space)", True, WHITE)
    screen.blit(text, (200, 250))

def run_game():
    screen.fill((30, 30, 30)) # רקע דמוי מלחמה
    # צייר חייל (נמצא בצד שמאל)
    pygame.draw.rect(screen, BLUE, (50, 300, 50, 50))
    
    # ניהול מפלצות
    for m in monsters:
        m["x"] -= 2
        pygame.draw.circle(screen, RED, (m["x"], m["y"]), 20)
        
    # ניהול יריות
    for b in bullets:
        b[0] += 10
        pygame.draw.rect(screen, WHITE, (b[0], b[1], 10, 5))

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and game_state == "PLAYING":
            bullets.append([100, 320]) # ירייה מהחייל
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_state = "PLAYING"

    if game_state == "MENU":
        draw_menu()
    else:
        run_game()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
