import pygame
# from datetime import datetime
# from datetime import timedelta
import json
import os
import math
import helpers
import numpy as np
from menu import main_menu
from pygame import mixer

# from copy import deepcopy

pygame.init()
pygame.font.init()
pygame.mixer.init()

win_sound = pygame.mixer.Sound('sound/muchasgracias.ogg')
win_sound.set_volume(1.0)
death_sound = pygame.mixer.Sound('sound/eaten.ogg')
death_sound.set_volume(1.0)
countdown_sound = pygame.mixer.Sound('sound/countdown.ogg')
countdown_sound.set_volume(1.0)

WIDTH, HEIGHT = 900, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeon Dash")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WINNER_FONT = pygame.font.SysFont('impact', 100)
COUNTDOWN_FONT = pygame.font.SysFont('impact', 500)


FPS = 30
PLAYER_WIDTH, PLAYER_HEIGHT = 60, 60
MONSTER_WIDTH, MONSTER_HEIGHT = 830, 350

P1_KEYS = {'up': pygame.K_UP, 'down': pygame.K_DOWN, 'left': pygame.K_LEFT, 'right': pygame.K_RIGHT}
P2_KEYS = {'up': pygame.K_w, 'down': pygame.K_s, 'left': pygame.K_a, 'right': pygame.K_d}

running_man = [
    pygame.transform.scale(pygame.image.load(os.path.join('running_man', x)), (PLAYER_WIDTH, PLAYER_HEIGHT))
    for x in sorted(os.listdir('running_man'))]
running_man_2 = [
    pygame.transform.scale(pygame.image.load(os.path.join('running_man_2', x)), (PLAYER_WIDTH, PLAYER_HEIGHT))
    for x in sorted(os.listdir('running_man'))]
monster_image = [pygame.transform.scale(pygame.image.load(os.path.join('monster', x)), (MONSTER_WIDTH, MONSTER_HEIGHT))
                 for x in sorted(os.listdir('monster'))]
standing_man = running_man[0]
bg = pygame.image.load('ground_seamless_texture_1668.jpg')
obstacle_image = pygame.image.load('granite_seamless_texture_3635.jpg')
finishing_line_image = pygame.transform.scale(pygame.image.load('finish_lineimg.png'), (1000, 650))
pygame.display.set_icon(pygame.transform.rotate(monster_image[0],180))


def draw_window(players, camera_speed, camera_position, frame_num, monster, obstacles, finishing_line):
    WIN.fill(BLACK)
    WIN.blit(bg, (0, camera_position % 1000))
    WIN.blit(bg, (0, - 1000 + camera_position % 1000))
    # print(camera_position, camera_position % 1000, ((camera_position // 1000) * 1000) - 1000 + camera_position)
    finishing_line.screen_y -= camera_speed
    WIN.blit(finishing_line_image, (finishing_line.x, finishing_line.screen_y))

    for obstacle in obstacles:
        obstacle.screen_y -= camera_speed
        WIN.blit(obstacle_image, (obstacle.x, obstacle.screen_y), (0, 0, obstacle.width, obstacle.height))

    for player_num, player in enumerate(players):
        player.screen_y += player.ver_vel - camera_speed
        man = running_man_2 if player_num else running_man
        rotimage = pygame.transform.rotate(man[int(player.walk_count // 3)],
                                           player.angle + 180)
        WIN.blit(rotimage, (player.x, player.screen_y))

        # pygame.draw.rect(WIN, BLACK, player.get_rect(), 1)
        # print(player.get_rect())

    # pygame.draw.rect(WIN, BLACK,
    #                  (players[0].x + PLAYER_WIDTH / 2 - 16, players[0].screen_y + PLAYER_HEIGHT / 2 + 2, 32, 32), 1)
    # WIN.blit(obstacle_image, (players[0].x + PLAYER_WIDTH / 2, players[0].screen_y + 15), (0, 0, 20, 32))

    if frame_num > FPS * 2:
        monster.max_distance = 900
        monster.speed = -3
        for player in players:
            if player.screen_y > 650:
                monster.max_distance = 775
                break
        monster.screen_y = min(monster.screen_y + monster.speed - camera_speed, monster.max_distance)
        # print(monster.screen_y)
    WIN.blit(monster_image[(int((frame_num // 4)) % 2)], (monster.x, monster.screen_y))

    for i, text in enumerate(['3', '2', '1', 'GO!']):
        if FPS * i < frame_num < FPS * (i + 1):
            draw_text_on_screen(text, COUNTDOWN_FONT)

    pygame.display.update()


def handle_player_movement(keys_pressed, player, obstacles, speed):
    # definitions
    directions = ['left', 'down', 'right', 'up']
    angles_dict = {'left': 90, 'down': 180, 'right': 270, 'up': 0}
    direction_signs = {x: -1 if x in ['left', 'up'] else 1 for x in directions}
    directions_pressed = []

    # basic velocity adjustments
    for direction in directions:
        if direction in ['left', 'right']:
            if keys_pressed[player.controls[direction]]:
                directions_pressed.append(direction)
                if player.speed < speed:
                    player.hor_vel += 0.25 * direction_signs[direction]
                else:
                    vel_added = 0
                    while abs(player.hor_vel) < abs(player.ver_vel) and vel_added <= 0.25:
                        player.hor_vel += 0.01 * direction_signs[direction]
                        player.ver_vel = np.sign(player.ver_vel) * (abs(player.ver_vel) - 0.01)
                        vel_added += 0.01
            elif np.sign(player.hor_vel) == direction_signs[direction]:
                player.hor_vel -= min(0.5, abs(player.hor_vel)) * direction_signs[direction]
        else:
            if keys_pressed[player.controls[direction]]:
                directions_pressed.append(direction)
                if player.speed < speed:
                    player.ver_vel += 0.25 * direction_signs[direction]
                else:
                    vel_added = 0
                    while abs(player.ver_vel) < abs(player.hor_vel) and vel_added <= 0.25:
                        player.ver_vel += 0.01 * direction_signs[direction]
                        player.hor_vel = np.sign(player.hor_vel) * (abs(player.hor_vel) - 0.01)
                        vel_added += 0.01
            elif np.sign(player.ver_vel) == direction_signs[direction]:
                player.ver_vel -= min(0.25, abs(player.ver_vel)) * direction_signs[direction]

    # collisions
    for obstacle in obstacles:
        player_rect = player.get_rect()
        prev_player_rect = player.prev_rect
        player_point_dict = {'TL': player_rect.topleft, 'BL': player_rect.bottomleft,
                             'TR': player_rect.topright, 'BR': player_rect.bottomright}
        prev_player_point_dict = {'TL': prev_player_rect.topleft, 'BL': prev_player_rect.bottomleft,
                                  'TR': prev_player_rect.topright, 'BR': prev_player_rect.bottomright}
        for player_point in player_point_dict:
            if obstacle.rect.collidepoint(*player_point_dict[player_point]):
                if np.sign(player.hor_vel) == -1:
                    vertical_side = (obstacle.rect.topright, obstacle.rect.bottomright)
                else:
                    vertical_side = (obstacle.rect.topleft, obstacle.rect.bottomleft)
                # if np.sign(player.ver_vel) == -1:
                #     horizontal_side = (obstacle.rect.bottomleft, obstacle.rect.bottomright)
                # else:
                #     horizontal_side = (obstacle.rect.topleft, obstacle.rect.topright)
                player_line = (prev_player_point_dict[player_point], player_point_dict[player_point])
                if helpers.intersect(player_line, vertical_side):
                    player.hor_vel = np.sign(player.hor_vel) * (-3)
                else:
                    player.ver_vel = np.sign(player.ver_vel) * (-3)
                break

    # set speed
    player.speed = math.sqrt(player.hor_vel ** 2 + player.ver_vel ** 2)

    # walk count
    if player.speed:
        player.walk_count = (player.walk_count + round(player.speed) / 5) % 24
    else:
        player.walk_count = 0

    # angle
    av_angle = round(np.mean([angles_dict[x] for x in directions_pressed] if directions_pressed else 0))
    player.angle = av_angle - av_angle % 45 if directions_pressed else player.angle

    # adjusting coordinates
    player.prev_rect = player.get_rect()
    if 0 < player.x + player.hor_vel < WIDTH - player.width:
        player.x += player.hor_vel
    player.y += player.ver_vel


class Player:
    def __init__(self, name, x, y, controls):
        self.name = name
        self.x = x
        self.y = y
        self.screen_y = max(y, 200)
        self.angle = 0
        self.controls = controls
        self.walk_count = 0
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.rect = pygame.Rect(self.x, self.screen_y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.hor_vel = 0
        self.ver_vel = 0
        self.speed = 0
        self.health = 10
        self.bullets = []
        self.prev_rect = self.get_rect()

    def get_rect(self):
        if self.angle % 180 == 0:
            return pygame.Rect(self.x, self.y + 15, self.width, self.height - 28)
        if self.angle % 180 == 45:
            return pygame.Rect(self.x + 10, self.y + 20, self.width - 6, self.height - 20)
        if self.angle % 180 == 90:
            return pygame.Rect(self.x + 10, self.y, self.height - 28, self.width)
        if self.angle % 180 == 135:
            return pygame.Rect(self.x + 10, self.y + 25, self.width - 10, self.height - 20)


class FinishingLine:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.screen_y = y


class Monster:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.screen_y = max(y, 200)
        self.width = MONSTER_WIDTH
        self.height = MONSTER_HEIGHT
        self.rect = pygame.Rect(self.x, self.y, MONSTER_WIDTH, MONSTER_HEIGHT)
        self.speed = -3
        self.max_distance = 900

    def get_rect(self):
        return pygame.Rect(self.x, self.y, MONSTER_WIDTH, MONSTER_HEIGHT)


class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.screen_y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, width, height)
        self.wider_rect = pygame.Rect(self.x - PLAYER_WIDTH, self.y - PLAYER_HEIGHT,
                                      width + PLAYER_WIDTH * 2, height + PLAYER_HEIGHT * 2)
        self.overlap = 0
        self.against_boundary = False

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


# def get_computer_player_moves(player, frame_num, obstacles):
#     highest_point = 0
#     second_highest = 0
#     second_best = [['left']] * 6
#     for j in range(25):
#         sims = deepcopy(player)
#         sims.controls = P1_KEYS
#         keys_combo = []
#         for i in range(4):
#             keys = np.random.choice(np.array([['up'], ['up', 'right'], ['up', 'left']],
#                                              dtype=object))
#             keys_combo.append(keys)
#         for combo in keys_combo:
#             for k in range(10):
#                 converted_keys = {P1_KEYS[x]: True if x in combo else False for x in ['left', 'right', 'up', 'down']}
#                 handle_player_movement(converted_keys, sims, obstacles)
#         if sims.y < highest_point:
#             highest_point = sims.y
#             best_combo = keys_combo
#         elif sims.y < second_highest:
#             second_highest = sims.y
#             second_best = keys_combo
#     print(best_combo, highest_point, second_best, second_highest)

def get_computer_player_keys(player, gaps, bottom_gaps, obstacles, controls):
    target_bottom_gap = find_target_bottom_gap(player, gaps, bottom_gaps, obstacles)
    # print(target_bottom_gap)
    line = get_line_to_target_bottom_gap(player, target_bottom_gap)
    keys = get_keys(line, controls)
    return keys


def generate_obstacles(seed, number_of_obstacles):
    # definitions
    np.random.seed(seed)
    obstacles = []
    no_overlap = []
    single_overlap = []
    obstacles_against_boundary = []

    for i in range(number_of_obstacles):
        valid_obstacle = False
        obstacle_no_overlap = []
        obstacle_overlap = []
        too_close = False
        against_boundary = False
        creates_dead_end = False
        for j in range(400):
            obs_width = max(min(np.random.normal(300, 100), (WIDTH / 2) - PLAYER_WIDTH), 50)
            obs_height = max(50, np.random.normal(300, 100))
            obs_x = np.random.uniform(0, 900 - obs_width)
            obs_y = np.random.uniform(0, -10000 + obs_height)
            obstacle = Obstacle(obs_x, obs_y, obs_width, obs_height)

            # check if obstacle close to edge
            for x in [0, 900]:
                if obstacle.wider_rect.clipline((x, 0), (x, -10000)):
                    against_boundary = True

            # check if obstacle too close or overlapping with already overlapping obstacles
            if obstacle.wider_rect.collidelist([x.wider_rect for x in single_overlap]) != -1:
                continue

            # iterate through obstacles that currently do not overlap with other obstacles
            for obs in no_overlap:

                # check if new obstacle overlapping or close to obs
                if obstacle.wider_rect.colliderect(obs.wider_rect):

                    # if obs close to edge
                    if obs.against_boundary:

                        # if new (overlapping or close) obstacle below obs
                        if obs_y + obs_height > obs.y + obs.height:
                            creates_dead_end = True

                    if against_boundary:
                        if obs_y + obs_height < obs.y + obs.height:
                            creates_dead_end = True
                    if not obstacle.rect.colliderect(obs.rect):
                        too_close = True
                        break
                    else:
                        obstacle_overlap.append(obs)
                    if len(obstacle_overlap) >= 2:
                        break
                else:
                    obstacle_no_overlap.append(obs)
            if len(obstacle_overlap) < 2 and not too_close and not creates_dead_end:
                valid_obstacle = True
            if valid_obstacle:
                obstacles.append(obstacle)
                for obs in obstacle_overlap:
                    obs.overlap = 1
                    single_overlap.append(obs)
                if len(obstacle_overlap) > 0:
                    single_overlap.append(obstacle)
                else:
                    no_overlap.append(obstacle)
                if against_boundary:
                    obstacles_against_boundary.append(obstacle)
                    obstacle.against_boundary = True
                break
    return obstacles


def get_gaps(obstacles):
    unfiltered_gaps = []
    lines = [((0, x), (WIDTH, x)) for x in range(600, -12000, -3)]
    for line in lines:
        y_coordinate = line[0][1]
        obstacles_intersected = []
        for obstacle in obstacles:
            if obstacle.rect.clipline(line):
                obstacles_intersected.append(obstacle)
        obstacles_intersected.sort(key=lambda k: k.rect.left)
        obstacle_intersection_lines = []
        skip_next_obstacle = False
        for index, obstacle in enumerate(obstacles_intersected):
            if skip_next_obstacle:
                continue
            left_point = obstacle.rect.left
            if len(obstacles_intersected) > index + 1:
                if obstacle.rect.colliderect(obstacles_intersected[index + 1]):
                    if obstacles_intersected[index + 1].rect.right > obstacle.rect.right:
                        right_point = obstacles_intersected[index + 1].rect.right
                    else:
                        right_point = obstacle.rect.right
                    skip_next_obstacle = True
                else:
                    right_point = obstacle.rect.right
                    skip_next_obstacle = False
            else:
                right_point = obstacle.rect.right
                skip_next_obstacle = False
            obstacle_intersection_lines.append(((left_point, y_coordinate), (right_point, y_coordinate)))
        left_points = [x[0] for x in obstacle_intersection_lines] + [(WIDTH, y_coordinate)]
        right_points = [(0, y_coordinate)] + [x[1] for x in obstacle_intersection_lines]
        unfiltered_gaps += list(zip(right_points, left_points))
    gaps = [x for x in unfiltered_gaps if x[1][0] - x[0][0] > PLAYER_WIDTH]
    return gaps


def get_middle_and_bottom_gaps(gaps):
    middle_gaps = []
    bottom_gaps = []
    gap_group_dict = {}
    another_dict = {}
    group_num = 0
    for gap in gaps:
        gap_str = str(gap[0][0]) + str(gap[0][1]) + str(gap[1][0]) + str(gap[1][1])
        gap_above_str = str(gap[0][0]) + str(gap[0][1] - 3) + str(gap[1][0]) + str(gap[1][1] - 3)
        gap_below_str = str(gap[0][0]) + str(gap[0][1] + 3) + str(gap[1][0]) + str(gap[1][1] + 3)
        if gap_below_str in another_dict:
            key = another_dict.get(gap_below_str)
        elif gap_above_str in another_dict:
            key = another_dict.get(gap_above_str)
        else:
            key = group_num
            gap_group_dict[group_num] = []
            group_num += 1
        gap_group_dict[key].append(gap)
        another_dict[gap_str] = key
    for key in gap_group_dict:
        gap_group = gap_group_dict[key]
        middle_gap = gap_group[len(gap_group) // 2]
        middle_gaps.append(middle_gap)
        bottom_gap = gap_group[0]
        bottom_gaps.append(bottom_gap)
    bottom_gaps.append(((0, -20000), (900, -20000)))
    bottom_gaps.append(((PLAYER_WIDTH, -21000), (900 - PLAYER_WIDTH, -21000)))
    bottom_gaps.append(((PLAYER_WIDTH + 1, -22000), (900 - PLAYER_WIDTH - 1, -22000)))
    return middle_gaps, bottom_gaps


def find_target_bottom_gap(player, gaps, bottom_gaps, obstacles):
    head_top = player.get_rect().midtop
    head_left = player.get_rect().topleft
    head_right = player.get_rect().topright
    for gap in gaps:
        if player.get_rect().clipline(gap):
            higher_bottom_gaps = [g for g in bottom_gaps
                                  if g[0][1] < gap[0][1] and (g[0][0], g[1][0]) != (gap[0][0], gap[1][0])
                                  and head_top[1] > g[0][1]]
            sorted_higher_bottom_gaps = sorted(higher_bottom_gaps, key=lambda k: k[0][1], reverse=True)
            # for bottom_gaps in sorted_higher_bottom_gaps:

            target_bottom_gap = sorted_higher_bottom_gaps[0]
            next_gap_up = sorted_higher_bottom_gaps[1]
            up_vertical_lines = [(head_left, (head_left[0], -10000)), (head_right, (head_right[0], -10000))]
            line_to_next_one = (head_top, (np.mean([next_gap_up[0][0], next_gap_up[1][0]]),
                                           np.mean([next_gap_up[0][1], next_gap_up[1][1]])))
            easy_gap = False
            for _bottom_gap in sorted_higher_bottom_gaps:
                bottom_gap = ((_bottom_gap[0][0] + PLAYER_WIDTH, _bottom_gap[0][1]),
                              (_bottom_gap[1][0] - PLAYER_WIDTH, _bottom_gap[1][1]))
                if helpers.intersect(up_vertical_lines[0], bottom_gap) \
                        and helpers.intersect(up_vertical_lines[1], bottom_gap):
                    collides = False
                    v_lines = [((x[0][0], x[0][1]), (x[0][0], bottom_gap[0][1])) for x in up_vertical_lines]
                    for obstacle in obstacles:
                        if obstacle.rect.clipline(v_lines[0]) or obstacle.rect.clipline(v_lines[1]):
                            collides = True
                            break
                    if not collides:
                        target_bottom_gap = _bottom_gap
                        easy_gap = True
            can_reach_next_one = False
            if not easy_gap:
                if next_gap_up[0][1] != target_bottom_gap[0][1]:
                    can_reach_next_one = True
                    for obstacle in obstacles:
                        # if obstacle.rect.clipline(up_vertical_line):
                        #     break
                        if obstacle.rect.clipline(line_to_next_one):
                            can_reach_next_one = False
                            break
            break
    # print(target_bottom_gap, next_gap_up, can_reach_next_one, line_to_next_one)
    return next_gap_up if can_reach_next_one else target_bottom_gap
    # return target_bottom_gap


def get_line_to_target_bottom_gap(player, tbg):
    head_top = player.get_rect().midtop
    up_vertical_line = (head_top, (head_top[0], -10000))
    down_vertical_line = (head_top, (head_top[0], 1000))
    narrow_tbg = ((tbg[0][0] + PLAYER_WIDTH, tbg[0][1]), (tbg[1][0] - PLAYER_WIDTH, tbg[1][1]))
    if helpers.intersect(up_vertical_line, narrow_tbg):
        return up_vertical_line
    elif helpers.intersect(down_vertical_line, narrow_tbg):
        return down_vertical_line
    else:
        return (head_top, (np.mean([tbg[0][0], tbg[1][0]]), np.mean([tbg[0][1], tbg[1][1]])))


def get_keys(line, controls):
    angle = helpers.get_angle(line)
    rounded_angle = (round(angle / 45) * 45) % 360
    if angle == 0:
        combo = ['up']
    elif rounded_angle == 45 or 0 < angle < 45:
        combo = ['up', 'right']
    elif rounded_angle == 90:
        combo = ['right']
    elif rounded_angle == 135:
        combo = ['down', 'right']
    elif rounded_angle == 180:
        combo = ['down']
    elif rounded_angle == 225:
        combo = ['down', 'left']
    elif rounded_angle == 270:
        combo = ['left']
    elif rounded_angle == 315 or 315 < angle < 360:
        combo = ['up', 'left']
    converted_keys = {controls[x]: True if x in combo else False for x in ['left', 'right', 'up', 'down']}
    return converted_keys


def draw_text_on_screen(text, font):
    draw_text = font.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() /
                         2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()


def main():
    level, comp_or_player, player1_name, player2_name = 'easy', 'computer', 'Player 1', 'Player 2'
    while True:

        mixer.music.load('sound/jaws.ogg')
        mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)

        level, comp_or_player, player1_name, player2_name = main_menu(level, comp_or_player, player1_name, player2_name)

        camera_position = 0

        p1 = Player(player1_name, 700, 500, P1_KEYS)
        p2 = Player(player2_name, 100, 500, P2_KEYS)
        monster = Monster(35, 700)
        players = [p1, p2]

        finishing_line = FinishingLine(-50, -9730)

        if level == 'easy':
            speed = 8
        elif level == 'medium':
            speed = 9
        else:
            speed = 10

        if comp_or_player == 'player':
            speed = 9

        with open('sims_results.json', encoding='utf8') as infile:
            sims_results = json.load(infile)
        seeds = [int(x) for x in sims_results if [y for y in sims_results[x] if y['speed'] == speed and y['frames']]]
        seed = np.random.choice(seeds)
        clock = pygame.time.Clock()
        run = True
        frame_num = 0
        obstacles = generate_obstacles(seed, 50)
        gaps = get_gaps(obstacles)
        middle_gap, bottom_gaps = get_middle_and_bottom_gaps(gaps)
        winner_text = ""
        win_frame = 0
        countdown_sound.play()
        # print(len(obstacles))
        # gaps = get_gaps(obstacles)
        winner_already_established = False
        while run:
            clock.tick(FPS)
            frame_num += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
            if frame_num < 90:
                draw_window(players, 0, camera_position, frame_num, monster, obstacles, finishing_line)
                continue
            for player in players:
                opponent = [x for x in players if x != player][0]
                if player.y < -9500:
                    winner_text = f'{player.name.capitalize()} Wins!'
                if opponent.screen_y >= monster.screen_y:
                    if not winner_already_established:
                        death_sound.play()
                    winner_text = f'{player.name.capitalize()} Wins!'

            if winner_text != "":
                if not winner_already_established:
                    win_sound.play()
                    winner_already_established = True
                if not win_frame:
                    win_frame = frame_num
                draw_text_on_screen(winner_text, WINNER_FONT)
                if frame_num - win_frame > FPS * 5:
                    break
                else:
                    continue

            keys_pressed = pygame.key.get_pressed()
            # for player in players:
            # print(p2.get_rect())
            # computer_keys1 = get_computer_player_keys(p1, gaps, bottom_gaps, obstacles, P1_KEYS)
            # computer_keys2 = get_computer_player_keys(p2, gaps, bottom_gaps, obstacles, P2_KEYS)
            handle_player_movement(keys_pressed, p1, obstacles, 9)
            handle_player_movement(get_computer_player_keys(p2, gaps, bottom_gaps, obstacles, P2_KEYS)
                                   if comp_or_player == 'computer' else keys_pressed, p2, obstacles, speed)

            players_at_boundary = [player for player in players if player.screen_y <= 300]
            if players_at_boundary:
                camera_speed = min(*[player.ver_vel for player in players_at_boundary], 0)
            else:
                camera_speed = 0
            if p2.y <= -10000:
                print(frame_num)
            camera_position -= camera_speed
            draw_window(players, camera_speed, camera_position, frame_num, monster, obstacles, finishing_line)
            # print(players[0].y)
            # print(players[0].ver_vel, players[1].ver_vel, players[0].screen_y, players[1].screen_y,
            #       players[0].y, players[1].y, camera_speed)
        # return players[0], frame_num, obstacles


if __name__ == "__main__":
    # player, frame_num, obstacles = main()
    # now = datetime.now()
    # get_computer_player_moves(player, frame_num, obstacles)
    # print((datetime.now() - now).total_seconds())
    main()
