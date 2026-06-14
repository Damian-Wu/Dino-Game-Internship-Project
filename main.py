"""Dino Game in Python

A game similar to the famous Chrome Dino Game, built using pygame-ce.
Made by intern: @bassemfarid, no one or nothing else. 🤖
Additional author: Damian Wu

import random
import pygame

# Initialize Pygame and create a window
pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
running = True  # Pygame main loop, kills pygame when False

# Game state variables
is_playing = True  # Whether in game or in menu
GROUND_Y = 300  # The Y-coordinate of the ground level
JUMP_GRAVITY_START_SPEED = -20  # The speed at which the player jumps
players_gravity_speed = 0  # The current speed at which the player falls
start_time = pygame.time.get_ticks()
current_score = 0
MAX_JUMPS = 2  # Allows the player to jump once in the air
jump_count = 0  # Tracks how many jumps have been used before landing

# Load level assets
SKY_SURF = pygame.image.load("graphics/level/sky.png").convert()
GROUND_SURF = pygame.image.load("graphics/level/ground.png").convert()
game_font = pygame.font.Font(pygame.font.get_default_font(), 50)
score_surf = game_font.render("SCORE?", False, "Black")
score_rect = score_surf.get_rect(center=(400, 50))

# Load sprite assets
player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(bottomleft=(25, GROUND_Y))
# Enlarged player image for the game over transition screen
player_stand = pygame.transform.rotozoom(player_walk_1, 0, 4)
player_stand_rect = player_stand.get_rect(center=(400, 215))
egg_surf = pygame.image.load("graphics/egg/egg_1.png").convert_alpha()
egg_rect = egg_surf.get_rect(bottomleft=(800, GROUND_Y))
enemy_rect_list = []

# Timer event creates enemies instead of using only one repeating egg
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1500)


def display_score():
    """Display and return the current score based on elapsed time."""
    current_time = int((pygame.time.get_ticks() - start_time) / 1000)
    score_surf = game_font.render(f"Score: {current_time}", False, "Black")
    score_rect = score_surf.get_rect(center=(400, 50))
    pygame.draw.rect(screen, "#c0e8ec", score_rect)
    pygame.draw.rect(screen, "#c0e8ec", score_rect, 10)
    screen.blit(score_surf, score_rect)
    return current_time

def player_animation():
    """Switch between walking images while the player is on the ground."""
    global player_surf, player_index
    if player_rect.bottom < GROUND_Y:
        player_surf = player_walk_1
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]

def move_enemies(enemy_list):
    """Move all enemies left, draw them, and remove enemies off screen."""
    if enemy_list:
        for enemy_rect in enemy_list:
            enemy_rect.x -= 5
            screen.blit(egg_surf, enemy_rect)

        enemy_list = [enemy for enemy in enemy_list if enemy.x > -100]
        return enemy_list
    else:
        return []

def check_enemy_collision(player, enemies):
    """Return False when the player hits an enemy, otherwise keep playing."""
    for enemy in enemies:
        if player.colliderect(enemy):
            return False
    return True

while running:
    # Poll for events
    for event in pygame.event.get():
        # pygame.QUIT --> user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

        elif is_playing:
            # When player wants to jump by pressing SPACE
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
                or event.type == pygame.MOUSEBUTTONDOWN
            ) and jump_count < MAX_JUMPS:
                # Double jump: count jumps and reset the count after landing
                players_gravity_speed = JUMP_GRAVITY_START_SPEED
                jump_count += 1
            if event.type == enemy_timer:
                # Spawn enemies at slightly different starting x positions
                enemy_rect_list.append(
                    egg_surf.get_rect(bottomleft=(random.randint(900, 1100), GROUND_Y))
                )
        else:
            # When player wants to play again by pressing SPACE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                is_playing = True
                start_time = pygame.time.get_ticks()
                egg_rect.left = 800
                player_rect.bottom = GROUND_Y
                players_gravity_speed = 0
                enemy_rect_list.clear()
                jump_count = 0

    if is_playing:
        screen.fill("purple")  # Wipe the screen

        # Blit the level assets
        screen.blit(SKY_SURF, (0, 0))
        screen.blit(GROUND_SURF, (0, GROUND_Y))
        current_score = display_score()

        # Move and draw all enemies
        enemy_rect_list = move_enemies(enemy_rect_list)

        # Adjust player's vertical location then blit it
        players_gravity_speed += 1
        player_rect.y += players_gravity_speed
        if player_rect.bottom > GROUND_Y:
            player_rect.bottom = GROUND_Y
            jump_count = 0
        
        player_animation()
        screen.blit(player_surf, player_rect)
        # When player collides with enemy, game ends
        is_playing = check_enemy_collision(player_rect, enemy_rect_list)

    # When game is over, display game over message
    else:
        screen.fill("gray20")

        game_over_surf = game_font.render("Game Over", False, "White")
        game_over_rect = game_over_surf.get_rect(center=(400, 55))
        screen.blit(game_over_surf, game_over_rect)

        pygame.draw.rect(screen, "White", player_stand_rect.inflate(30, 30), border_radius=10)
        screen.blit(player_stand, player_stand_rect)

        score_message_surf = game_font.render(f"Score: {current_score}", False, "White")
        score_message_rect = score_message_surf.get_rect(center=(400, 325))
        screen.blit(score_message_surf, score_message_rect)

        restart_surf = game_font.render("Press SPACE", False, "White")
        restart_rect = restart_surf.get_rect(center=(400, 370))
        screen.blit(restart_surf, restart_rect)

    # flip the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # Limits game loop to 60 FPS

pygame.quit()
