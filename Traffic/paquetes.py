from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid as PathGrid
from pathfinding.finder.a_star import AStarFinder
from numpy import copy
import numpy as np
import random

# 0 = Vacio
# 1 = Via
# 2 = Alto
# 3 = Limite entrada
# 4 = Limite salida

mat = [
  [0,0,0,0,0,0,0,0,4,0,0,0,0,3,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,1,0,0,0,0,1,2,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,2,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
  [3,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,4],
  [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
  [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
  [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
  [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
  [4,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,3],
  [0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,2,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,2,1,0,0,0,0,1,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,3,0,0,0,0,4,0,0,0,0,0,0,0,0],
]

class Auto(Agent):
  def __init__(self, model, entrada, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.salida = None
        self.entrada = entrada
        self.standBy = False
        self.waitTime = 3
        self.roaming = False
        self.endX = 1
        self.endY = 1
        self.localMatrix = None

  def step(self):

    self.localMatrix = copy(mat)
    if(self.entrada.pos == self.model.entradas[0].pos):
      self.localMatrix[10][6] = 0
    elif(self.entrada.pos == self.model.entradas[1].pos):
      self.localMatrix[15][9] = 0
    elif(self.entrada.pos == self.model.entradas[2].pos):
      self.localMatrix[6][10] = 0
    elif(self.entrada.pos == self.model.entradas[3].pos):
      self.localMatrix[10][15] = 0

    if(self.waitTime == 0):
        self.standBy = False
        self.waitTime = 3
      
    if(self.standBy == False):  
      if(self.roaming == False and self.salida == None):
        i = random.randint(0,len(self.model.salidas)-1)
        self.salida = self.model.salidas[i]
        
      pathGrid = PathGrid(matrix=self.localMatrix)
      
      if(self.roaming == False and self.salida != None):
        self.endX = self.salida.pos[0]
        self.endY = self.salida.pos[1]
        self.roaming = True

      start = pathGrid.node(self.pos[0],self.pos[1])
      end = pathGrid.node(self.endX,self.endY)
      
      finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
      path, runs = finder.find_path(start, end, pathGrid)

      if(len(path) > 1):
        if(len(self.model.grid.get_cell_list_contents(path[1])) <= 1):
          next_move = path[1]
          self.model.grid.move_agent(self, next_move)
      else:
          i = random.randint(0,len(self.model.entradas)-1)
          self.model.grid.move_agent(self,self.model.entradas[i].pos)
          self.entrada = self.model.entradas[i]
          self.roaming = False

          pathGrid.cleanup()
      
      for neighbor in self.model.grid.neighbor_iter(self.pos, moore=False):
        if type(neighbor) == Alto:
          self.standBy = True
    else:
        self.waitTime-=1

    return
  
  def parar(self):
    self.standBy = True

class Alto(Agent):
  def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos

class LimiteE(Agent):
  def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos

class LimiteS(Agent):
  def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos

class Via(Agent):
  def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos

class Calle(Model):
  def __init__(self):
        super().__init__()
        
        self.carN = 4
        self.salidas = []
        self.entradas = []
        self.posibilidades = None
        self.paso = 0
        
        self.matrix = mat
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(22, 22, torus=True)

        for _,x,y in self.grid.coord_iter():
          if self.matrix[y][x] == 1:
            via = Via(self, (x, y))
            self.grid.place_agent(via, via.pos)
            self.schedule.add(via)


          if self.matrix[y][x] == 2:
            alto = Alto(self, (x, y))
            self.grid.place_agent(alto, alto.pos)
            self.schedule.add(alto)

          if self.matrix[y][x] == 3:
            limite = LimiteE(self, (x, y))
            self.entradas.append(limite)
            self.grid.place_agent(limite, limite.pos)
            self.schedule.add(limite)

          if self.matrix[y][x] == 4:
            limite = LimiteS(self, (x, y))
            self.salidas.append(limite)
            self.grid.place_agent(limite, limite.pos)
            self.schedule.add(limite)
       

        self.extras  = copy(self.entradas)
        #self.extras = np.append(quinto,self.posibilidades)
        #self.extras = copy(self.posibilidades)
        for i in range(self.carN):
          i = random.randint(0, len(self.extras)-1)
          auto = Auto(self,self.extras[i], self.extras[i].pos)
          self.extras = np.delete(self.extras, i)
          self.grid.place_agent(auto, auto.pos)
          self.schedule.add(auto)

        auto5 = Auto(self,self.entradas[2], (13,3))
        self.grid.place_agent(auto5, (13,3))
        self.schedule.add(auto5)
          
  def step(self):
      self.schedule.step()


def agent_portrayal(agent):
    if(type(agent) == Auto):
      return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Yellow", "Layer": 1}
    elif (type(agent) == Alto):
      return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Blue", "Layer": 0}
    elif (type(agent) == LimiteE):
      return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Gray", "Layer": 0}
    elif (type(agent) == LimiteS):
      return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Gray", "Layer": 0}
    elif (type(agent) == Via):
      return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Green", "Layer": 0}
