import pgzrun
import random

WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
ALIEN_SIZE = 30
BULLET_SIZE = 10
PLAYER_SPEED = 5
ALIEN_SPEED = 2
BULLET_SPEED = 5
LIVES = 3

WHITE = (255, 255, 255)
RED = (255, 0, 0)

player = Actor('player', center=(WIDTH / 2, HEIGHT - PLAYER_SIZE - 20))
aliens = []
for _ in range(10):
    alien = Actor('alien', pos=(random.randint(0, WIDTH - ALIEN_SIZE), 0))  # Start at the top of the screen
    aliens.append(alien)

bullets = []
lives = LIVES
player_invincible = False
player_invincible_time = 0
game_over = False
score = 0

def draw():
    screen.clear()
    screen.fill(WHITE)
    if not player_invincible:
        player.draw()
    for alien in aliens:
        alien.draw()
    for bullet in bullets:
        bullet.draw()
    screen.draw.text("Lives: " + str(lives), topleft=(10, 10), color=RED, fontsize=30)
    screen.draw.text("Score: " + str(score), topleft=(10, 40), color=RED, fontsize=30)
    if game_over:
        screen.draw.text("Game Over!", center=(WIDTH / 2, HEIGHT / 2), color=RED, fontsize=50)
    if score >= 100:
        screen.draw.text("You Win!", center=(WIDTH / 2, HEIGHT / 2), color=RED, fontsize=50)

def update():
    global ALIEN_SPEED, lives, player_invincible, player_invincible_time, game_over, score
    if game_over or score >= 100:
        return  # Stop updating the game state if the game is over or won

    if keyboard.left:
        player.x -= PLAYER_SPEED
    if keyboard.right:
        player.x += PLAYER_SPEED

    for alien in aliens:
        alien.y += ALIEN_SPEED  # Move aliens down the screen
        if alien.y > HEIGHT:  # If an alien reaches the bottom, reset its position
            alien.y = 0
            alien.x = random.randint(0, WIDTH - ALIEN_SIZE)

    for bullet in bullets:
        bullet.y -= BULLET_SPEED
        if bullet.y < 0:
            bullets.remove(bullet)

    for bullet in bullets:
        for alien in aliens:
            if bullet.colliderect(alien):
                bullets.remove(bullet)
                aliens.remove(alien)
                score += 10
                break

    if len(aliens) == 0:
        aliens.append(Actor('alien', pos=(random.randint(0, WIDTH - ALIEN_SIZE), 0)))

    for alien in aliens:
        if player.colliderect(alien) and not player_invincible:
            lives -= 1
            if lives == 0:
                game_over = True
            else:
                player_invincible = True
                player_invincible_time = 0

    if player_invincible:
        player_invincible_time += 1
        if player_invincible_time >= 240:  # 4 seconds at 60 FPS
            player_invincible = False

def on_key_down(key):
    if key == keys.SPACE:
        bullet = Actor('bullet', pos=player.pos)
        bullets.append(bullet)

pgzrun.go()