import tkinter
import threading
import time
from random import randint
top = tkinter.Tk()


def falling_leaf():
    base_x = randint(10*size, 100*size)
    base_y = 45 * size
    leaf = C.create_polygon(base_x + 5 * size, base_y + 3 * size, base_x + 5.5 * size, base_y + 1 * size, base_x + 7 * size, base_y + 0 * size, base_x + 7 * size, base_y + 2 * size, base_x + 5 * size, base_y + 3 * size,  smooth=True, fill='green')
    falling_place = randint(600, 700)
    while base_y < falling_place:
            base_y += 5
            time.sleep(0.03)
            C.coords(leaf, base_x + 5 * size, base_y + 3 * size, base_x + 5.5 * size, base_y + 1 * size, base_x + 7 * size, base_y + 0 * size, base_x + 7 * size, base_y + 2 * size, base_x + 5 * size, base_y + 3 * size)


def windowdrag(event):
    chance_to_fall = randint(1, 100)
    if chance_to_fall == 5:
        threading.Thread(target=falling_leaf).start()
top.bind('<Configure>', windowdrag)
C = tkinter.Canvas(top, height=700, width=1000, bg='#bbe')
C.create_rectangle(0, 700, 1000, 500, fill='#5e5')
scale = 1


size = 6
base_x = 0
base_y = 0

trunk_points = [
    (40, 45), (47.5, 52), (52.5, 50), (52.5, 50), (52.5, 90),
    (54, 93), (60, 100), (64, 103), (68, 106), (73, 110),
    (66, 107), (62, 103), (55, 100), (53, 103), (54, 108),
    (50, 115), (55, 109), (48, 103), (50, 100), (40, 105), (27, 107),
    (17, 116), (18, 105), (30, 102), (35, 100), (43, 90), (42.5, 45)
]

scaled_trunk_coords = []
for point in trunk_points:
    scaled_trunk_coords.append(size * point[0] + base_x)
    scaled_trunk_coords.append(size * point[1] + base_y)

trunk = C.create_polygon(scaled_trunk_coords, fill='brown', smooth=True)

leafs_points = [
    (42.5, 50), (47.5, 52), (52.5, 50), (60, 55),
    (80, 60), (90, 55), (95, 45), (102, 35), (95, 25),
    (97, 25), (80, 10), (70, 5), (62, 10), (50, 5),
    (35, 10), (20, 15), (15, 25), (10, 35), (15, 45),
    (10, 55), (20, 65), (35, 60), (42.5, 50)
]

scaled_leafs_coords = []
for point in leafs_points:
    scaled_leafs_coords.append(size * point[0] + base_x)
    scaled_leafs_coords.append(size * point[1] + base_y)

leafs = C.create_polygon(scaled_leafs_coords, fill='green', smooth=True)


class Apple:
    def __init__(self, base_x, base_y, size):
        self.isDisrupted = False
        self.base_x = base_x
        self.base_y = base_y

        self.size = size
        self.size *= scale
        self.leaf = C.create_polygon(base_x + 5 * size, base_y + 3 * size, base_x + 5.5 * size, base_y + 1 * size, base_x + 7 * size, base_y + 0 * size, base_x + 7 * size, base_y + 2 * size, base_x + 5 * size, base_y + 3 * size,  smooth=True, fill='green')
        self.apple = C.create_polygon(base_x + 5 * size, base_y + 3 * size, base_x + 6.5 * size, base_y + 2.5 * size, base_x + 8 * size, base_y + 3 * size, base_x + 8.5 * size, base_y + 5.5 * size, base_x + 7 * size, base_y + 8 * size, base_x + 5 * size, base_y + 7.8 * size, base_x + 3 * size, base_y + 8 * size, base_x + 1.5 * size, base_y + 5.5 * size, base_x + 2 * size, base_y + 3 * size, base_x + 3.5 * size, base_y + 2.5 * size, base_x + 5 * size, base_y + 3 * size, fill='red', smooth=True, outline='black')
        self.line = C.create_line(base_x + 5 * size, base_y + 1 * size, base_x + 5 * size, base_y + 3 * size, width=5, fill='brown', smooth=True)

    def change_size(self, size):
        self.size = size
        C.coords(self.leaf, self.base_x + 5 * size, self.base_y + 3 * size, self.base_x + 5.5 * size, self.base_y + 1 * size, self.base_x + 7 * size, self.base_y + 0 * size, self.base_x + 7 * size, self.base_y + 2 * size, self.base_x + 5 * size, self.base_y + 3 * size)
        C.coords(self.apple, self.base_x + 5 * size, self.base_y + 3 * size, self.base_x + 6.5 * size, self.base_y + 2.5 * size, self.base_x + 8 * size, self.base_y + 3 * size, self.base_x + 8.5 * size, self.base_y + 5.5 * size, self.base_x + 7 * size, self.base_y + 8 * size, self.base_x + 5 * size, self.base_y + 7.8 * size, self.base_x + 3 * size, self.base_y + 8 * size, self.base_x + 1.5 * size, self.base_y + 5.5 * self.size, self.base_x + 2 * self.size, self.base_y + 3 * self.size, self.base_x + 3.5 * self.size, self.base_y + 2.5 * self.size, self.base_x + 5 * self.size, self.base_y + 3 * self.size)
        C.coords(self.line, self.base_x + 5 * size, self.base_y + 1 * size, self.base_x + 5 * size, self.base_y + 3 * size)

    def change_position(self, base_x, base_y):
        self.base_x = base_x
        self.base_y = base_y
        C.coords(self.leaf, self.base_x + 5 * self.size, self.base_y + 3 * self.size, self.base_x + 5.5 * self.size, self.base_y + 1 * self.size, self.base_x + 7 * self.size, self.base_y + 0 * self.size, self.base_x + 7 * self.size, self.base_y + 2 * self.size, self.base_x + 5 * self.size, self.base_y + 3 * self.size)
        C.coords(self.apple, self.base_x + 5 * self.size, self.base_y + 3 * self.size, self.base_x + 6.5 * self.size, self.base_y + 2.5 * self.size, self.base_x + 8 * self.size, self.base_y + 3 * self.size, self.base_x + 8.5 * self.size, self.base_y + 5.5 * self.size, self.base_x + 7 * self.size, self.base_y + 8 * self.size, self.base_x + 5 * self.size, self.base_y + 7.8 * self.size, self.base_x + 3 * self.size, self.base_y + 8 * self.size, self.base_x + 1.5 * self.size, self.base_y + 5.5 * self.size, self.base_x + 2 * self.size, self.base_y + 3 * self.size, self.base_x + 3.5 * self.size, self.base_y + 2.5 * self.size, self.base_x + 5 * self.size, self.base_y + 3 * self.size)
        C.coords(self.line, self.base_x + 5 * self.size, self.base_y + 1 * self.size, self.base_x + 5 * self.size, self.base_y + 3 * self.size)


    def growing(self, i):

        if i < 5 and not self.isDisrupted:
            self.change_size(i)
            C.after(100, self.growing, (i + 0.01))


    def falling(self, i):

        self.base_y += 5
        falling_place = randint(600, 700)
        if self.base_y < falling_place:

            self.change_position(self.base_x, self.base_y)
            top.after(30, self.falling, (i+1))
            # time.sleep(0.03)




# def group_fall(list):
#     while list[len(list) - 1].base_y < 600
#         for apple in list:
#             apple.change_position(apple.base_x, apple.base_y + 5)
#             time.sleep(0.5)

def onAppleClick(event, apple):
    # threading.Thread(target=apple.falling).start()
    apple.isDisrupted = True
    apple.falling(1)
def clock():
    # apple = Apple(40, 34, 1)
    # apple2 = Apple(50, 545, 1)
    # apple3 = Apple(150, 123, 1)
    # apple4 = Apple(230, 454, 1)
    # apple5 = Apple(390, 340, 1)


    chance_to_grow = randint(1, 10)
    if chance_to_grow == 5:
        base_x = randint(20*size, 80*size)
        base_y = randint(15*size, 50*size)
        apple = Apple(base_x, base_y, 1)
        apple.growing(0)
        C.tag_bind(apple.apple, '<ButtonPress-1>', lambda event, apple=apple:
                                 onAppleClick(event, apple))
    C.after(2000, clock)

    # for i in range(0, 100):
    #     base_x = randint(20*size, 80*size)
    #     base_y = randint(15*size, 50*size)
    #     apple = Apple(base_x, base_y, 4)
    #     C.tag_bind(apple.apple, '<ButtonPress-1>', lambda event, apple=apple:
    #                         onAppleClick(event, apple))


    # apple.growing()
    # apple2.growing()
    # apple3.growing()
    # apple4.growing()
    # apple5.growing()
    #
    # apple.falling()
    # apple2.falling()
    # apple3.falling()
    # apple4.falling()
    # apple5.falling()

threading.Thread(target=clock).start()





C.pack()

top.mainloop()


