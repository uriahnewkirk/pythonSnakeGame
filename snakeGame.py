import tkinter
import random
import math

rows = 25
columns = 25
tile_size = 25

window_width = tile_size * columns
window_height = tile_size * rows

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y


#create game window
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)
canvas = tkinter.Canvas(window, background="black", width=window_width, height=window_height, borderwidth=0, highlightthickness=0)
canvas.pack()
canvas.update()

#make sure to center the game window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_x = int((screen_width/2) - (window_width/2));
window_y = int((screen_height/2) - (window_height/2));
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}");


#initialize game board & starting variables
snake = Tile(tile_size * 5, tile_size * 5)
food = Tile(tile_size * 10, tile_size * 10)
velocityX = 0;
velocityY = 0;
snakeBody = [];
gameOver = False;
score = 0;


def changeDirection(e):
    global velocityX, velocityY, gameOver
    if (gameOver):
        #reset game variables as well :)
        return
    
    if (e.keysym == "Up" and velocityY != 1):
        velocityX = 0
        velocityY = -1
    
    elif (e.keysym == "Down" and velocityY != -1):
        velocityX = 0
        velocityY = 1
    
    elif (e.keysym == "Left" and velocityX != 1):
        velocityX = -1
        velocityY = 0

    elif (e.keysym == "Right" and velocityX != -1):
        velocityX = 1
        velocityY = 0


#detect player's input and move snake
def move():
    global snake, food, snakeBody, gameOver, score
    if (gameOver):
        return
    
    for tile in snakeBody:
        if (snake.x == tile.x and snake.y == tile.y):
            gameOver = True
            return
        
    #formula to detect collision with food
    if (snake.x == food.x and snake.y == food.y):
        snakeBody.append(Tile(food.x, food.y))
        food.x = random.randint(0, columns-1) * tile_size
        food.y = random.randint(0, rows-1) * tile_size
        score += 1
    
    #update the snake body location on the game board
    for w in range(len(snakeBody)-1, -1, -1):
        tile = snakeBody[w]
        if (w == 0):
            tile.x = snake.x
            tile.y = snake.y
        
        else:
            previousTile = snakeBody[w-1]
            tile.x = previousTile.x
            tile.y = previousTile.y

    snake.x += velocityX * tile_size
    snake.y += velocityY * tile_size


#draw game board
def draw():
    global snake, food, snakeBody, gameOver, score
    move()

    canvas.delete("all")

    #generate food
    canvas.create_rectangle(food.x, food.y, food.x + tile_size, food.y + tile_size, fill="red")
    canvas.create_rectangle(snake.x, snake.y, snake.x + tile_size, snake.y + tile_size, fill="lime green")
    
    for tile in snakeBody:
        canvas.create_rectangle(tile.x, tile.y, tile.x + tile_size, tile.y + tile_size, fill="lime green")

    if (gameOver):
        canvas.create_text(window_width/2, window_height/2, font="Arial 20", text= f"Game Over: {score}", fill="white")
    else:
        canvas.create_text(30, 20, font="Arial 10", text= f"Score: {score}", fill="white")
    
    window.after(100, draw)

draw()
window.bind("<KeyRelease>", changeDirection)
window.mainloop()