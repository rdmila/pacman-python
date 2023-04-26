class GameConfig:
    maze = 'maze.txt'
    ghosts_count = 5
    pacman_position = [9, 18]
    ghost_position_left_up = [9, 14]
    ghost_position_right_down = [11, 8]
    pacman_speed = 1
    ghost_speed = 1
    cell_width = 31
    assert(cell_width % 2 == 1)
    cell_in_pixels = 31
