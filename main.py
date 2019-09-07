
import utils
import generate
import cv2

import networkx as nx
import matplotlib.pyplot as plt

import numpy as np
import time

if __name__=="__main__":
    g = utils.Grid(20)
    g.get_neighbors(1, 1)

    maze = generate.dfs_generator(g)

    width = 400
    height = 400
    scale = int(width/g.get_dim())
    md = utils.MazeDisplayer(height, width, scale, maze)
    md.execute()

    path = maze.solve(utils.Cell(0,0), utils.Cell(g.get_dim()-1, g.get_dim()-1))
    pd = utils.PathDisplayer(height, width, int(width/g.get_dim()), maze)
    pd.play()

