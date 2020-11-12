class BodyPart:
    def __init__(self, x, y, p_dir="left", w=20, h=20, head=False, tail=False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.is_head = head
        self.is_tail_and_has_turned = (tail, False)  # if tail and has turned
        self.p_dir = p_dir

    def move(self, change_pixels=20):
        if self.p_dir == "left":
            change = (-change_pixels, 0)
        elif self.p_dir == "right":
            change = (change_pixels, 0)
        elif self.p_dir == "up":
            change = (0, -change_pixels)
        else:
            change = (0, change_pixels)

        self.x += change[0]
        self.y += change[1]
