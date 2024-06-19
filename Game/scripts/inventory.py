
class Inventory:

    def __init__(self, img):
        self.slot_img = img
        self.current_selected = 0
        self.item_list = [None, None]
        self.max_slot = 2

    def remove_item(self):
        self.item_list[self.current_selected] = None

    def update(self, item=None):
        if item:
            if len(self.item_list) + 1 < self.max_slot:
                self.item_list.append(item)
        
    def render(self, surf, tile_size=16):
        
        for i in range(self.max_slot):
            pos = (i* tile_size, 0)
            if self.item_list[i]:
                surf.blit(self.item_list[i].animation.img(), pos)
                self.item_list[i].animation.update()

            img = self.slot_img[1 if i == self.current_selected else 0]
            img.set_alpha(100)
            surf.blit(img, pos)
