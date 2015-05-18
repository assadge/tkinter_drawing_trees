import tkinter
from tkinter.ttk import Combobox
from random import randint

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700

GRASS_BOTTOM = WINDOW_HEIGHT
GRASS_TOP = WINDOW_HEIGHT - 200
GRASS_COLOR = '#5e5' #green

TREE_INITIAL_BASE_X = 400
TREE_INITIAL_BASE_Y = 1
TREE_INITIAL_SIZE = 5

apple_trunk_color = 'brown'
apple_trunk_points = [
    (40, 45), (47.5, 52), (52.5, 50), (52.5, 50), (52.5, 90),
    (54, 93), (60, 100), (64, 103), (68, 106), (73, 110),
    (66, 107), (62, 103), (55, 100), (53, 103), (54, 108),
    (50, 115), (55, 109), (48, 103), (50, 100), (40, 105), (27, 107),
    (17, 116), (18, 105), (30, 102), (35, 100), (43, 90), (42.5, 45)
]

apple_leafs_color = 'green'
apple_leafs_points = [
    (42.5, 50), (47.5, 52), (52.5, 50), (60, 55),
    (80, 60), (90, 55), (95, 45), (102, 35), (95, 25),
    (97, 25), (80, 10), (70, 5), (62, 10), (50, 5),
    (35, 10), (20, 15), (15, 25), (10, 35), (15, 45),
    (10, 55), (20, 65), (35, 60), (42.5, 50)
]

leaf_color = 'green'
leaf_points = [
    (5, 3), (5.5, 1), (7, 0), (7, 2), (5, 3)
]

apple_color = 'red'
apple_points = [
    (5, 3), (6.5, 2.5), (8, 3), (8.5, 5.5),
    (7, 8), (5, 7.8), (3, 8), (1.5, 5.5),
    (2, 3), (3.5, 2.5), (5, 3)
]

stick_color = 'brown'
stick_points = [
    (5, 1), (5, 3)
]

apricot_color = 'orange'
apricot_points = [
    (3.1, 2.5), (5, 5), (3, 8), (1.5, 5.5), (2, 3), (3.5, 2.5), (3.1, 2.5)
]

plum_color = 'purple'
plum_points = [
    (3.1, 2.5), (5, 5), (3, 8), (1.5, 5.5), (2, 3), (3.5, 2.5), (3.1, 2.5)
]

def scaled_coordinates(points, base_x, base_y, size):
    scaled_coords = []
    for point in points:
        scaled_coords.append(size * point[0] + base_x)
        scaled_coords.append(size * point[1] + base_y)
    return scaled_coords


class Tree:
    def __init__(self, trunk_points, trunk_color, leafs_points, leafs_color, base_x, base_y, max_size):
        self.base_x = base_x
        self.base_y = base_y
        self.size = max_size
        self.max_size = max_size

        self.trunk = canvas.create_polygon(
            scaled_coordinates(trunk_points, self.base_x, self.base_y, self.size),
            fill='brown', smooth=True, outline='black'
        )
        self.leafs = canvas.create_polygon(
            scaled_coordinates(leafs_points, self.base_x, self.base_y, self.size),
            fill='green', smooth=True, outline='black'
        )

    def change_size(self, size):
        self.size = size
        scaled_trunk_coords = scaled_coordinates(
            apple_trunk_points, self.base_x, self.base_y, self.size
        )
        scaled_leafs_coords = scaled_coordinates(
            apple_leafs_points, self.base_x, self.base_y, self.size
        )

        canvas.coords(self.leafs, tkinter._flatten(scaled_leafs_coords))
        canvas.coords(self.trunk, tkinter._flatten(scaled_trunk_coords))


    def growing(self, i):
        if i <= self.max_size:
            self.change_size(i)
            canvas.after(10, self.growing, (i + 0.001))
            self.base_y += -0.1
            self.base_x += -0.05

    def generate_leaf(self):
        leaf_base_x = round(
            self.base_x + randint(round(10 * self.size), round(100 * self.size))
        )
        leaf_base_y = round(self.base_y + 45 * self.size)
        leaf = canvas.create_polygon(
            scaled_coordinates(leaf_points, leaf_base_x, leaf_base_y, self.size),
            fill='green', smooth=True
        )

        falling_place = randint(
            round(self.base_y + 100 * self.size),  round(self.base_y + 120 * self.size)
        )

        self.falling_leaf(leaf, leaf_base_x, leaf_base_y, falling_place)

    def falling_leaf(self, leaf, leaf_base_x, leaf_base_y, falling_place):
        leaf_base_y += 5
        if leaf_base_y < falling_place:
            scaled_leaf_coords = scaled_coordinates(
                leaf_points, leaf_base_x, leaf_base_y, self.size
            )

            canvas.coords(leaf, tkinter._flatten(scaled_leaf_coords))
            canvas.after(
                30, self.falling_leaf, leaf, leaf_base_x, leaf_base_y, falling_place
            )

    def generate_fruit(self, fruit_points, fruit_color,
            leaf_points, leaf_color, stick_points, stick_color):
        if round(self.size, 2) == self.max_size:
            chance_to_grow = randint(1, 10)
            if chance_to_grow == 1:
                base_x = randint(
                    round(self.base_x + 20*self.size), round(self.base_x + 80*self.size)
                )
                base_y = randint(
                    round(self.base_y + 15*self.size), round(self.base_y + 50*self.size)
                )
                apple = Fruit(
                    fruit_points, fruit_color, leaf_points, leaf_color,
                    stick_points, stick_color,
                    self.base_y, base_x, base_y, self.max_size
                )
                apple.growing(0)
                canvas.tag_bind(
                    apple.fruit, '<ButtonPress-1>', lambda event,
                    apple=apple:onAppleClick(event, apple)
                )
        canvas.after(2000, self.generate_fruit, fruit_points, fruit_color,
            leaf_points, leaf_color, stick_points, stick_color)


class Fruit:
    def __init__(self, fruit_points, fruit_color, leaf_points, leaf_color,
            stick_points, stick_color, tree_base_y, base_x, base_y, max_size):

        self.isDisrupted = False
        self.base_x = base_x
        self.base_y = base_y
        self.tree_base_y = tree_base_y

        self.fruit_points = fruit_points
        self.fruit_color = fruit_color
        self.leaf_points = leaf_points
        self.leaf_color = leaf_color
        self.stick_points = stick_points
        self.stick_color = stick_color


        size = 0
        self.max_size = max_size

        self.leaf = canvas.create_polygon(
            scaled_coordinates(leaf_points, self.base_x, self.base_y, size),
            fill=leaf_color, smooth=True
        )

        self.fruit = canvas.create_polygon(
            scaled_coordinates(fruit_points, self.base_x, self.base_y, size),
            fill=fruit_color, smooth=True, outline='black'
        )

        self.stick = canvas.create_line(
            scaled_coordinates(stick_points, self.base_x, self.base_y, size),
            width=5, fill=stick_color, smooth=True
        )

    def change_size(self, size):
        self.size = size

        scaled_leaf_coords = scaled_coordinates(
            self.leaf_points, self.base_x, self.base_y, self.size
        )
        canvas.coords(self.leaf, tkinter._flatten(scaled_leaf_coords))

        scaled_fruit_coords = scaled_coordinates(
            self.fruit_points, self.base_x, self.base_y, self.size
        )
        canvas.coords(self.fruit, tkinter._flatten(scaled_fruit_coords))

        scaled_stick_coords = scaled_coordinates(
            self.stick_points, self.base_x, self.base_y, self.size
        )
        canvas.coords(self.stick, tkinter._flatten(scaled_stick_coords))

    def change_position(self, base_x, base_y):
        self.base_x = base_x
        self.base_y = base_y

        scaled_leaf_coords = scaled_coordinates(
            self.leaf_points, self.base_x, self.base_y, self.size
        )
        canvas.coords(self.leaf, tkinter._flatten(scaled_leaf_coords))

        scaled_fruit_coords = scaled_coordinates(
            self.fruit_points, self.base_x, self.base_y, self.size
        )
        canvas.coords(self.fruit, tkinter._flatten(scaled_fruit_coords))

        scaled_stick_coords = scaled_coordinates(
            self.stick_points, self.base_x, self.base_y, self.size
        )
        canvas.coords(self.stick, tkinter._flatten(scaled_stick_coords))
        # canvas.coords(self.leaf, self.base_x + 5 * self.size, self.base_y + 3 * self.size, self.base_x + 5.5 * self.size, self.base_y + 1 * self.size, self.base_x + 7 * self.size, self.base_y + 0 * self.size, self.base_x + 7 * self.size, self.base_y + 2 * self.size, self.base_x + 5 * self.size, self.base_y + 3 * self.size)
        # canvas.coords(self.fruit, self.base_x + 5 * self.size, self.base_y + 3 * self.size, self.base_x + 6.5 * self.size, self.base_y + 2.5 * self.size, self.base_x + 8 * self.size, self.base_y + 3 * self.size, self.base_x + 8.5 * self.size, self.base_y + 5.5 * self.size, self.base_x + 7 * self.size, self.base_y + 8 * self.size, self.base_x + 5 * self.size, self.base_y + 7.8 * self.size, self.base_x + 3 * self.size, self.base_y + 8 * self.size, self.base_x + 1.5 * self.size, self.base_y + 5.5 * self.size, self.base_x + 2 * self.size, self.base_y + 3 * self.size, self.base_x + 3.5 * self.size, self.base_y + 2.5 * self.size, self.base_x + 5 * self.size, self.base_y + 3 * self.size)
        # canvas.coords(self.stick, self.base_x + 5 * self.size, self.base_y + 1 * self.size, self.base_x + 5 * self.size, self.base_y + 3 * self.size)

    def growing(self, i):
        if i < self.max_size and not self.isDisrupted:
            self.change_size(i)
            canvas.after(10, self.growing, (i + 0.01))

    def falling(self, i):
        self.base_y += 5
        falling_place = randint(round(self.tree_base_y + 100 * self.max_size),  round(self.tree_base_y + 120 * self.max_size))
        if self.base_y < falling_place:

            self.change_position(self.base_x, self.base_y)
            window.after(30, self.falling, (i+1))

def windowdrag(event):
    chance_to_fall = randint(1, 100)
    if chance_to_fall == 5:
        if tree1 is not None:
            tree1.generate_leaf()
        if tree2 is not None:
            tree2.generate_leaf()
        if tree3 is not None:
            tree3.generate_leaf()


def onAppleClick(event, apple):
    apple.isDisrupted = True
    apple.falling(1)


def make_tree(event):
    global place1_occupied
    global place2_occupied
    global place3_occupied
    global tree1
    global tree2
    global tree3
    global leaf_points

    size = (200 - (700 - event.y)) / 50

    if event.x < 300 and not place1_occupied:
        place1_occupied = True
        tree1 = Tree(apple_trunk_points, apple_trunk_color,
                     apple_leafs_points, apple_leafs_color,
                     event.x, event.y, size
        )
        tree1.growing(0)
        tree1.generate_fruit(apple_points, apple_color,
            leaf_points, leaf_color, stick_points, stick_color)
    elif event.x > 400 and event.x < 600 and not place2_occupied:
        place2_occupied = True
        tree2 = Tree(apple_trunk_points, apple_trunk_color,
                     apple_leafs_points, apple_leafs_color,
                     event.x, event.y, size
        )
        tree2.growing(0)
        tree2.generate_fruit(apricot_points, apricot_color,
            leaf_points, leaf_color, stick_points, stick_color)
    elif event.x > 800 and not place3_occupied:
        place3_occupied = True
        tree3 = Tree(apple_trunk_points, apple_trunk_color,
                     apple_leafs_points, apple_leafs_color,
                     event.x, event.y, size
        )
        tree3.growing(0)
        tree3.generate_fruit(plum_points, plum_color,
            leaf_points, leaf_color, stick_points, stick_color)
    # tree = Tree(event.x, event.y, size)
    # tree.growing(0)

tree1 = None
tree2 = None
tree3 = None

place1_occupied = False
place2_occupied = False
place3_occupied = False

window = tkinter.Tk()
window.bind('<Configure>', windowdrag)
canvas = tkinter.Canvas(window, height=WINDOW_HEIGHT, width=WINDOW_WIDTH, bg='#bbe')

# tree = Tree(TREE_INITIAL_BASE_X, TREE_INITIAL_BASE_Y, TREE_INITIAL_SIZE)
tool_panel = tkinter.Frame(window, height=50, width=300)
tool_panel.pack()
tree_size_label = tkinter.Label(tool_panel, text='tree size: ')
tree_size_label.pack(side=tkinter.LEFT)
tree_size_combobox = Combobox(tool_panel, state='readonly', values=['1', '2', '3', '4'], width=10)
tree_size_combobox.pack()
grass = canvas.create_rectangle(0, GRASS_BOTTOM, WINDOW_WIDTH, GRASS_TOP, fill='#5e5')
canvas.tag_bind(grass, '<ButtonPress-1>', make_tree)
# tree.generate_apple()
# threading.Thread(target=tree.generate_apple).start()

canvas.pack()

window.mainloop()


