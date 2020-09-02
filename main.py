import pygame
import math
import sys

# Initialize game
pygame.init()

# Screen 
WIDTH = 300
HEIGHT = 320
HEADER = 20
ROWS = 3
BLOCK_BORDER = 1
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Images
X_IMAGE = pygame.transform.scale(pygame.image.load("x.png"), (80, 80))
O_IMAGE = pygame.transform.scale(pygame.image.load("o.png"), (80, 80))

# Fonts
STANDARD_FONT = pygame.font.SysFont('courier', 40)
X_SCORE_FONT = pygame.font.SysFont('courier', 18)
O_SCORE_FONT = pygame.font.SysFont('courier', 18)

# Global variables
score = {'x': 0, 'o': 0}

def draw_grid() :
    block_size = WIDTH // ROWS

    for y in range(ROWS) :
        for x in range(ROWS) :
            x_pos = x*block_size
            y_pos = y*block_size + HEADER
            rect = pygame.Rect(x_pos, y_pos, block_size, block_size)
            pygame.draw.rect(SCREEN, GRAY, rect, BLOCK_BORDER)

def draw_score() :
    score_area = pygame.Rect(0, 0, WIDTH, HEADER)
    SCREEN.fill(GRAY, rect = score_area)

    SCREEN.blit(X_SCORE_FONT.render("O : " + str(score['o']), True, BLUE), (5, 0))
    SCREEN.blit(X_SCORE_FONT.render("X : " + str(score['x']), True, RED), (5 + WIDTH//4, 0))

def initialize_grid():
    dis_to_cen = WIDTH // ROWS // 2

    # Initializing the array
    game_array = [[None, None, None], [None, None, None], [None, None, None]]

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x = dis_to_cen * (2 * j + 1)
            y = dis_to_cen * (2 * i + 1)

            # Adding centre coordinates
            game_array[i][j] = (x, y + HEADER, "", True)

    return game_array

def click(game_array):
    global turn, images

    # Mouse position
    m_x, m_y = pygame.mouse.get_pos()

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x, y, char, can_play = game_array[i][j]

            # Distance between mouse and the centre of the square
            dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)

            # If it's inside the square
            if dis < WIDTH // ROWS // 2 and can_play:
                if turn:  # If it's X's turn
                    images.append((x, y, X_IMAGE))
                    turn = False
                    game_array[i][j] = (x, y, 'x', False)

                else :  # If it's O's turn
                    images.append((x, y, O_IMAGE))
                    turn = True
                    game_array[i][j] = (x, y, 'o', False)

# Checking if someone has won
def has_won(game_array):
    # Checking rows
    for row in range(len(game_array)):
        if (game_array[row][0][2] == game_array[row][1][2] == game_array[row][2][2]) and game_array[row][0][2] != "":
            display_message(game_array[row][0][2].upper() + " has won!")
            return True

    # Checking columns
    for col in range(len(game_array)):
        if (game_array[0][col][2] == game_array[1][col][2] == game_array[2][col][2]) and game_array[0][col][2] != "":
            display_message(game_array[0][col][2].upper() + " has won!")
            return True

    # Checking main diagonal
    if (game_array[0][0][2] == game_array[1][1][2] == game_array[2][2][2]) and game_array[0][0][2] != "":
        display_message(game_array[0][0][2].upper() + " has won!")
        return True

    # Checking reverse diagonal
    if (game_array[0][2][2] == game_array[1][1][2] == game_array[2][0][2]) and game_array[0][2][2] != "":
        display_message(game_array[0][2][2].upper() + " has won!")
        return True

    return False

def has_drawn(game_array):
    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            if game_array[i][j][2] == "":
                return False

    display_message("It's a draw!")
    return True

def display_message(content):
    pygame.time.delay(500)
    SCREEN.fill(WHITE)
    end_text = STANDARD_FONT.render(content, 1, BLACK)
    SCREEN.blit(end_text, ((WIDTH - end_text.get_width()) // 2, (WIDTH - end_text.get_height()) // 2))
    pygame.display.update()
    pygame.time.delay(3000)

def render() :
    SCREEN.fill(WHITE)
    draw_score()
    draw_grid()

    for image in images:
        x, y, IMAGE = image
        SCREEN.blit(IMAGE, (x - IMAGE.get_width() // 2, y - IMAGE.get_height() // 2))

    pygame.display.update()

def main() :
    global turn, images

    images = []
    run = True
    turn = True

    game_array = initialize_grid()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click(game_array)

        render()

        if has_won(game_array) or has_drawn(game_array):
            run = False
            if(turn) :
                score['o'] += 1
            else :
                score['x'] += 1

while True :
    if __name__ == '__main__' :
        main()