BLACK = (0, 0, 0)

# define display surface
WIDTH, HEIGHT = 1000, 600

# Player properties
PLAYER_ACC = 2
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 1.5

DIRECTION = ("left", "right")

# Starting platforms
PLATFORM_LIST = [(-2000, HEIGHT - 70, WIDTH * 4, 70),
                 (50, HEIGHT - 200, 70, 200),
                 (150, HEIGHT - 200, 70, 200),
                 (900, HEIGHT - 200, 70, 200),
                 (-900, HEIGHT - 200, 70, 200),
                 ]
