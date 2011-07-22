import Tkinter as tk
from Tkinter import Canvas, Label, Tk
import tkMessageBox
from random import choice

class Game():
    WIDTH = 300
    HEIGHT = 500

    def start(self):
        '''Starts the game.

        Creates a window, a canvas, and a first shape. Binds the event handler.
        Then starts a GUI timer of ms interval self.speed and starts the GUI main 
        loop.

        '''
        self.level = 1
        self.score = 0
        self.speed = 10
        self.create_new_game = True

        self.root = Tk()
        self.root.title("Tetris")

        self.status = Label(self.root, 
                text="Level: %d, Score: %d" % (self.level, self.score), 
                font=("Helvetica", 10, "bold"))
        self.status.pack()
        
        self.canvas = Canvas(
                self.root, 
                width=Game.WIDTH, 
                height=Game.HEIGHT)
        self.canvas.pack()

        self.root.bind("<Key>", self.handle_events)
        self.timer()
        self.root.mainloop()
    
    def timer(self):
        '''Every self.speed ms, attempt to cause the current_shape to fall().

        If fall() returns False, create a new shape and check if it can fall.
        If it can't, then the game is over.
        
        '''
        if self.create_new_game == True:
            self.current_shape = Shape(self.canvas)
            self.create_new_game = False

        if not self.current_shape.fall():
            self.current_shape = Shape(self.canvas)
            if self._is_game_over(): 
                self.create_new_game = True
                self._game_over()

        self.root.after(self.speed, self.timer)

    def handle_events(self, event):
        '''Handle all user events.'''
        if event.keysym == "Left": self.current_shape.move(-1, 0)
        if event.keysym == "Right": self.current_shape.move(1, 0)
        if event.keysym == "Down": self.current_shape.move(0, 1)
        if event.keysym == "Up": self.current_shape.rotate()

    def _is_game_over(self):
        '''Check if a newly created shape is able to fall.

        If it can't fall, then the game is over.

        '''
        for box in self.current_shape.boxes:
            if not self.current_shape._can_move_box(box, 0, 1):
                return True
            return False

    def _game_over(self):
            self.canvas.delete(tk.ALL)
            tkMessageBox.showinfo(
                    "Game Over", 
                    "You scored %d points." % self.score)

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

           
    def move(self, x, y):
        '''Moves this shape (x, y) boxes.'''
        if not self._can_move_shape(x, y): 
            return False         
        else:
            for box in self.boxes: 
                self.canvas.move(box, x * Shape.BOX_SIZE, y * Shape.BOX_SIZE)
            return True

    def fall(self):
        '''Moves this shape one box-length down.'''
        if not self._can_move_shape(0, 1):
            return False
        else:
            for box in self.boxes:
                self.canvas.move(box, 0 * Shape.BOX_SIZE, 1 * Shape.BOX_SIZE)
            return True

    def rotate(self):
        '''Rotates the shape clockwise.'''
        boxes = self.boxes[:]
        pivot = boxes.pop(2)

        def get_move_coords(box):
            '''Return (x, y) boxes needed to rotate a box around the pivot.'''
            box_coords = self.canvas.coords(box)
            pivot_coords = self.canvas.coords(pivot)
            x_diff = box_coords[0] - pivot_coords[0]
            y_diff = box_coords[1] - pivot_coords[1]
            x_move = (- x_diff - y_diff) / self.BOX_SIZE
            y_move = (x_diff - y_diff) / self.BOX_SIZE
            return x_move, y_move

        # Check if shape can legally move
        for box in boxes:
            x_move, y_move = get_move_coords(box)
            if not self._can_move_box(box, x_move, y_move): 
                return False
            
        # Move shape
        for box in boxes:
            x_move, y_move = get_move_coords(box)
            self.canvas.move(box, 
                    x_move * self.BOX_SIZE, 
                    y_move * self.BOX_SIZE)

        return True

    def _can_move_box(self, box, x, y):
        '''Check if box can move (x, y) boxes.'''
        x = x * Shape.BOX_SIZE
        y = y * Shape.BOX_SIZE
        coords = self.canvas.coords(box)
        
        # Returns False if moving the box would overrun the screen
        if coords[3] + y > Game.HEIGHT: return False
        if coords[0] + x < 0: return False
        if coords[2] + x > Game.WIDTH: return False

        # Returns False if moving box (x, y) would overlap another box
        overlap = set(self.canvas.find_overlapping(
                (coords[0] + coords[2]) / 2 + x, 
                (coords[1] + coords[3]) / 2 + y, 
                (coords[0] + coords[2]) / 2 + x,
                (coords[1] + coords[3]) / 2 + y
                ))
        other_items = set(self.canvas.find_all()) - set(self.boxes)
        if overlap & other_items: return False

        return True


    def _can_move_shape(self, x, y):
        '''Check if the shape can move (x, y) boxes.'''
        for box in self.boxes:
            if not self._can_move_box(box, x, y): return False
        return True

if __name__ == "__main__":
    game = Game()
    game.start()
