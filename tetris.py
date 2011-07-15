import Tkinter as tk
from random import choice

class Game():
    WIDTH = 300
    HEIGHT = 500
    SPEED = 100

    def start(self):
        # Create the main window and the canvas
        self.root = tk.Tk()
        self.root.title("Tetris")
        self.canvas = tk.Canvas(
                self.root, 
                width=Game.WIDTH, 
                height=Game.HEIGHT)
        self.canvas.pack()

        # Create a first shape, start the timer, and start the app
        self.current_shape = Shape(self.canvas)
        self.timer()
        self.root.mainloop()
    
    def timer(self):
        move = True
        self.root.after(Game.SPEED, self.timer)

        for box in self.current_shape.boxes:
            # Stop if you reach the bottom of the window
            if Game.HEIGHT in self.canvas.coords(box):
                move = False

        for box in self.current_shape.boxes:
            if move == True: self.canvas.move(box, 0, 20)

        # If you stopped, make a new shape
        if move == False: self.current_shape = Shape(self.canvas)

class Shape:
    BOX_SIZE = 20
    START_POINT = Game.WIDTH / 2 / BOX_SIZE * BOX_SIZE - BOX_SIZE
    SHAPES = (
            ("yellow", (0, 0), (1, 0), (0, 1), (1, 1)),     # square
            ("lightblue", (0, 0), (1, 0), (2, 0), (3, 0)),  # line
            ("orange", (2, 0), (0, 1), (1, 1), (2, 1)),     # right el
            ("blue", (0, 0), (0, 1), (1, 1), (2, 1)),       # left el
            ("green", (0, 1), (1, 1), (1, 0), (2, 0)),      # right wedge
            ("red", (0, 0), (1, 0), (1, 1), (2, 1)),        # left wedge
            ("purple", (1, 0), (0, 1), (1, 1), (2, 1)),     # symmetrical wedge
            )

    def __init__(self, canvas):
        self.boxes = []
        self.shape = choice(Shape.SHAPES)
        self.color = self.shape[0]

        for point in self.shape[1:]:
            box = canvas.create_rectangle(
                point[0] * Shape.BOX_SIZE + Shape.START_POINT,
                point[1] * Shape.BOX_SIZE,
                point[0] * Shape.BOX_SIZE + Shape.BOX_SIZE + Shape.START_POINT,
                point[1] * Shape.BOX_SIZE + Shape.BOX_SIZE,
                fill=self.color)
            self.boxes.append(box)

if __name__ == "__main__":
    game = Game()
    game.start()
