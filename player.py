import keyboard
import time
import mouse
from image import capture_region
from PIL import Image

def press_a():
    keyboard.press("a") 
def press_d():
    keyboard.press("d") 
def press_jump():
    keyboard.press("space") 
def click_mleft():
    mouse.click("left")
def click_mright():
    mouse.click("right")
def release_all():
    for key in ("a", "d", "space"):
        keyboard.release(key)


def move_mouse(x:int,y:int):
    x = x/1.25
    y = y/1.25
    #move x right and y down
    #abs = F =>relative to current location
    #abs = T =>move to absolute position x and y on the screen
    mouse.move(x, y, absolute=True,duration=0.2) 

def check_pixel_org(pixel:tuple):
    # around f04010 
    if(pixel[0]>230 and (pixel[1] > 54 and pixel[1]<75) and pixel[2]<25):
        return True
    return False

def check_pixel_blue(pixel:tuple):
    #around 206be5
    if((pixel[0] > 10 and pixel[0]<55)and (pixel[1] > 90 and pixel[1]<115) and pixel[2]>200):
        return True
    return False

def check_pixel_player(pixel:tuple):
    r, g, b = pixel
    return r > 200 and g > 200 and b > 200 and abs(r-g) < 20

class player:
    def __init__(self):
        self.pos_org = None
        self.pos_blue= None
    def move_left(self):
        release_all()
        press_a()
    def move_right(self):
        release_all()
        press_d()
    def jump(self):
        press_jump()
    def shoot(self):
        click_mleft()
    def block(self):
        click_mright()
    def get_initial_pos(self):
        orange_img = capture_region(0,300,640,1080) #orange
        blue_img = capture_region(1280,300,1920,1080) #blue
        width,height = orange_img.size
        org = None
        blue = None
        for i in range(0,width,3):
            for j in range(0,height,3):
                if org is None:
                    org_pixel = check_pixel_org(orange_img.getpixel((i, j)))
                    if org_pixel == True:  # strong red
                        org = (i,j+550)
                if blue is None:
                    blue_pixel = check_pixel_blue(blue_img.getpixel((i, j)))
                    if blue_pixel==True: 
                        blue = (i+1280,j+550)
                if org is not None and blue is not None:
                    self.pos_org = org
                    self.pos_blue = blue
        print(self.pos_org,"\t",self.pos_blue,"\n")
    def play(self):
        while not keyboard.is_pressed("esc"):
            move_mouse(self.pos_blue[0],self.pos_blue[1])
            self.shoot()
            self.block()
            self.jump()
            orange_img = capture_region(self.pos_org[0]-300,self.pos_org[1]-300,self.pos_org[0]+300,self.pos_org[1]+300) #orange
            blue_img = capture_region(self.pos_blue[0]-300,self.pos_blue[1]-300,self.pos_blue[0]+300,self.pos_blue[1]+300) #blue
            width,height = orange_img.size
            previous_org = self.pos_org
            previous_blue = self.pos_blue
            org_updated = False
            blue_updated = False
            timea = time.time()
            for i in range(0,width,3):
                if(not (org_updated and blue_updated)):
                    for j in range(0,height,3):
                        if(not (org_updated and blue_updated)):
                            if(not org_updated):
                                org_pixel = check_pixel_org(orange_img.getpixel((i, j)))
                                if(org_pixel == True):
                                    self.pos_org = (
                                        self.pos_org[0] - 300 + i,  # x
                                        self.pos_org[1] - 300 + j   # y
                                    )
                                    org_updated = True
                            if(not blue_updated):
                                blue_pixel = check_pixel_blue(blue_img.getpixel((i, j)))
                                if(blue_pixel == True):
                                    self.pos_blue = (
                                        self.pos_blue[0] - 300 + i,
                                        self.pos_blue[1] - 300 + j
                                    )

                                    blue_updated = True
            if(self.pos_blue[0]<0):
                self.pos_blue = (self.pos_blue[0]+300,self.pos_blue[1])
            if(self.pos_blue[1]>1080):
                self.pos_blue = (self.pos_blue[0],self.pos_blue[1]-300)
            if(self.pos_org[0]<0):
                self.pos_org = (self.pos_org[0]+300,self.pos_org[1])
            if(self.pos_org[1]>1080):
                self.pos_org = (self.pos_org[0],self.pos_org[1]-300)
            if(self.pos_org[0]-self.pos_blue[0]<0):
                release_all()
                self.move_right()
            if(self.pos_org[0]-self.pos_blue[0]>0):
                release_all()
                self.move_left()
            timeb = time.time()
            print(self.pos_org,"\t",self.pos_blue,"\t",(timeb-timea)*1000," ms","\n")
        release_all()

if __name__ =="__main__":
    time.sleep(2)
    P = player()
    P.get_initial_pos()
    P.play()