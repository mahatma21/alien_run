import pygame
from pygame.locals import *
import random
# Custom module
from runner_module.locals import *

def load_img(alpha_channel: bool, *img_path: str):
    img = pygame.image.load(get_file(*img_path))

    if alpha_channel:
        return img.convert_alpha()
    return img.convert()

def load_sound(*sound_path: str) -> pygame.mixer.Sound:
    return pygame.mixer.Sound(get_file(*sound_path))


class Player(Rect):

    def __init__(self):
        super().__init__(100, 200, 64, 84)
        self.y_momentum = 0
        self.movement = [0, 0]
        self.frame_count = 0
        self.is_jump = 0
        self.score = 0
        # Set score text
        self.update_score_text()

    def jump(self):
        if not self.is_jump:
            self.jump_sound.play()
            self.y_momentum = -10
            self.is_jump = 1

    def draw(self, display, scroll):
        if self.is_jump:
            frame = self.jump_img
        else:
            frame = self.walk_frames[0 if self.frame_count < 7 else 1]

            self.frame_count += 1
            if self.frame_count > 13:
                self.frame_count = 0

        display.blit(frame, self.move(-scroll, 0))

    def reset_movement(self):
        self.movement = [0, 0]

    def update_score_text(self):
        self.score_text = SCORE_FONT.render(
            f"Score: {self.score}", 0, Color('black'))

    def increment_score(self):
        """Increment player score and update the score text."""
        self.score += 1
        self.update_score_text()

    def reset_score(self):
        """Set score value to 0 and update the score text."""
        self.score = 0
        self.update_score_text()

    def get_mid_score_text(self):
        return self.score_text.get_width() / 2

    @classmethod
    def load_assets(cls):
        # Load player animation and images
        cls.walk_frames = (
            load_img(1, PLAYER_PATH, 'player_walk_1.png'),
            load_img(1, PLAYER_PATH, 'player_walk_2.png'),
        )
        cls.stand_img = load_img(1, PLAYER_PATH, 'player_stand.png')
        cls.stand_img = pygame.transform.scale(
            cls.stand_img, [n * 2 for n in cls.stand_img.get_size()])
        cls.jump_img = load_img(1, PLAYER_PATH, 'jump.png')
        # Load player sound effect
        cls.jump_sound = load_sound(AUDIO_PATH, 'jump.wav')
        cls.jump_sound.set_volume(0.3)


class Enemy(Rect):
    x_vel = 1

    def __init__(self, type: str, ground_rect: Rect, scroll: int):
        super().__init__(self.animation_frames[type][0].get_rect())

        if type == 'snail':
            self.bottom = ground_rect.top
        elif type == 'fly':
            self.y = 150

        self.type = type
        self.x = WIN_SIZE[0] + self.width + scroll
        self.frame_count = 0

    def move_sprite(self):
        """Moving enemy sprite to the left base on 'Enemy' x_vel."""
        self.x -= self.x_vel

    def draw(self, display, scroll):
        frame = self.animation_frames[self.type][0 if self.frame_count < 7 else 1]

        self.frame_count += 1
        if self.frame_count > 13:
            self.frame_count = 0

        display.blit(frame, self.move(-scroll, 0))

    @classmethod
    def reset_x_vel(cls):
        cls.x_vel = 1

    @classmethod
    def increment_x_vel(cls):
        cls.x_vel += 0.05 / cls.x_vel

    @classmethod
    def load_images(cls):
        cls.animation_frames = {
            'snail': (load_img(1, SNAIL_PATH, 'snail1.png'),
                      load_img(1, SNAIL_PATH, 'snail2.png')),
            'fly': (load_img(1, FLY_PATH, 'fly1.png'),
                    load_img(1, FLY_PATH, 'fly2.png')),
        }


def generate_enemy(ground_rect: Rect, scroll: int) -> Enemy:
    enemy_type = random.choice(('snail', 'snail', 'fly'))
    return Enemy(enemy_type, ground_rect, scroll)
