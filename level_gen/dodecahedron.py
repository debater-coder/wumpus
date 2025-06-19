# TODO: use actual dodecahedron coordinates
import pygame as pg
import json
import random

from level_gen.graph import Node, force_directed_layout


caves = [
  {
    "location": 1,
    "tunnels": [2, 5, 8]
  },
  {
    "location": 2,
    "tunnels": [1, 3, 10]
  },
  {
    "location": 3,
    "tunnels": [2, 4, 12]
  },
  {
    "location": 4,
    "tunnels": [3, 5, 14]
  },
  {
    "location": 5,
    "tunnels": [1, 4, 6]
  },
  {
    "location": 6,
    "tunnels": [5, 7, 15]
  },
  {
    "location": 7,
    "tunnels": [6, 8, 17]
  },
  {
    "location": 8,
    "tunnels": [1, 7, 9]
  },
  {
    "location": 9,
    "tunnels": [8, 10, 18]
  },
  {
    "location": 10,
    "tunnels": [2, 9, 11]
  },
  {
    "location": 11,
    "tunnels": [10, 12, 19]
  },
  {
    "location": 12,
    "tunnels": [3, 11, 13]
  },
  {
    "location": 13,
    "tunnels": [12, 14, 20]
  },
  {
    "location": 14,
    "tunnels": [4, 13, 15]
  },
  {
    "location": 15,
    "tunnels": [6, 14, 16]
  },
  {
    "location": 16,
    "tunnels": [15, 17, 20]
  },
  {
    "location": 17,
    "tunnels": [7, 16, 18]
  },
  {
    "location": 18,
    "tunnels": [9, 17, 19]
  },
  {
    "location": 19,
    "tunnels": [11, 18, 20]
  },
  {
    "location": 20,
    "tunnels": [13, 16, 19]
  }
]

graph = {cave["location"]: Node(index=cave["location"], edges=cave["tunnels"], vector=pg.Vector2(random.uniform(-50, 50), random.uniform(-50, 50))) for cave in caves}

force_directed_layout(graph)

with open("dodecahedron.json", "w") as fp:
   json.dump([
       {
           "location": node.index,
           "tunnels": node.edges,
           "coords": (node.vector.x, node.vector.y)
       } for node in graph.values()
   ], fp)
