import Tkinter as tk
from random import choice

class Game():
    WIDTH = 300
    HEIGHT = 500
    SPEED = 100

    def start(self):
        '''Starts the game.

        1. Creates game window of WIDTH and HEIGHT
        2. Creates canvas
        3. Creates first shape on canvas
        4. Starts GUI timer of ms interval SPEED
        5. Starts the GUI main loop
        
        '''
        # Creates the main window and the canvas
        self.root = tk.Tk()
        self.root.title("Tetris")
        self.canvas = tk.Canvas(
                self.root, 
                width=Game.WIDTH, 
                height=Game.HEIGHT)
        self.canvas.pack()

        # Creates a first shape
        self.current_shape = self.create_shape()

        # Starts the timer and the GUI
        self.timer()
        self.root.mainloop()
    
    def timer(self):
        '''Every Game.SPEED ms, attempt to cause the current_shape to fall().

        If fall() returns False, create a new shape.
        
        '''
        self.root.after(Game.SPEED, self.timer)
        if not self.current_shape.fall(self.canvas):
            self.current_shape = self.create_shape()
        
    def create_shape(self):
        '''Create a new shape.'''
        return Shape(self.canvas)

class Shape:
    '''Defines a tetris shape.'''
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
        '''Create a shape.

        For each point in the shape definition given in the SHAPES dictionary,
        create a rectangle of size BOX_SIZE. Save the integer references to
        these rectangles in the self.boxes list.

        Args:
        canvas - the parent canvas on which the shape appears

        '''
        self.boxes = [] # the squares drawn by canvas.create_rectangle()
        self.shape = choice(Shape.SHAPES) # a random shape
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
        '''Move this shape (x, y) boxes.

        For each box in the list self.boxes, get its coordinates. If the box is
        at the bottom of the screen, return False. If moving the box would
        cause it to overlap an existing box, return False. Otherwise, move the
        box (x, y) * BOX_SIZE and return True.

        '''
        for box in self.boxes:
            coords = canvas.coords(box)
            
            # Returns False if shape is at bottom of screen
            if coords[3] == Game.HEIGHT:
                return False

            # Returns False if moving box (x, y) would overlap another box
            overlap = set(canvas.find_overlapping(
                    (coords[0] + coords[2]) / 2 + x * Shape.BOX_SIZE, 
                    (coords[1] + coords[3]) / 2 + y * Shape.BOX_SIZE, 
                    (coords[0] + coords[2]) / 2 + x * Shape.BOX_SIZE,
                    (coords[1] + coords[3]) / 2 + y * Shape.BOX_SIZE 
                    ))
            other_items = set(canvas.find_all()) - set(self.boxes)
            if overlap & other_items: return False
        
        # Moves the boxes
        for box in self.boxes:
            canvas.move(box, x * Shape.BOX_SIZE, y * Shape.BOX_SIZE)
        return True

    def fall(self, canvas):
        '''Convenience function to move a shape one box-length down.'''
        return self.move(canvas, 0, 1)

if __name__ == "__main__":
    game = Game()
    game.start()
