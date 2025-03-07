import pyautogui
distance = 500
while distance > 0:
        pyautogui.drag(distance, 0, duration=0.1)   # move right
        distance -= 5
        pyautogui.drag(0, distance, duration=0.1)   # move down
        pyautogui.drag(-distance, 0, duration=0.1)  # move left
        distance -= 5
        pyautogui.drag(0, -distance, duration=0.1)  # move up