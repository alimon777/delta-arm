import serial
import time
import math

frame_width = 640
frame_height = 480
plane_height = 415  # in mm
plane_circle_radius = 110
k = plane_height / frame_height
angshift=110 #take angshift as +ve if x-axis on paper is shifted counter-clockwise compared to the x-axis on screen

type_desc = ["Can","HDPE","PET_Bottle","Tetrapak"] # maintain the index as the bin number for sorting
type_height = [-280,-255,-258,-240] # maintain the same order as in type_desc for waste heights
e = 150.0  # end effector
f = 230.0  # base
re = 220.0
rf = 95.0
sqrt3 = math.sqrt(3.0)
pi = math.pi
sin120 = sqrt3 / 2.0
cos120 = -0.5
tan60 = sqrt3
sin30 = 0.5
tan30 = 1 / sqrt3

arduino_port = 'COM6'  # Change this to match your Arduino's port
baud_rate = 9600
ser = None

def connect_to_arduino():
    global ser
    try:
        ser = serial.Serial(arduino_port, baud_rate)
        time.sleep(2)
        print("Connected to Arduino.")
        return True
    except serial.SerialException:
        print("Arduino not detected. Please ensure it is connected and try again.")
        return False

def move_to_center_on_line(x, y):
    distance_to_origin = math.sqrt(x**2 + y**2)
    if distance_to_origin > plane_circle_radius:
        x -= x * (distance_to_origin - plane_circle_radius) / distance_to_origin
        y -= y * (distance_to_origin - plane_circle_radius) / distance_to_origin
    return x, y

def send_for_sorting(x,y,b):
    z = type_height[b]
    x,y = screenToPlane(x, y)
    ang1, ang2, ang3 = delta_calcInverse(-1 * x, y, z)
    if ang1 is None or ang2 is None or ang3 is None:
        x,y=move_to_center_on_line(x, y)
        print("object placed out of circle x,y resolved to :", x , y)
        ang1, ang2, ang3 = delta_calcInverse(-1 * x, y, z)
    while ang1 is None or ang2 is None or ang3 is None:
        x += -1 if x >= 0 else 1
        y += -1 if y >= 0 else 1
        print("single point adjustment to :",x ,y )
        ang1, ang2, ang3 = delta_calcInverse(-1 * x, y, z)
    
    tang1, tang2, tang3 = delta_calcInverse(-1 * x, y, z+30)
    if tang1 is None or tang2 is None or tang3 is None:
        x,y=move_to_center_on_line(x, y)
        print("object placed out of circle x,y resolved to :", x , y)
        tang1, tang2, tang3 = delta_calcInverse(-1 * x, y, z+30)
    while tang1 is None or tang2 is None or tang3 is None:
        x += -1 if x >= 0 else 1
        y += -1 if y >= 0 else 1
        print("single point adjustment to :",x ,y )
        tang1, tang2, tang3 = delta_calcInverse(-1 * x, y, z+30)



    # angles_str = f"<{ang1},{ang2},{ang3}>"
    angles_str = f"<{ang1},{ang2},{ang3},{tang1},{tang2},{tang3},{b}>"
    # Send string to Arduino
    angles_str = angles_str.strip() + '\n'  # Ensure the string is terminated properly
    ser.write(angles_str.encode())
    print(f"<{ang1},{ang2},{ang3}> coordinates were sent to arduino...")
    print(type_desc[b],"sorting in progress...")
    # Wait for acknowledgment from Arduino
    received_ack = ser.readline().decode().strip()
    if received_ack.startswith("<ACK>"):
        print("Sorted", type_desc[b])
    else:
        print("Unexpected response from Arduino :", received_ack)

def delta_calcAngleYZ(x0, y0, z0):
    y1 = -0.5 * 0.57735 * f  # f/2 * tg 30
    y0 -= 0.5 * 0.57735 * e  # shift center to edge
    a = (x0 * x0 + y0 * y0 + z0 * z0 + rf * rf - re * re - y1 * y1) / (2 * z0)
    b = (y1 - y0) / z0
    d = -(a + b * y1) * (a + b * y1) + rf * (b * b * rf + rf)
    if d < 0:
        return None
    yj = (y1 - a * b - math.sqrt(d)) / (b * b + 1)
    zj = a + b * yj
    theta = 180.0 * math.atan(-zj / (y1 - yj)) / pi + (180.0 if yj > y1 else 0.0)
    return theta

# Function to calculate inverse kinematics
def delta_calcInverse(x0, y0, z0):
    theta1 = delta_calcAngleYZ(x0, y0, z0)
    theta2 = delta_calcAngleYZ(x0 * cos120 + y0 * sin120, y0 * cos120 - x0 * sin120, z0)
    theta3 = delta_calcAngleYZ(x0 * cos120 - y0 * sin120, y0 * cos120 + x0 * sin120, z0)
    if theta1 is None or theta2 is None or theta3 is None:
        return None, None, None
    else:
        return round(theta1), round(theta2), round(theta3)
    
def screenToPlane(x, y):
    # shifting (0,0) from top-left of screen to center
    x = x - (frame_width / 2)  
    y = (frame_height / 2) - y 
    print("after shifting : x =", x, ", y =",y)
    # change pixel to mm
    x *= k 
    y *= k 
    print("after scaling : x =", x, ", y =",y)    
    #to rotate the coordinates if the x,y lines on the screen and surface don't match
    costheta = math.cos(math.radians(angshift))
    sintheta = math.sin(math.radians(angshift))
    # print("cos theta : " , costheta, "sin theta : " , sintheta)
    xplane= (x*costheta)+(y*sintheta)
    yplane= (y*costheta)-(x*sintheta)
    print("after rotating : x =", xplane, ", y =",yplane)
    return xplane, yplane

def segregate(x, y):
    # Attempt to connect to Arduino
    global ser
    while not ser:
        if not connect_to_arduino():
            time.sleep(3)  # Wait for 3 seconds before attempting to reconnect

    # x, y = map(float, input("Enter the coordinates (x,y) : ").split())
    b = 0
    send_for_sorting(x,y,b)