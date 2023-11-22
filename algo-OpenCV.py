import cv2
import numpy as np 

#image_path = "newGood/randomGraph50_80.png"
folder_path = "newGood/"
image_path = "randomGraph50_80.png"

#load image
image = cv2.imread(folder_path + image_path)

def drawCircles(detected_circles, image):

  #Convert the circle parameters a, b and r to integers. 
  detected_circles = np.uint16(np.around(detected_circles)) 
  
  for pt in detected_circles[0, :]: 
    a, b, r = pt[0], pt[1], pt[2] 
    #Draw the circumference of the circle. 
    cv2.circle(image, (a, b), r, (0, 255, 0), 2) 

    #Draw a small circle (of radius 1) to show the center. 
    cv2.circle(image, (a, b), 1, (0, 0, 255), 3) 
  
  cv2.imwrite("detected circles.png",image)


def drawEdges(lines_list, image):
  for p1, p2 in lines_list:
    cv2.line(image, p1, p2, (0,255,0), 2)

  cv2.imwrite('detected lines.png', image)


def detectCircles(image): #https://www.geeksforgeeks.org/circle-detection-using-opencv-python/
  #Creating kernel 
  kernel = np.ones((5, 5), np.uint8)

  #erode and then dilate image to remove edges (For some reason the functions to the opposite of what they should do)
  image_circles = cv2.dilate(image, kernel, iterations = 1)  
  image_circles = cv2.erode(image_circles, kernel, iterations = 1)  
  #Convert to grayscale. 
  gray = cv2.cvtColor(image_circles, cv2.COLOR_BGR2GRAY) 

  detected_circles = cv2.HoughCircles(gray,  
                  cv2.HOUGH_GRADIENT, 1, 25, param1 = 30, 
              param2 = 13.49, minRadius = 8, maxRadius = 40) 
  
  cv2.imwrite("Circles.png", image_circles)
  drawCircles(detected_circles, image_circles)

  return detected_circles

def detectEdges(img): #https://www.geeksforgeeks.org/line-detection-python-opencv-houghline-method/

  circles = cv2.imread("Circles.png")
  no_circles = cv2.subtract(circles, img)
  cv2.imwrite("Image without Circles.png", no_circles)

  #Convert image to grayscale
  gray = cv2.cvtColor(no_circles,cv2.COLOR_BGR2GRAY)
  
  #Use canny edge detection
  edges = cv2.Canny(gray,50,150,apertureSize=3)
  #Apply HoughLinesP method to 
  #to directly obtain line end points
  lines_list =[]
  lines = cv2.HoughLinesP(
              edges, #Input edge image
              1, #Distance resolution in pixels
              np.pi/180, #Angle resolution in radians
              threshold=40, #Min number of votes for valid line
              minLineLength=30, #Min allowed length of line
              maxLineGap=10 #Max allowed gap between line for joining them
              )
  
  #Iterate over points
  for points in lines:
    #Extracted points nested in the list
    x1,y1,x2,y2=points[0]

    #Maintain a simples lookup list for points
    lines_list.append([(x1,y1),(x2,y2)])
  
  drawEdges(lines_list, img)
  return lines_list


detected_circles = detectCircles(image)
edges = detectEdges(image)

  
