import Tkinter as tk
from random import choice

class Game():
    WIDTH = 300
    HEIGHT = 500
    SPEED = 500

    def start(self):
        '''Starts the game.

        Creates a window, a canvas, and a first shape. Binds the event handler.
        Then starts a GUI timer of ms interval SPEED and starts the GUI main 
        loop.

        '''
        self.root = tk.Tk()
        self.root.title("Tetris")
        
        self.canvas = tk.Canvas(
                self.root, 
                width=Game.WIDTH, 
                height=Game.HEIGHT)
        self.canvas.pack()

        self.current_shape = self.create_shape()

        self.root.bind("<Key>", self.handle_events)
        self.timer()
        self.root.mainloop()
    
    def timer(self):
        '''Every Game.SPEED ms, attempt to cause the current_shape to fall().

        If fall() returns False, create a new shape.
        
        '''
        self.root.after(Game.SPEED, self.timer)
        if not self.current_shape.fall():
            self.current_shape = self.create_shape()
        
    def create_shape(self):
        '''Create a new shape.'''
        return Shape(self.canvas)

    def handle_events(self, event):
        '''Handle all user events.'''
        if event.keysym == "Left": self.current_shape.move(-1, 0)
        if event.keysym == "Right": self.current_shape.move(1, 0)
        if event.keysym == "Down": self.current_shape.move(0, 1)
        if event.keysym == "Up": self.current_shape.rotate()

class Shape:
    '''Defines a tetris shape.'''
    BOX_SIZE = 20
    # START_POINT relies on screwy integer arithmetic to approximate the middle
    # of the canvas while remaining correctly on the grid.
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

        Select a random shape from the SHAPES tuple. Then, for each point
        in the shape definition given in the SHAPES tuple, create a 
        rectangle of size BOX_SIZE. Save the integer references to these 
        rectangles in the self.boxes list.

        Args:
        canvas - the parent canvas on which the shape appears

        '''
        self.boxes = [] # the squares drawn by canvas.create_rectangle()
        self.shape = choice(Shape.SHAPES) # a random shape
        self.color = self.shape[0]
        self.canvas = canvas

        for point in self.shape[1:]:
            box = canvas.create_rectangle(
                point[0] * Shape.BOX_SIZE + Shape.START_POINT,
                point[1] * Shape.BOX_SIZE,
                point[0] * Shape.BOX_SIZE + Shape.BOX_SIZE + Shape.START_POINT,
                point[1] * Shape.BOX_SIZE + Shape.BOX_SIZE,
                fill=self.color)
            self.boxes.append(box)

    def _can_move(self, x, y):
        '''Check if the shape can move (x, y).
        
        For each box in the list self.boxes, get its coordinates. If moving
        the box would cause it to overrun the screen or overlap an existing 
        shape, return False. If all boxes pass these tests, return True.
        
        '''
        for box in self.boxes:
            coords = self.canvas.coords(box)
            
            # Returns False if moving the box would overrun the screen
            if coords[3] == Game.HEIGHT and y == 1: return False
            if coords[0] == 0 and x == -1: return False
            if coords[2] == Game.WIDTH and x == 1: return False

            # Returns False if moving box (x, y) would overlap another box
            overlap = set(self.canvas.find_overlapping(
                    (coords[0] + coords[2]) / 2 + x * Shape.BOX_SIZE, 
                    (coords[1] + coords[3]) / 2 + y * Shape.BOX_SIZE, 
                    (coords[0] + coords[2]) / 2 + x * Shape.BOX_SIZE,
                    (coords[1] + coords[3]) / 2 + y * Shape.BOX_SIZE 
                    ))
            other_items = set(self.canvas.find_all()) - set(self.boxes)
            if overlap & other_items: return False

        return True

    def move(self, x, y):
        '''Moves this shape (x, y) boxes.'''
        if not self._can_move(x, y): 
            return False         
        else:
            for box in self.boxes: 
                self.canvas.move(box, x * Shape.BOX_SIZE, y * Shape.BOX_SIZE)
            return True

    def fall(self):
        '''Moves this shape one box-length down.'''
        if not self._can_move(0, 1):
            return False
        else:
            for box in self.boxes:
                self.canvas.move(box, 0 * Shape.BOX_SIZE, 1 * Shape.BOX_SIZE)
            return True

    def rotate(self):
        '''Rotates the shape clockwise.'''
        boxes = self.boxes[:]
        pivot = boxes.pop(2)
        pivot_coords = self.canvas.coords(pivot)

        #TODO This for loop contains code very similar to _can_move. Refactor.
        for box in boxes:
            coords = self.canvas.coords(box)
            x = coords[0] - pivot_coords[0]
            y = coords[1] - pivot_coords[1]
            
            # Returns False if moving the box would overrun the screen
            if coords[3] + x - y > Game.HEIGHT: return False
            if coords[0] - x - y <  0: return False
            if coords[2] - x -y > Game.WIDTH: return False

            # Returns False if moving box (x, y) would overlap another box
            overlap = set(self.canvas.find_overlapping(
                    (coords[0] + coords[2]) / 2 - x - y, 
                    (coords[1] + coords[3]) / 2 + x - y, 
                    (coords[0] + coords[2]) / 2 - x - y,
                    (coords[1] + coords[3]) / 2 + x - y
                    ))
            other_items = set(self.canvas.find_all()) - set(self.boxes)
            if overlap & other_items: return False

        for box in boxes:
            coords = self.canvas.coords(box)
            x = coords[0] - pivot_coords[0]
            y = coords[1] - pivot_coords[1]
            self.canvas.move(box, -x-y, x-y)

        return True

if __name__ == "__main__":
    game = Game()
    game.start()
