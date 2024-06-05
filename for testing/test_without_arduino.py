import serial
import time
import math

# Define constants
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


def modAngle(ang):
    ang = 110 - ang
    if (ang < 0):
        ang = 0
    if (ang > 160):
        ang = 160
    return ang



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

def main():
    while True:
        xc, yc, zc = map(float, input("Enter the coordinates (xc, yc, zc): ").split())
        ang1, ang2, ang3 = delta_calcInverse(xc, yc, zc)
        if ang1 is None or ang2 is None or ang3 is None:
            print("Invalid coordinates! Unable to calculate angles.")
            continue
        print("Angles  before mod:",ang1,ang2,ang3)
        print("Angles:", modAngle(ang1), modAngle(ang2), modAngle(ang3))

if __name__ == "__main__":
    main()
