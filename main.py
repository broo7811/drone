from codrone_edu.drone import *
import multiprocessing
from pynput.keyboard import Key, Listener
import time
bolRun = True
drone = Drone()
drone.pair()
def RunFunctions():
    print("1: Detecting Colors")
    print("2: Move And Turn")
    print("3: Elevation Detection")
    strFunctionCheck = str(input("input number or numbers (separated by spaces): "))
    global bolDetect_color
    global bolKey_Listener
    global bolMoveAndTurn
    global bolElevationDetection
    if "1" in strFunctionCheck:
        bolDetect_color = True
    else:
        bolDetect_color = False
    if "2" in strFunctionCheck:
        bolMoveAndTurn = True
    else:
        bolMoveAndTurn = False
    if "3" in strFunctionCheck:
        bolElevationDetection = True
    else:
        bolElevationDetection = False
def Detect_color():
    bolDetector = True
    with Listener(on_press=key_listener) as listener:
        while listener != 1:
            time.sleep(1)
            strColor = drone.get_colors()
            print(strColor)
            if strColor == "Yellow":
               print("yippee")


def key_listener(key):
    if key == Key.space:
        drone.emergency_stop()
        global bolRun
        bolRun = False
        return 1
    if key == Key.tab:
        drone.land()
        quit()

def ElevationDetection():
    drone.takeoff()
    battery = drone.get_battery()
    print("Battery: " + str(battery))
    time.sleep(4)
    intTracker = 1
    initialE = drone.get_pos_z()
    currentE = initialE
    while int(currentE) <= int(initialE) + 5 and int(currentE) >= int(initialE) - 5:
        time.sleep(1)
        currentE = drone.get_pos_z()
        print("Initial Elevation: " + str(int(initialE)))
        print("Current Elevation: " + str(int(currentE)))
    drone.land()

def EnvironmentDetection():
    pressure = drone.get_pressure() # unit: Pascals
    temp = drone.get_temperature()  # unit: Celsius
    battery = drone.get_battery()   # unit: percentage
    print("Air Pressure: " + pressure + " Pascals  ( " + (pressure / 101325) + " atm )" + "\n"
          "Temperature: " + temp + " Celsius  ( " + (drone.get_temperature("F")) + " F )" + "\n"
          "Battery: " + battery + "%")
def MoveAndTurn():
    drone.takeoff()
    battery = drone.get_battery()
    print("Battery: " + str(battery))
    time.sleep(2)
    intUserChoice = input("Input number of times it turns before landing: ")
    if intUserChoice == str:
        intUserChoice = 0
    intTracker = 1
    bolTest = True
    while bolTest:
        if drone.detect_wall(98):
            strColor = drone.get_color_data()
            print(strColor)
            drone.turn_left(90)
            print("wall detected")
            distance = drone.get_front_range()
            print("DISTANCE: " + str(distance))
            print(battery)
            if intTracker == int(intUserChoice):
                bolTest = False
            intTracker = intTracker + 1

        drone.set_pitch(50)
        drone.move_forward(0.5)
    drone.land()
    drone.close()
    global bolRun
    bolRun = False
    exit()

while bolRun:
    RunFunctions()
    with Listener(on_press=key_listener) as listener:
        if bolMoveAndTurn:
            threadMoveTurn = multiprocessing.Process(target=MoveAndTurn())
            threadMoveTurn.start()
            threadMoveTurn.join()
        if bolDetect_color:
            threadColor = multiprocessing.Process(target=Detect_color())
            threadColor.start()
            threadColor.join()
        if bolElevationDetection:
            threadElevation = multiprocessing.Process(target=ElevationDetection())
            threadElevation.start()
            threadElevation.join()
        listener.join()
drone.emergency_stop()
drone.close()