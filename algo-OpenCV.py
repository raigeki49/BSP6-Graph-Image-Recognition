import cv2
import numpy as np 

#image_path = "newGood/randomGraph50_80.png"
folder_path = "mySimpleGraphs/"
image_path = "very simple graph3.png"

#load image
image = cv2.imread(folder_path + image_path)

def drawCircles(circles, image):

  #Convert the circle parameters a, b and r to integers. 
  circles = np.uint16(np.around(circles)) 
  
  for circle in circles: 
    a, b, r = circle 
    #Draw the circumference of the circle. 
    cv2.circle(image, (a, b), r, (0, 255, 0), 2) 

    #Draw a small circle (of radius 1) to show the center. 
    cv2.circle(image, (a, b), 1, (0, 0, 255), 3) 
  
  cv2.imwrite("detected circles.png",image)

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


def detectCircles(image): #https://www.geeksforgeeks.org/circle-detection-using-opencv-python/
  #Creating kernel 
  kernel = np.ones((5, 5), np.uint8)

  #erode and then dilate image to remove edges (For some reason the functions to the opposite of what they should do)
  image_circles = cv2.dilate(image, kernel, iterations = 5)  
  image_circles = cv2.erode(image_circles, kernel, iterations = 5)  
  #Convert to grayscale. 
  gray = cv2.cvtColor(image_circles, cv2.COLOR_BGR2GRAY) 

  detected_circles = cv2.HoughCircles(gray,  
                  cv2.HOUGH_GRADIENT, 1, 100, param1 = 15, 
              param2 = 14, minRadius = 114, maxRadius = 125) 
  
  cv2.imwrite("Circles.png", image_circles)

  circles = []
  for pt in detected_circles[0, :]: 
    a, b, r = pt[0], pt[1], pt[2] 

    circles.append((a,b,r))

  drawCircles(circles, image_circles)

  return circles

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
              2, #Distance resolution in pixels
              np.pi/180, #Angle resolution in radians
              threshold=55, #Min number of votes for valid line
              minLineLength=50, #Min allowed length of line
              maxLineGap=70 #Max allowed gap between line for joining them
              )
  
  #Iterate over points
  for points in lines:
    #Extracted points nested in the list
    x1,y1,x2,y2=points[0]

    #Maintain a simples lookup list for points
    lines_list.append([x1,y1,x2,y2])
  
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
    threshold=10
    if px >= cx-r-threshold and px <= cx+r+threshold and py >= cy-r-threshold and py <= cy+r+threshold:
      return circle
  
  return False

def connectVertices(vertices, edges):
  adj_list = {}
  for v in vertices:
  	adj_list[v] = set()

  for edge in edges:
    v1 = checkIfInCircle((edge[0], edge[1]), vertices)
    v2 = checkIfInCircle((edge[2], edge[3]), vertices)
    if v1 and v2:
      adj_list[v1].add(v2)
      adj_list[v2].add(v1)
  
  return adj_list

def drawExtractedGraph(vertices, edges):
  blank_image = np.zeros((1000,1000,3), np.uint8)

  #Convert the circle parameters a, b and r to integers. 
  vertices = np.uint16(np.around(vertices)) 
  
  for v in vertices: 
    a, b, r = v 
    #Draw the circumference of the circle. 
    cv2.circle(blank_image, (a, b), r, (0, 255, 0), 2) 

    #Draw a small circle (of radius 1) to show the center. 
    cv2.circle(blank_image, (a, b), 1, (0, 0, 255), 3) 

  for edge in edges:
    x1,y1,x2,y2 = edge
    cv2.line(blank_image, (x1,y1), (x2,y2), (0,0,255), 2)

  cv2.imwrite("Extracted Graph.png", blank_image)

detected_circles = detectCircles(image)
edges = detectEdges(image)

adj_list = connectVertices(detected_circles, edges)

print(adj_list)

drawExtractedGraph(detected_circles, edges)


  
