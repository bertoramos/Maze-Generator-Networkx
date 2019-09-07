
import networkx as nx
from collections import namedtuple
import cv2
import time
import numpy as np

Cell = namedtuple('Cell', 'i j')

class Grid:

    def __init__(self, dim):
        self.__dim = dim
        self.__G = nx.Graph()
        for i in range(dim):
            for j in range(dim):
                self.__G.add_node(Cell(i,j))

        for i in range(dim):
            for j in range(dim):
                n = Cell(i, j-1)
                s = Cell(i, j+1)
                e = Cell(i+1, j)
                w = Cell(i-1, j)

                if 0 <= n.i < dim and 0 <= n.j < dim:
                    self.__G.add_edge(Cell(i,j), n)
                if 0 <= s.i < dim and 0 <= s.j < dim:
                    self.__G.add_edge(Cell(i,j), s)
                if 0 <= e.i < dim and 0 <= e.j < dim:
                    self.__G.add_edge(Cell(i,j),e)
                if 0 <= w.i < dim and 0 <= w.j < dim:
                    self.__G.add_edge(Cell(i,j),w)
    
    def get_dim(self):
        return self.__dim
    
    def nodes(self):
        return list(self.__G.nodes())
    
    def edges(self):
        return list(self.__G.edges())

    def get_neighbors(self, i, j):
        return list(self.__G.adj[Cell(i, j)])


class Maze:

    def __init__(self, path):
        self.__G = nx.Graph()
        for a, b in path:
            self.__G.add_edge(a, b)

    def edges(self):
        return list(self.__G.edges())

    def solve(self, source, end):
        return list(nx.all_simple_paths(self.__G, source, end))


class MazeDisplayer:

    def __init__(self, height, width, scale, maze):
        self.__height = height
        self.__width = width
        self.__scale = scale
        self.__maze = maze
        
        self.__img = np.zeros([self.__height, self.__width, 3], np.uint8)
    
    def execute(self):
        for a, b in self.__maze.edges():
            self.__img = cv2.line(self.__img,
                                  (a.i*self.__scale + int(self.__scale/2), a.j*self.__scale + int(self.__scale/2)),
                                  (b.i*self.__scale + int(self.__scale/2), b.j*self.__scale + int(self.__scale/2)),
                                  (255, 255, 255), self.__scale - 10)        
        cv2.imshow('image', self.__img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

class PathDisplayer:

    def __init__(self, height, width, scale, maze):
        self.__height = height
        self.__width = width
        self.__scale = scale
        self.__maze = maze
        self.__path = maze.solve(Cell(0,0), Cell(int(width/scale) - 1, int(height/scale) - 1))
        
        self.__frame = np.zeros([self.__height, self.__width, 4], np.uint8)

    def play(self):
        n = 0
        while True:
            # Key listener
            k = cv2.waitKey(10)
            if k == 27:
                break
            # clear
            self.__frame = cv2.rectangle(self.__frame, (0,0), (self.__width, self.__height),(0,0,0),-1)

            # Draw maze
            for a, b in self.__maze.edges():
                self.__frame = cv2.line(self.__frame,
                                  (a.i*self.__scale + int(self.__scale/2), a.j*self.__scale + int(self.__scale/2)),
                                  (b.i*self.__scale + int(self.__scale/2), b.j*self.__scale + int(self.__scale/2)),
                                  (255, 255, 255), self.__scale - 10) 

            # Draw trail
            for e in range(n):
                a = self.__path[0][e]
                b = self.__path[0][e+1]
                self.__frame = cv2.line(self.__frame,
                                  (a.i*self.__scale + int(self.__scale/2), a.j*self.__scale + int(self.__scale/2)),
                                  (b.i*self.__scale + int(self.__scale/2), b.j*self.__scale + int(self.__scale/2)),
                                  (100, 100, 100), int(self.__scale/2))

            # Draw point
            point = self.__path[0][n]
            center = (point.i*self.__scale + int(self.__scale/2),
                      point.j*self.__scale + int(self.__scale/2))
            color = (0, 0, 255)
            self.__frame = cv2.circle(self.__frame, center, int((self.__scale - 10)/2), color, -1)
            
            n+=1
            if n == len(self.__path[0]):
                n = 0
            
            # show
            cv2.imshow('Animation', self.__frame)
            time.sleep(0.1)
        cv2.destroyAllWindows()

