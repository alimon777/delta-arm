import math

frame_width = 640
frame_height = 480
pixelCircleRadius = 480
paperCircleRadius = 415  # in mm
k = paperCircleRadius / pixelCircleRadius

def rotateCoordinates(x, y, angshift):
    costheta = math.cos(math.radians(angshift))
    sintheta = math.sin(math.radians(angshift))
    print("cos theta : " ,costheta)
    print("sin theta : " ,sintheta)
    # if x-axis on paper is shifted counter-clockwise compared to the x-axis on screen
    xrot= (x*costheta)+(y*sintheta)
    yrot= (y*costheta)-(x*sintheta)
    return xrot,yrot

def convertToDelta(x, y):
    # coordinate change while shifting (0,0) from top-left of screen to center
    x = x - (frame_width / 2)  
    y = (frame_height / 2) - y 
    print("aftershift")
    print("x ",x)
    print("y ",y)
    #change pixel to mm
    x *= k 
    y *= k 
    print("afterscaling")
    print("x ",x)
    print("y ",y)
    
    #to rotate the coordinates if the x,y lines on the screen and surface don't match
    #take angshift as +ve if x-axis on paper is shifted counter-clockwise compared to the x-axis on screen
    #take angshift as -ve if x-axis on paper is shifted clockwise compared to the x-axis on screen

    x,y = rotateCoordinates(x, y, angshift=110) 
    print("afterrotating")
    print("xrot : " ,x)
    print("yrot : " ,y)
    return x, y
def main():
    # x1,y1= float(input("Enter coordinates of top-left corner of bounding box: "))
    # x2,y2= float(input("Enter coordinates of top-left corner of bounding box: "))
    # x=(x1+x2)/2
    # y=(y1+y2)/2
    
    # x = float(input("Enter the X-pixel centre coordinate of bounding box: "))
    # y = float(input("Enter the Y-pixel centre coordinate of bounding box: "))
    x = 390
    y = 296
    delta_x, delta_y = convertToDelta(x, y)
    print("Delta X:", delta_x)
    print("Delta Y:", delta_y)

if __name__ == "__main__":
    main()
