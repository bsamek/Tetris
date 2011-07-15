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

        # Create a first shape
        self.current_shape = self.create_shape()

        # Start the timer and the GUI
        self.timer()
        self.root.mainloop()
    
    def timer(self):
        self.root.after(Game.SPEED, self.timer)
        if not self.current_shape.fall(self.canvas):
            self.current_shape = self.create_shape()
        
    def create_shape(self):
        return Shape(self.canvas)


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

    def move(self, canvas, x, y):
        '''Move this shape (x, y) boxes.'''
        for box in self.boxes:
            if Game.HEIGHT in canvas.coords(box):
                return False
        for box in self.boxes:
            canvas.move(box, x * Shape.BOX_SIZE, y * Shape.BOX_SIZE)
        return True

    def fall(self, canvas):
        '''Convenience function to move one box down.'''
        return self.move(canvas, 0, 1)

if __name__ == "__main__":
    game = Game()
    game.start()
