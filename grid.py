# grid.py
# accesses grid by block

class GridBlock:
    def __init__(self, canvas, x, y, size):
        # initialize grid
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size

        # initialize color
        self.color = "gray"

        # create grid
        self.rect = canvas.create_rectangle(
            x, y, x+size, y+size,
            fill=self.color, outline="black"
        )

    def set_color(self, color):
        self.color = color
        self.canvas.itemconfig(self.rect, fill=color)

    def isWithinBounds(self, px, py):
        return ((self.x <= px <= self.x + self.size) and (self.y <= py <= self.y + self.size))