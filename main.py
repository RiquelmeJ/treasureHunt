import pgzrun
import random
from pgzero.actor import Actor
from pgzero.keyboard import keyboard

WIDTH, HEIGHT = 800, 600
playing = False
isSoundOn = True
gameEnded = False
music.play('background_music')
music.set_volume(0.5)

up_images = ['up_1', 'up_2', 'up_3']
down_images = ['down_1', 'down_2', 'down_3']
left_images = ['left_1', 'left_2', 'left_3']
right_images = ['right_1', 'right_2', 'right_3']
current_image_index = 0
player = Actor(up_images[current_image_index], center=(400, 300))
player_lives = 5
player_score = 0
invincible = False

m1_images = ['monster_d1', 'monster_d2', 'monster_d3']
m2_images = ['monster_u1', 'monster_u2', 'monster_u3']
m3_images = ['monster_r1', 'monster_r2', 'monster_r3']
m4_images = ['monster_l1', 'monster_l2', 'monster_l3']

m1_image_index = m2_image_index = m3_image_index = m4_image_index = 0

background = Actor('background_menu', topleft=(0, 0))
play_button = Actor('play_button', center=(400, 400))
sound_button = Actor('sound_on_button', center=(350, 475))
quit_button = Actor('quit_button', center=(450, 475))

monster1 = Actor(
    m1_images[m1_image_index],
    center=(random.randint(40, WIDTH - 40), 0)
)
monster2 = Actor(
    m2_images[m2_image_index],
    center=(random.randint(40, WIDTH - 40), HEIGHT)
)
monster3 = Actor(
    m3_images[m3_image_index],
    center=(0, random.randint(40, HEIGHT - 40))
)
monster4 = Actor(
    m4_images[m4_image_index],
    center=(WIDTH, random.randint(40, HEIGHT - 40))
)

treasure = Actor(
    'treasure',
    center=(random.randint(40, WIDTH - 40), random.randint(40, HEIGHT - 40))
)


def on_mouse_down(pos):
    global isSoundOn, playing
    if not playing and not gameEnded:
        if play_button.collidepoint(pos):
            if isSoundOn:
                sounds.sfx_select.play()
            playing = True
        if sound_button.collidepoint(pos):
            if isSoundOn:
                music.set_volume(0)
                isSoundOn = False
                sound_button.image = 'sound_off_button'
            else:
                music.set_volume(0.5)
                sounds.sfx_select.play()
                isSoundOn = True
                sound_button.image = 'sound_on_button'
        if quit_button.collidepoint(pos):
            quit()


def advance_image():
    global current_image_index, m1_image_index, m2_image_index, m3_image_index, m4_image_index

    # Player
    if keyboard.up:
        current_image_index = (current_image_index + 1) % len(up_images)
        player.image = up_images[current_image_index]
    elif keyboard.down:
        current_image_index = (current_image_index + 1) % len(down_images)
        player.image = down_images[current_image_index]
    elif keyboard.left:
        current_image_index = (current_image_index + 1) % len(left_images)
        player.image = left_images[current_image_index]
    elif keyboard.right:
        current_image_index = (current_image_index + 1) % len(right_images)
        player.image = right_images[current_image_index]
    else:
        player.image = 'down_1'

    # Monster 1
    m1_image_index = (m1_image_index + 1) % len(m1_images)
    monster1.image = m1_images[m1_image_index]

    # Monster 2
    m2_image_index = (m2_image_index + 1) % len(m2_images)
    monster2.image = m2_images[m2_image_index]

    # Monster 3
    m3_image_index = (m3_image_index + 1) % len(m3_images)
    monster3.image = m3_images[m3_image_index]

    # Monster 4
    m4_image_index = (m4_image_index + 1) % len(m4_images)
    monster4.image = m4_images[m4_image_index]


def manage_player_movement():
    if keyboard.left:
        player.x -= 5
    if keyboard.right:
        player.x += 5
    if keyboard.up:
        player.y -= 5
    if keyboard.down:
        player.y += 5
    player.x = max(60, min(player.x, WIDTH - 60))
    player.y = max(60, min(player.y, HEIGHT - 60))


def manage_monsters_movement():
    monster1.y += random.randint(4, 7)
    if monster1.top > HEIGHT:
        monster1.midbottom = (random.randint(40, WIDTH - 40), 0)
    monster2.y -= random.randint(4, 7)
    if monster2.bottom < 0:
        monster2.midtop = (random.randint(40, WIDTH - 40), HEIGHT)
    monster3.x += random.randint(4, 7)
    if monster3.left > WIDTH:
        monster3.midright = (0, random.randint(40, HEIGHT - 40))
    monster4.x -= random.randint(4, 7)
    if monster4.right < 0:
        monster4.midleft = (WIDTH, random.randint(40, HEIGHT - 40))


def hit_player():
    global player_lives, invincible, gameEnded, playing, isSoundOn
    if not invincible:
        if isSoundOn:
            sounds.sfx_hurt.play()
        player_lives -= 1
        invincible = True
        if player_lives == 0:
            playing = False
            gameEnded = True
        clock.schedule_unique(reset_invincibility, 1.5)


def reset_invincibility():
    global invincible
    invincible = False


def manage_collisions():
    global player_score, isSoundOn
    if (player.colliderect(monster1) or
            player.colliderect(monster2) or
            player.colliderect(monster3) or
            player.colliderect(monster4)):
        hit_player()

    if player.colliderect(treasure):
        player_score += 1
        if isSoundOn:
            sounds.sfx_coin.play()
        treasure.center = (random.randint(40, WIDTH - 40), random.randint(40, HEIGHT - 40))


def draw():
    screen.clear()
    if not playing and not gameEnded:
        background.draw()
        play_button.draw()
        sound_button.draw()
        quit_button.draw()

    if playing and not gameEnded:
        background.image = 'background_game'
        background.draw()
        player.draw()
        monster1.draw()
        monster2.draw()
        monster3.draw()
        monster4.draw()
        treasure.draw()
        score_text = f"Score: {player_score}"
        screen.draw.text(
            score_text, (15, 10),
            color="white", fontname="geo_regular", fontsize=40
        )
        life_text = f"Lives: {player_lives}"
        screen.draw.text(
            life_text, (650, 10),
            color="white", fontname="geo_regular", fontsize=40
        )

    if not playing and gameEnded:
        music.set_volume(0)
        screen.draw.text(
            "Game ended!",
            centerx=400, centery=300,
            color="white", fontname="geo_regular", fontsize=100
        )
        score_text = f"Your score: {player_score}"
        screen.draw.text(
            score_text,
            centerx=400, centery=400,
            color="white", fontname="geo_regular", fontsize=60
        )


def update():
    if playing:
        manage_player_movement()
        manage_monsters_movement()
        manage_collisions()


clock.schedule_interval(advance_image, 0.1)

pgzrun.go()