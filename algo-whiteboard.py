import cv2
import numpy as np 
from math import *
import random

#image_path = "newGood/randomGraph50_80.png"
folder_path = "whiteboard/"
image_path = "whiteboard1.JPG"

#load image
image = cv2.imread(folder_path + image_path)

def drawCircles(circles, image):
  circles_image = np.zeros(shape=(image.shape), dtype=np.int16)

  #Convert the circle parameters a, b and r to integers. 
  circles = np.uint16(np.around(circles)) 
  
  for circle in circles: 
    a, b, r = circle 
    #Draw the circumference of the circle. 
    cv2.circle(circles_image, (a, b), r, (255, 255, 255), -1) 

  cv2.imwrite("Circles.png", circles_image)

def drawLines(lines_list, image):
  for l in lines_list:
    x1,y1,x2,y2=l
    color = tuple(np.random.randint(0, 256, size=3))
    color = ( int (color [ 0 ]), int (color [ 1 ]), int (color [ 2 ])) 
    cv2.line(image, (x1,y1), (x2,y2), color, 2)

  cv2.imwrite('detected Lines.png', image)


def drawEdges(lines_list, image):
  for l in lines_list:
    x1,y1,x2,y2=l
    cv2.line(image, (x1,y1), (x2,y2), (0,255,0), 2)

  cv2.imwrite('detected Edges.png', image)

def angle_trunc(a):
    while a < 0.0:
        a += pi * 2
    return a

def getAngleBetweenPoints(p1, p2):
    deltaY = p2[1] - p1[1]
    deltaX = p2[0] - p1[0]
    return angle_trunc(atan2(deltaY, deltaX))

def detectCircles(image): #https://www.geeksforgeeks.org/circle-detection-using-opencv-python/
  #Creating kernel 

  #Convert to grayscale. 
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

  detected_circles = cv2.HoughCircles(gray,  
                  cv2.HOUGH_GRADIENT, 1, 100, param1 = 80, 
              param2 = 60, minRadius = 3, maxRadius = 100) 
  
  #cv2.imwrite("Circles.png", image)

  circles = []
  for pt in detected_circles[0, :]: 
    a, b, r = pt[0], pt[1], pt[2] 

    circles.append((a,b,r))

  drawCircles(circles, image)

  return circles

def detectEdges(img): #https://www.geeksforgeeks.org/line-detection-python-opencv-houghline-method/

  #Convert image to grayscale
  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  
  #Use canny edge detection
  edges = cv2.Canny(gray,50,150,apertureSize=3)
  #Apply HoughLinesP method to 
  #to directly obtain line end points
  lines_list = []
  """
  lines = cv2.HoughLinesP(
              edges, #Input edge image
              2, #Distance resolution in pixels
              np.pi/180, #Angle resolution in radians
              threshold=40, #Min number of votes for valid line
              minLineLength=5, #Min allowed length of line
              maxLineGap=70 #Max allowed gap between line for joining them
              )"""
  iterations = 200 #bit high, but only way to consistently find all edges
  for i in range(iterations):
    detected_lines = cv2.HoughLinesP(
              edges, #Input edge image
              1, #Distance resolution in pixels
              np.pi/180, #Angle resolution in radians
              threshold = random.randint(1, 100), #Min number of votes for valid line
              minLineLength = random.randint(1, 50), #Min allowed length of line
              maxLineGap = random.randint(1, 100) #Max allowed gap between line for joining them
              )
    try:
      if i == 0:
        lines = detected_lines.copy()
      else:
        lines = np.append(lines, detected_lines.copy(), axis=0)
    except:
      continue

  #make the detected lines longer, so they go inside the vertices
  for points in lines:
    x1,y1,x2,y2=points[0]
    angle = getAngleBetweenPoints((x1,y1),(x2,y2)) #https://stackoverflow.com/questions/7586063/how-to-calculate-the-angle-between-a-line-and-the-horizontal-axis
    new_x1 = int(x1 - np.cos(angle)*10)
    new_y1 = int(y1 - np.sin(angle)*10)
    new_x2 = int(x2 + np.cos(angle)*10)
    new_y2 = int(y2 + np.sin(angle)*10)
    lines_list.append([new_x1,new_y1,new_x2,new_y2])
  
  drawLines(lines_list, img.copy())

  edges = mergeLinesToEdge(lines_list)

  drawEdges(edges,img.copy())

  return edges

def mergeLinesToEdge(lines_list):
  """
  edges = []
  for l1 in lines_list:
    lines_list.remove(l1)
    x11,y11,x12,y12=l1
    for l2 in lines_list:
      x21,y21,x22,y22=l2

      if abs(x11-x21)<10 and abs(y11-y21)<10 and abs(x12-x22)<10 and abs(y12-y22)<10: #dont know if there is guarantee that x11 and x21 are closest together and not x11 and x22
        lines_list.remove(l2)
        x1 = int((x11+x21)/2)
        y1 = int((y11+y21)/2)
        x2 = int((x12+x22)/2)
        y2 = int((y12+y22)/2)

        edges.append([x1,y1,x2,y2])

  return edges"""
  return lines_list

def checkIfInCircle(point,circles):
  for circle in circles:
    cx, cy, r = circle[0], circle[1], circle[2]
    px, py = point
    threshold=0
    if px >= cx-r-threshold and px <= cx+r+threshold and py >= cy-r-threshold and py <= cy+r+threshold:
      return circle
  
  return False

def connectVertices(vertices, edges):
  adj_list = {}
  true_edges = {}
  correct_edges = []
  for v in vertices:
  	adj_list[v] = set()

  for edge in edges:
    v1 = checkIfInCircle((edge[0], edge[1]), vertices)
    v2 = checkIfInCircle((edge[2], edge[3]), vertices)
    if v1 and v2 and (not(v1==v2)):     
      try:
        true_edges[tuple(sorted((v1,v2)))] += 1
      except:
        true_edges[tuple(sorted((v1,v2)))] = 0
      
  for edge in true_edges:
    if true_edges[edge] >= 0:
      correct_edges.append(edge)
  
  for edge in correct_edges:
    v1 = edge[0]
    v2 = edge[1]
    adj_list[v1].add(v2)
    adj_list[v2].add(v1)
  return adj_list, correct_edges

def drawExtractedGraph(vertices, edges, image):
  blank_image = np.zeros(shape=(image.shape), dtype=np.int16)

  #Convert the circle parameters a, b and r to integers. 
  vertices = np.uint16(np.around(vertices)) 
  
  for v in vertices: 
    a, b, r = v 
    #Draw the circumference of the circle. 
    cv2.circle(blank_image, (a, b), r, (0, 255, 0), 2) 

    #Draw a small circle (of radius 1) to show the center. 
    cv2.circle(blank_image, (a, b), 1, (0, 0, 255), 3) 

  for edge in edges:
    x1,y1 = edge[0][0:2]
    x2,y2 = edge[1][0:2]
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)
    cv2.line(blank_image, (x1,y1), (x2,y2), (0,0,255), 2)
    cv2.circle(blank_image, (x1, y1), 1, (0, 255, 0), 3) 
    cv2.circle(blank_image, (x2, y2), 1, (255, 0, 0), 3) 

  cv2.imwrite("Extracted Graph.png", blank_image)

detected_circles = detectCircles(image)
edges = detectEdges(image)

adj_list, true_edges = connectVertices(detected_circles, edges)

print(adj_list)

drawExtractedGraph(detected_circles, true_edges, image)


  
