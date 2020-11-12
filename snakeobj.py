import pygame
from bodypart import BodyPart

pygame.init()


class Snake:
    def __init__(self, x, y, w, h, speed):
        self.head = BodyPart(x, y, "left", w, h, True, True)
        self.body_lst = [self.head]
        self.speed = speed # dont need
        self.turning = False
        self.turn_ind = -1
        self.turn_count = 0
        self.turns = []  # could be made a queue

    def add_body(self):
        curr_x, curr_y = self.body_lst[-1].x, self.body_lst[-1].y
        change = (0, 0)  # (X_change, y_change)
        if self.body_lst[-1].p_dir == "left":
            change = (self.head.w, 0)
        elif self.body_lst[-1].p_dir == "right":
            change = (-self.head.w, 0)
        elif self.body_lst[-1].p_dir == "up":
            change = (0, self.head.h)
        else:
            change = (0, -self.head.h)

        new_x, new_y = curr_x + change[0], curr_y + change[1]
        new_part = BodyPart(new_x, new_y, p_dir=self.body_lst[-1].p_dir, tail=True)
        self.body_lst[-1].is_tail_and_has_turned = (False, False)
        self.body_lst.append(new_part)

    def draw(self):
        rects = []
        for body_part in self.body_lst:
            rects.append((body_part.x, body_part.y, body_part.w, body_part.h))
        return rects

    def move(self):
        if len(self.turns) != 0:
            for x, y, direction in self.turns:
                for part in self.body_lst:
                    if part.x == x and part.y == y:
                        part.p_dir = direction
                        if part.is_tail_and_has_turned[0]:
                            part.is_tail_and_has_turned = (True, True)
            if self.body_lst[-1].is_tail_and_has_turned[1] and len(self.turns) != 0:
                self.turns.pop(0)
                self.body_lst[-1].is_tail_and_has_turned = (True, False)

        for part in self.body_lst:
            part.move()

    def turn(self, pos):
        self.turns.append(pos)
