import pygame
from pygame.locals import *
import sys
import time
# Custom module
from runner_module.locals import *
import runner_module.logic as lg

pygame.mixer.pre_init(48000, -16, 2, 512)
pygame.init()

clock = pygame.time.Clock()
true_scroll = 0
text_count = 30
is_game_active = 0
is_game_start = 1

pygame.mixer.music.load(get_file(AUDIO_PATH, 'music.wav'))
pygame.mixer.music.set_volume(0.1)

player = lg.Player()
enemies = []

ADD_ENEMY = USEREVENT + 1
pygame.time.set_timer(ADD_ENEMY, 1000)

pygame.display.set_caption("Alien Run")
display = pygame.display.set_mode(WIN_SIZE)
pygame.display.set_icon(lg.load_img(1, IMG_PATH, 'icon.png'))

ground_img = lg.load_img(0, IMG_PATH, 'ground.png')
ground_rect = ground_img.get_rect(bottomleft=(0, WIN_SIZE[1]))
bg_img = lg.load_img(0, IMG_PATH, 'bg.png')
bg_rect = bg_img.get_rect()

lg.Player.load_assets()
lg.Enemy.load_images()

pygame.mixer.music.play(-1)
while 1:
    if is_game_active:
        true_scroll += player.centerx - true_scroll - (WIN_MID[0])
        scroll = round(true_scroll + 200)

        # Display rect
        display_r = Rect(scroll, 0, *WIN_SIZE)

        display.fill(Color('black'))

        # Draw background image
        draw_x = (bg_rect.x - (scroll * 0.5)) % bg_rect.width
        display.blit(bg_img, (draw_x, bg_rect.y))
        display.blit(bg_img, (draw_x - bg_rect.width, bg_rect.y))

        # Draw ground image
        draw_x = (ground_rect.x - scroll) % ground_rect.width
        display.blit(ground_img, (draw_x, ground_rect.y))
        display.blit(ground_img, (draw_x - ground_rect.width, ground_rect.y))

        # Handling and draw enemies
        for enemy in enemies:
            enemy.draw(display, scroll)
            enemy.move_sprite()
            if enemy.type == 'snail':
                enemy.bottom = ground_rect.top

            if enemy.colliderect(player):
                is_game_active = 0
                enemies.clear()
                is_end_wait = 1
                end_score_text = END_SCORE_FONT.render(
                    f"Score: {player.score}", 0, Color('black'))

            if enemy.right < display_r.left:
                enemies.remove(enemy)

        # Draw player
        player.draw(display, scroll)

        # Increment score text every second
        currentTm = time.time()
        if currentTm - score_start_time >= 1:
            player.increment_score()
            score_start_time = currentTm
        # Draw score text
        display.blit(
            player.score_text, (WIN_MID[0] - player.get_mid_score_text(), 50))

        for event in pygame.event.get():
            if event.type == QUIT or (
                    event.type == KEYDOWN and event.key == K_ESCAPE):
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    player.jump()
            if event.type == ADD_ENEMY:
                enemies.append(lg.generate_enemy(ground_rect, scroll))

        player.reset_movement()
        player.movement[0] += 7

        player.y_momentum += 0.5
        if player.y_momentum > 8:
            player.y_momentum = 8
        player.movement[1] += player.y_momentum

        player.move_ip(player.movement)
        if player.bottom > ground_rect.top:
            player.bottom = ground_rect.top
            player.y_momentum = 0
            player.is_jump = 0

        # Increment enemy move velocity
        lg.Enemy.increment_x_vel()

    else:
        display.fill((110, 150, 170))
        display.blit(TITLE_TEXT,
                     (WIN_MID[0] - (TITLE_TEXT.get_width() / 2),
                      20))

        if is_game_start:
            # Draw start text
            if text_count >= 30:
                display.blit(START_TEXT,
                             (WIN_MID[0] - (START_TEXT.get_width() / 2),
                              400))
            # Handling text blink
            text_count += 1
            if text_count >= 60:
                text_count = 0
        else:
            # Draw score
            display.blit(
                end_score_text,
                (WIN_MID[0] - (end_score_text.get_width() / 2),
                 350))
            if text_count >= 30:
                display.blit(
                    PLAY_AGAIN_TEXT,
                    (WIN_MID[0] - (START_TEXT.get_width() / 2),
                     400))
            text_count += 1
            if text_count >= 60:
                text_count = 0


        display.blit(player.stand_img, (
            WIN_MID[0] - (player.stand_img.get_width() / 2),
            WIN_MID[1] - (player.stand_img.get_height() / 2)))

        for event in pygame.event.get():
            if event.type == QUIT or (
                    event.type == KEYDOWN and event.key == K_ESCAPE):
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    text_count = 30
                    player.bottom = ground_rect.top
                    player.x_vel = 7
                    player.reset_score()
                    is_game_active = 1
                    is_game_start = 0
                    score_start_time = time.time()
                    lg.Enemy.reset_x_vel()

    pygame.display.update()
    clock.tick(60)
