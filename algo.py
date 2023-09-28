from PIL import Image, ImageDraw
import numpy as np
import Vertex, Edge

image_path = "goodGraphs/graph3.png"

color_white = (255, 255, 255)
color_black = (0, 0, 0)
color_red = (237, 28, 36)
color_green = (34, 177, 76)

im = Image.open(image_path)
im = im.convert('RGB')

id = [[0 for i in range(im.size[0]) ] for i in range(im.size[1])]
Vertices = []
Edges = []
colors = {0}
#Identify the pixel
for j in range(1,im.size[1] - 1):
    for i in range(1,im.size[0] - 1):
        pixel = im.getpixel((i,j))
        #colors.add(pixel)
        if not(pixel == color_white):

            up_left_pixel = im.getpixel((i - 1,j - 1))
            up_pixel = im.getpixel((i,j - 1))
            up_right_pixel = im.getpixel((i + 1,j - 1))

            left_pixel = im.getpixel((i - 1,j))
            right_pixel = im.getpixel((i + 1,j))

            down_left_pixel = im.getpixel((i - 1,j + 1))
            down_pixel = im.getpixel((i,j + 1))
            down_right_pixel = im.getpixel((i + 1,j + 1))

            if id[j][i] == 0:
                if (pixel == down_right_pixel) and not(id[j + 1][i + 1]==0):  
                    id[j][i] = id[j + 1][i + 1]
                    #print("upleft")

                elif (pixel == down_pixel) and not(id[j + 1][i]==0):
                                    id[j][i] = id[j + 1][i]
                                    
                                    #print("up")

                elif (pixel == down_left_pixel) and not(id[j + 1][i - 1]==0):
                                    id[j][i] = id[j + 1][i - 1]
                                    
                                    #print("upright")

                elif (pixel == right_pixel) and not(id[j][i + 1]==0):
                                    id[j][i] = id[j][i + 1]
                                    
                                    #print("left")

                elif pixel == left_pixel and not(id[j][i - 1]==0):
                                    id[j][i] = id[j][i - 1]
                                    
                                    #print("left")

                elif pixel == up_right_pixel and not(id[j - 1][i + 1]==0):
                                    id[j][i] = id[j - 1][i + 1]
                                    
                                    #print("upright")

                elif pixel == up_pixel and not(id[j - 1][i]==0):
                                    id[j][i] = id[j - 1][i]
                                    
                                    #print("up")

                elif pixel == up_left_pixel and not(id[j - 1][i - 1]==0):                          
                                    id[j][i] = id[j - 1][i - 1]
                                    
                                    #print("upleft")
                
                else:
                    if pixel == color_black:
                        
                        id[j][i] = Edge.Edge(tuple(np.random.choice(range(256), size=3)))
                        #id[j][i] = Edge.Edge(pixel)
                        Edges.append(id[j][i])
                    else:
                        id[j][i] = Vertex.Vertex(tuple(np.random.choice(range(256), size=3)))
                        #id[j][i] = Vertex.Vertex(pixel)
                        Vertices.append(id[j][i])
            
            id[j][i].add(i,j)

            if pixel == up_left_pixel:
                if not(id[j - 1][i - 1]==0):
                    id[j - 1][i - 1].remove(i - 1, j - 1)
                id[j - 1][i - 1] = id[j][i]
                id[j - 1][i - 1].add(i - 1,j - 1)
                #print("upleft)

            if pixel == up_pixel:
                if not(id[j - 1][i]==0):
                    id[j - 1][i].remove(i, j - 1)
                id[j - 1][i] = id[j][i]
                id[j - 1][i].add(i, j - 1)
                #print("up")

            if pixel == up_right_pixel:
                if not(id[j - 1][i + 1]==0):
                    id[j - 1][i + 1].remove(i + 1, j - 1)
                id[j - 1][i + 1] = id[j][i]
                id[j - 1][i + 1].add(i + 1, j - 1)
                #print("upright")

            if pixel == left_pixel:
                if not(id[j][i - 1]==0):
                    id[j][i - 1].remove(i - 1, j)
                id[j][i - 1] = id[j][i]
                id[j][i - 1].add(i - 1, j)
                #print("left")
            
            if pixel == right_pixel:
                if not(id[j][i + 1]==0):
                    id[j][i + 1].remove(i + 1, j)
                id[j][i + 1] = id[j][i]
                id[j][i + 1].add(i + 1, j)
                #print("left")

            if pixel == down_left_pixel:
                if not(id[j + 1][i - 1]==0):
                    id[j + 1][i - 1].remove(i - 1,j + 1)
                id[j + 1][i - 1] = id[j][i]
                id[j + 1][i - 1].add(i - 1,j + 1)
                #print("upright")

            if pixel == down_pixel:
                if not(id[j + 1][i]==0):
                    id[j + 1][i].remove(i, j + 1)
                id[j + 1][i] = id[j][i]
                id[j + 1][i].add(i, j + 1)
                #print("up")

            if pixel == down_right_pixel:
                if not(id[j + 1][i + 1]==0):
                    id[j + 1][i + 1].remove(i + 1,j + 1)
                id[j + 1][i + 1] = id[j][i]
                id[j + 1][i + 1].add(i + 1,j + 1)
                #print("upleft")


  
#draw image
image = Image.new("RGB", im.size, (255, 255, 255))

for vertex in Vertices:
    pixels = vertex.pixel_coordinates
    for pixel in pixels:
        image.putpixel(pixel, vertex.color)

for edge in Edges:
    pixels = edge.pixel_coordinates
    for pixel in pixels:
        image.putpixel(pixel, edge.color)

#image.putpixel((10,6), (0,0,0))
#print(id[10][6].color)

image.save("first iteration.png")
print(colors)
for count in range(0,50):
    for j in range(1,im.size[1] - 1):
        for i in range(1,im.size[0] - 1):
            pixel = im.getpixel((i,j))
            #colors.add(pixel)
            if not(pixel == color_white):

                up_left_pixel = im.getpixel((i - 1,j - 1))
                up_pixel = im.getpixel((i,j - 1))
                up_right_pixel = im.getpixel((i + 1,j - 1))

                left_pixel = im.getpixel((i - 1,j))
                right_pixel = im.getpixel((i + 1,j))

                down_left_pixel = im.getpixel((i - 1,j + 1))
                down_pixel = im.getpixel((i,j + 1))
                down_right_pixel = im.getpixel((i + 1,j + 1))

                count = {}
                if (pixel == down_right_pixel) and not(id[j + 1][i + 1]==0):
                        if id[j + 1][i + 1] in count:
                              count[id[j + 1][i + 1]] = count[id[j + 1][i + 1]] + 1
                        else:
                              count[id[j + 1][i + 1]] = 0
                
                if (pixel == down_pixel) and not(id[j + 1][i]==0):
                        if id[j + 1][i] in count:
                              count[id[j + 1][i]] = count[id[j + 1][i]] + 1
                        else:
                              count[id[j + 1][i]] = 0
                
                if (pixel == down_left_pixel) and not(id[j + 1][i - 1]==0):
                        if id[j + 1][i - 1] in count:
                              count[id[j + 1][i - 1]] = count[id[j + 1][i - 1]] + 1
                        else:
                              count[id[j + 1][i - 1]] = 0

                if (pixel == right_pixel) and not(id[j][i + 1]==0):
                        if id[j][i + 1] in count:
                              count[id[j][i + 1]] = count[id[j][i + 1]] + 1
                        else:
                              count[id[j][i + 1]] = 0

                if (pixel == left_pixel) and not(id[j][i - 1]==0):
                        if id[j][i - 1] in count:
                              count[id[j][i - 1]] = count[id[j][i - 1]] + 1
                        else:
                              count[id[j][i - 1]] = 0

                if (pixel == up_right_pixel) and not(id[j - 1][i + 1]==0):
                        if id[j - 1][i + 1] in count:
                              count[id[j - 1][i + 1]] = count[id[j - 1][i + 1]] + 1
                        else:
                              count[id[j - 1][i + 1]] = 0
                
                if (pixel == up_pixel) and not(id[j - 1][i]==0):
                        if id[j - 1][i] in count:
                              count[id[j - 1][i]] = count[id[j - 1][i]] + 1
                        else:
                              count[id[j - 1][i]] = 0

                if (pixel == up_left_pixel) and not(id[j - 1][i - 1]==0):
                        if id[j - 1][i - 1] in count:
                              count[id[j - 1][i - 1]] = count[id[j - 1][i - 1]] + 1
                        else:
                              count[id[j - 1][i - 1]] = 0

                biggest_count = [0,0]
                for key in count:
                       if count[key] > biggest_count[1]:
                              biggest_count[0] = key
                              biggest_count[1] = count[key]

                if len(count)>4:
                    print(len(count))

                if not(id[j][i]==biggest_count[0]) and not (biggest_count[0] == 0):
                    id[j][i].remove(i,j)
                    id[j][i] = biggest_count[0]
                    id[j][i].add(i,j)

                """if (pixel == down_right_pixel) and not(id[j + 1][i + 1]==id[j][i]):
                    id[j][i].remove(i,j)
                    id[j][i] = id[j + 1][i + 1]
                    id[j][i].add(i,j)
                    #print("upleft")

                elif (pixel == down_pixel) and not(id[j + 1][i]==id[j][i]):
                    id[j][i].remove(i,j)
                    id[j][i] = id[j + 1][i]
                    id[j][i].add(i,j)
                    #print("up")

                elif (pixel == down_left_pixel) and not(id[j + 1][i - 1]==id[j][i]):
                    id[j][i].remove(i,j)
                    id[j][i] = id[j + 1][i - 1]
                    id[j][i].add(i,j)
                    #print("upright")

                elif (pixel == right_pixel) and not(id[j][i + 1]==id[j][i]):
                    id[j][i].remove(i,j)
                    id[j][i] = id[j][i + 1]
                    id[j][i].add(i,j)
                    #print("left")

                elif pixel == left_pixel and not(id[j][i - 1]==id[j][i]):
                    id[j][i].remove(i,j)
                    id[j][i] = id[j][i - 1]
                    id[j][i].add(i,j)
                    #print("left")

                elif pixel == up_right_pixel and not(id[j - 1][i + 1]==id[j][i]):
                    id[j][i].remove(i,j)
                    id[j][i] = id[j - 1][i + 1]
                    id[j][i].add(i,j)
                    #print("upright")

                elif pixel == up_pixel and not(id[j - 1][i]==id[j][i]):
                    id[j][i].remove(i,j)
                    id[j][i] = id[j - 1][i]
                    id[j][i].add(i,j)
                    #print("up")

                elif pixel == up_left_pixel and not(id[j - 1][i - 1]==id[j][i]):
                    id[j][i].remove(i,j)                
                    id[j][i] = id[j - 1][i - 1]
                    id[j][i].add(i,j)
                    #print("upleft")"""
                 
"""
for j in reversed(range(1,im.size[1] - 1)):
    for i in reversed(range(1,im.size[0] - 1)):
        pixel = im.getpixel((i,j))
        if not(pixel == color_white):

            up_left_pixel = im.getpixel((i - 1,j - 1))
            up_pixel = im.getpixel((i,j - 1))
            up_right_pixel = im.getpixel((i + 1,j - 1))

            left_pixel = im.getpixel((i - 1,j))
            right_pixel = im.getpixel((i + 1,j))

            down_left_pixel = im.getpixel((i - 1,j + 1))
            down_pixel = im.getpixel((i,j + 1))
            down_right_pixel = im.getpixel((i + 1,j - 1))

            if pixel == down_right_pixel:
                id[j][i] = id[j - 1][i + 1]
                #print("upleft")

            elif pixel == down_pixel:
                id[j][i] = id[j + 1][i]
                #print("up")

            elif pixel == down_left_pixel:
                id[j][i] = id[j + 1][i - 1]
                #print("upright")

            elif pixel == right_pixel:
                id[j][i] = id[j][i + 1]
                #print("left")

            else:
                if pixel == color_black:
                    id[j][i] = Edge.Edge(tuple(np.random.choice(range(256), size=3)))
                    #id[j][i] = Edge.Edge(pixel)
                    Edges.append(id[j][i])
                else:
                    id[j][i] = Vertex.Vertex(tuple(np.random.choice(range(256), size=3)))
                    #id[j][i] = Vertex.Vertex(pixel)
                    Vertices.append(id[j][i])

            id[j][i].add(i,j)"""

        
#draw image
image = Image.new("RGB", im.size, (255, 255, 255))

for vertex in Vertices:
    pixels = vertex.pixel_coordinates
    for pixel in pixels:
        image.putpixel(pixel, vertex.color)

for edge in Edges:
    pixels = edge.pixel_coordinates
    for pixel in pixels:
        image.putpixel(pixel, edge.color)

#image.putpixel((10,6), (0,0,0))
#print(id[10][6].color)

image.save("second iteration.png")

polished_Edges = []
polished_Vertices = []
for edge in Edges:
       if not(edge.get_size() == 0):
              polished_Edges.append(edge)

for vertex in Vertices:
       if not(vertex.get_size() == 0):
              polished_Vertices.append(vertex)

print(len(polished_Edges))
print(len(polished_Vertices))