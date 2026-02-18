from PIL import ImageGrab
def capture_region(left,top, right, bottom):
    if(left<0):
        left = 0
    """
    Captures a specific region of the screen
    Args:
        top (int): Top coordinate  
        left (int): Left coordinate
        bottom (int): Bottom coordinate
        right (int): Right coordinate
    """
    # Define the region to capture (left, top, right, bottom)
    bbox = (left, top, right, bottom)
    # Capture the specified region
    screenshot = ImageGrab.grab(bbox)
    return screenshot

def capture_full():
    """
    Captures a full screenshot using PIL and saves it 
    """
    # Capture the entire screen
    screenshot = ImageGrab.grab()
    return screenshot