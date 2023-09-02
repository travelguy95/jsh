import random
import pandas as pd
import math
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
from numba import jit
import matplotlib.colors as colors

class Particle():
  def __init__(self, x, y, u, v, radius, list_pos):
    self.x = x
    self.y = y
    self.u = u
    self.v = v
    self.radius = radius
    self.list_pos = list_pos

jit(nopython=True)
def collide(p1,p2):
    reduction = 1.0
    x = p1.x - p2.x
    y = p1.y - p2.y
    slength = x*x+y*y
    length = math.sqrt(slength)
    target = p1.radius + p2.radius
    if length < target and length!=0:
        factor = reduction*(length-target)/length
        p1.x -= x*factor*0.5
        p1.y -= y*factor*0.5
        p2.x += x*factor*0.5
        p2.y += y*factor*0.5

jit(nopython=True)
def border_collide(self,rows,cols):
  dt = 0.05
  if self.x > cols - self.radius:
      self.x = 2 * (cols - self.radius) - self.x
  elif self.x < self.radius:
      self.x = 2 * self.radius - self.x
  if self.y > rows - self.radius:
      self.y = 2 * (rows - self.radius) - self.y
  elif self.y < self.radius:
      self.y = 2 * self.radius - self.y
  if obstruct[math.floor(self.y)][math.floor(self.x)] == 99:
    self.x = self.x - dt*self.u
    self.y = self.y + dt*self.v

obstruct = np.load("/content/jsh/obstruct.npy")
obstruct_u = np.load("/content/jsh/obstruct_u.npy")
obstruct_v = np.load("/content/jsh/obstruct_v.npy")
obstruct_copy = np.load("/content/jsh/obstruct_copy.npy")

jit(nopython=True)
def run_code(rows,cols,steps,obstruct,obstruct_u,obstruct_v,skip_value):
  h = 1 
  my_particles = []
  n = 0
  radius = 0.25
  water_width = 50
  water_height = 190
  for row in range(0,int(190/(2*radius))):
    for col in range(0,int(50/(2*radius))):
      anti_row = int(rows/(2*radius))-row
      list_pos = n
      n = n + 1
      x = (2*radius)*col+radius
      y = (2*radius)*anti_row-radius
      particle = Particle(x, y, 0.0, 0.0, radius, list_pos)
      my_particles.append(particle)
  save_images = []
  dt = 0.05
  g = -9.81
  for iter in range(0,steps+1):
    for i, particle in enumerate(my_particles):
      particle.v = particle.v + dt*g
      particle.x = particle.x + particle.u*dt
      particle.y = particle.y + (-1*particle.v)*dt
    for count in range(0,10):
      for i, particle in enumerate(my_particles):
        border_collide(particle,rows,cols)
    list_of_list_positions = [None] * rows * cols
    for i, particle in enumerate(my_particles):
      row = math.floor(particle.y)
      if row > rows -1:
        row = rows-1
      col = math.floor(particle.x)
      if col > cols-1:
        col = cols-1
      if list_of_list_positions[row*cols+col] == None:
          list_of_list_positions[row*cols+col] = [particle.list_pos] #list_pos --> particle.list_pos
      else:
          list_of_list_positions[row*cols+col].append(particle.list_pos) #list_pos --> particle.list_pos
    for times in range(0,1):
      for i, particle in enumerate(my_particles):
        # the grid position of this particle:
        row = math.floor(particle.y)
        col = math.floor(particle.x)
        if col > cols-1:
            col = cols-1
        if row > rows-1:
            row = rows-1
        neighbor_particles = []
        if list_of_list_positions[row * cols + col] != None:
            neighbor_particles = neighbor_particles + list_of_list_positions[row * cols + col]
        if col !=0 and list_of_list_positions[row * cols + col-1] != None:
            neighbor_particles = neighbor_particles + list_of_list_positions[row * cols + col-1]
        if col !=0 and row!= 0 and list_of_list_positions[(row-1) * cols + col-1] != None:
            neighbor_particles = neighbor_particles + list_of_list_positions[(row-1) * cols + col-1]
        if col !=0 and row!= rows-1 and list_of_list_positions[(row+1) * cols + col-1] != None:
            neighbor_particles = neighbor_particles + list_of_list_positions[(row+1) * cols + col-1]
        if col != cols-1 and list_of_list_positions[row * cols + col+1] != None:
            neighbor_particles = neighbor_particles + list_of_list_positions[row * cols + col+1]
        if col != cols - 1 and row != 0 and list_of_list_positions[(row-1) * cols + col + 1] != None:
            neighbor_particles = neighbor_particles + list_of_list_positions[(row-1) * cols + col + 1]
        if col != cols - 1 and row != rows-1 and list_of_list_positions[(row+1) * cols + col + 1] != None:
            neighbor_particles = neighbor_particles + list_of_list_positions[(row+1) * cols + col + 1]
        if row != 0 and list_of_list_positions[(row-1) * cols + col] != None:
            neighbor_particles = neighbor_particles + list_of_list_positions[(row-1) * cols + col]
        if row != rows-1 and list_of_list_positions[(row+1) * cols + col] != None:
            neighbor_particles = neighbor_particles + list_of_list_positions[(row+1) * cols + col]
        neighbor_length = len(neighbor_particles)
        neighbor_particles2 = []
        if neighbor_length != 0:
            for count in range(0,neighbor_length):
                neighbor_list_position = neighbor_particles[count]
                if neighbor_list_position != particle.list_pos:
                    neighbor_particles2.append(my_particles[neighbor_list_position])
        for particle2 in neighbor_particles2:
            collide(particle, particle2)
        for count in range(0,10):
          border_collide(particle,rows,cols) #check again as particles moved due to collision
        
    list_of_list_positions = [None] * rows * cols
    for i, particle in enumerate(my_particles):
      row = math.floor(particle.y)
      col = math.floor(particle.x)
      if col > cols-1:
        col = cols-1
      if row > rows-1:
        row = rows-1
      if list_of_list_positions[row*cols+col] == None:
          list_of_list_positions[row*cols+col] = [particle.list_pos] #list_pos --> particle.list_pos
      else:
          list_of_list_positions[row*cols+col].append(particle.list_pos) #list_pos --> particle.list_pos
    u_old = np.zeros((rows,cols+1))
    for row in range(0,rows):
      for col in range(0,cols+1):
        if col == 0 or col == cols:
          pass
        else:
          if list_of_list_positions[row*cols+col-1] == None and list_of_list_positions[row*cols+col] == None:
            u_old[row][col] = 'nan'
    v_old = np.zeros((rows+1,cols))
    for row in range(0,rows+1):
      for col in range(0,cols):
        if row == 0 or row == rows:
          pass
        else:
          if list_of_list_positions[(row-1)*cols+col] == None and list_of_list_positions[row*cols+col] == None:
            v_old[row][col] = 'nan'
    u_weight = np.zeros((rows,cols+1))
    v_weight = np.zeros((rows+1,cols))
    for i, particle in enumerate(my_particles):
      x, y = particle.x, particle.y
      dx = x-math.floor(x)
      if y-math.floor(y) < 0.5:
        dy = 0.5 - (y-math.floor(y))
      else:
        dy = 1.5 - (y-math.floor(y))
      if math.floor(y-0.5) >= 0 and math.ceil(x) != 0 and math.ceil(x) != cols and (not pd.isnull(u_old[math.floor(y-0.5)][math.ceil(x)])):
        if obstruct_u[math.floor(y-0.5)][math.ceil(x)] == 1:
          u_old[math.floor(y-0.5)][math.ceil(x)] = u_old[math.floor(y-0.5)][math.ceil(x)] + (dx/h)*(dy/h)*particle.u
          u_weight[math.floor(y-0.5)][math.ceil(x)] = u_weight[math.floor(y-0.5)][math.ceil(x)] + (dx/h)*(dy/h)
      if math.floor(y-0.5) >= 0 and math.floor(x) != 0 and math.floor(x) != cols and (not pd.isnull(u_old[math.floor(y-0.5)][math.floor(x)])):
        if obstruct_u[math.floor(y-0.5)][math.floor(x)] == 1:
          u_old[math.floor(y-0.5)][math.floor(x)] = u_old[math.floor(y-0.5)][math.floor(x)] + (1-dx/h)*(dy/h)*particle.u
          u_weight[math.floor(y-0.5)][math.floor(x)] = u_weight[math.floor(y-0.5)][math.floor(x)] + (1-dx/h)*(dy/h)
      if math.ceil(y-0.5) < rows and math.ceil(x) != 0 and math.ceil(x) != cols and (not pd.isnull(u_old[math.ceil(y-0.5)][math.ceil(x)])):
        if obstruct_u[math.ceil(y-0.5)][math.ceil(x)] == 1:
          u_old[math.ceil(y-0.5)][math.ceil(x)] = u_old[math.ceil(y-0.5)][math.ceil(x)] + (dx/h)*(1-dy/h)*particle.u
          u_weight[math.ceil(y-0.5)][math.ceil(x)] = u_weight[math.ceil(y-0.5)][math.ceil(x)] + (dx/h)*(1-dy/h)
      if math.ceil(y-0.5) < rows and math.floor(x) != 0 and math.floor(x) != cols and (not pd.isnull(u_old[math.ceil(y-0.5)][math.floor(x)])):
        if obstruct_u[math.ceil(y-0.5)][math.floor(x)] == 1:
          u_old[math.ceil(y-0.5)][math.floor(x)] = u_old[math.ceil(y-0.5)][math.floor(x)] + (1-dx/h)*(1-dy/h)*particle.u
          u_weight[math.ceil(y-0.5)][math.floor(x)] = u_weight[math.ceil(y-0.5)][math.floor(x)] + (1-dx/h)*(1-dy/h)
      dy = math.ceil(y) - y
      if x-math.floor(x) > 0.5:
        dx = x - math.floor(x) - 0.5
      else:
        dx = x - math.floor(x) + 0.5
      if math.ceil(x-0.5)<cols and math.floor(y) != 0 and math.floor(y) != rows and (not pd.isnull(v_old[math.floor(y)][math.ceil(x-0.5)])):
        if obstruct_v[math.floor(y)][math.ceil(x-0.5)] == 1:
          v_old[math.floor(y)][math.ceil(x-0.5)] = v_old[math.floor(y)][math.ceil(x-0.5)] + (dx/h)*(dy/h)*particle.v
          v_weight[math.floor(y)][math.ceil(x-0.5)] = v_weight[math.floor(y)][math.ceil(x-0.5)] + (dx/h)*(dy/h)
      if math.floor(x-0.5)>= 0 and math.floor(y) != 0 and math.floor(y) != rows and (not pd.isnull(v_old[math.floor(y)][math.floor(x-0.5)])):
        if obstruct_v[math.floor(y)][math.floor(x-0.5)] == 1:
          v_old[math.floor(y)][math.floor(x-0.5)] = v_old[math.floor(y)][math.floor(x-0.5)] + (1-dx/h)*(dy/h)*particle.v
          v_weight[math.floor(y)][math.floor(x-0.5)] = v_weight[math.floor(y)][math.floor(x-0.5)] + (1-dx/h)*(dy/h)
      if math.ceil(x-0.5)<cols and math.ceil(y) != 0 and math.ceil(y) != rows and (not pd.isnull(v_old[math.ceil(y)][math.ceil(x-0.5)])):
        if obstruct_v[math.ceil(y)][math.ceil(x-0.5)] == 1:
          v_old[math.ceil(y)][math.ceil(x-0.5)] = v_old[math.ceil(y)][math.ceil(x-0.5)] + (dx/h)*(1-dy/h)*particle.v
          v_weight[math.ceil(y)][math.ceil(x-0.5)] = v_weight[math.ceil(y)][math.ceil(x-0.5)] + (dx/h)*(1-dy/h)
      if math.floor(x-0.5)>= 0 and math.ceil(y) != 0 and math.ceil(y) != rows and (not pd.isnull(v_old[math.ceil(y)][math.floor(x-0.5)])):
        if obstruct_v[math.ceil(y)][math.floor(x-0.5)] == 1:
          v_old[math.ceil(y)][math.floor(x-0.5)] = v_old[math.ceil(y)][math.floor(x-0.5)] + (1-dx/h)*(1-dy/h)*particle.v
          v_weight[math.ceil(y)][math.floor(x-0.5)] = v_weight[math.ceil(y)][math.floor(x-0.5)] + (1-dx/h)*(1-dy/h)
    for row in range(0,rows):
      for col in range(0,cols+1):
        if col != 0 and col != cols and (not pd.isnull(u_old[row][col])):
          if obstruct_u[row][col] == 1:
            u_old[row][col] = u_old[row][col]/u_weight[row][col]
    for row in range(0,rows+1):
      for col in range(0,cols):
        if row != 0 and row != rows and (not pd.isnull(v_old[row][col])):
          if obstruct_v[row][col] == 1:
            v_old[row][col] = v_old[row][col]/v_weight[row][col]
    rho = np.zeros((rows,cols))
    for i, particle in enumerate(my_particles):
      x = particle.x
      y = particle.y
      if x - math.floor(x) > 0.5:
        min_col = math.floor(x)
        max_col = math.floor(x) + 1
        dx = x - math.floor(x) - 0.5
      else:
        min_col = math.floor(x) - 1
        max_col = math.floor(x)
        dx = x - math.floor(x) + 0.5
      if y - math.floor(y) > 0.5:
        min_row = math.floor(y)
        max_row = math.floor(y) + 1
        dy = math.ceil(y)-y+0.5
      else:
        min_row = math.floor(y)-1
        max_row = math.floor(y)
        dy = math.ceil(y)-y-0.5
      denom = 0
      if max_row <= rows-1 and min_col >= 0 and obstruct[max_row][min_col] == 0:
        rho1 = (1-dx/h)*(1-dy/h)
        denom = denom + rho1
      if max_row <= rows-1 and max_col <= cols-1 and obstruct[max_row][max_col] == 0:
        rho2 = (dx/h)*(1-dy/h)
        denom = denom + rho2
      if min_row >= 0 and min_col >= 0 and obstruct[min_row][min_col] == 0:
        rho3 = (1-dx/h)*(dy/h)
        denom = denom + rho3
      if min_row >= 0 and max_col <= cols-1 and obstruct[min_row][max_col] == 0:
        rho4 = (dx/h)*(dy/h)
        denom = denom + rho4
      if max_row <= rows-1 and min_col >= 0 and obstruct[max_row][min_col] == 0:
        rho[max_row][min_col] = rho[max_row][min_col] + rho1/denom
      if max_row <= rows-1 and max_col <= cols-1 and obstruct[max_row][max_col] == 0:
        rho[max_row][max_col] = rho[max_row][max_col] + rho2/denom
      if min_row >= 0 and min_col >= 0 and obstruct[min_row][min_col] == 0:
        rho[min_row][min_col] = rho[min_row][min_col] + rho3/denom
      if min_row >= 0 and max_col <= cols-1 and obstruct[min_row][max_col] == 0:
        rho[min_row][max_col] = rho[min_row][max_col] + rho4/denom
    over_relax = 1.9
    for iterations in range(0,100):
      for row in range(0,rows):
        for col in range(0,cols):
          if list_of_list_positions[row*cols+col] == None or obstruct[row][col] == 99:
            pass
          else:
            sides = 4
            if col == 0 or obstruct_u[row][col] == 0:
              left = 0
              sides = sides - 1
            else:
              left = u_old[row][col]
            if col == cols-1 or obstruct_u[row][col+1] == 0:
              right = 0
              sides = sides - 1
            else:
              right = u_old[row][col+1]
            if row == 0 or obstruct_v[row][col] == 0:
              above = 0
              sides = sides - 1
            else:
              above = v_old[row][col]
            if row == rows-1 or obstruct_v[row+1][col] == 0:
              below = 0
              sides = sides - 1
            else:
              below = v_old[row+1][col]
            d = over_relax*(above-below+right-left)-(rho[row][col]-4) #we initialized to 4 molecules per water cell
            if row!=0 and obstruct_v[row][col] == 1:
              v_old[row][col] = v_old[row][col]-d/sides
            if row != rows-1 and obstruct_v[row+1][col] == 1:
              v_old[row+1][col] = v_old[row+1][col]+d/sides
            if col != cols-1 and obstruct_u[row][col+1] == 1:
              u_old[row][col+1] = u_old[row][col+1]-d/sides
            if col != 0 and obstruct_u[row][col] == 1:
              u_old[row][col] = u_old[row][col]+d/sides
    for i, particle in enumerate(my_particles):
      x, y = particle.x, particle.y
      dx = x-math.floor(x)
      if y-math.floor(y) < 0.5:
        dy = 0.5 - (y-math.floor(y))
      else:
        dy = 1.5 - (y-math.floor(y))
      max_row = math.ceil(y-0.5)
      min_row = math.floor(y-0.5)
      max_col = math.ceil(x)
      min_col = math.floor(x)
      if max_row > rows -1:
        max_row = rows-1
      if min_row < 0:
        min_row = 0
      u4 = u_old[min_row][max_col]
      u3 = u_old[min_row][min_col]
      u2 = u_old[max_row][max_col]
      u1 = u_old[max_row][min_col]
      if pd.isnull(u4):
        if pd.isnull(u3):
          u4 = u2
        else:
          u4 = u3
      if pd.isnull(u3):
        if pd.isnull(u4):
          u3 = u1
        else:
          u3 = u4
      if pd.isnull(u2):
        if pd.isnull(u4):
          u2 = u1
        else:
          u2 = u4
      if pd.isnull(u1):
        if pd.isnull(u2):
          u1 = u3
        else:
          u1 = u2
      particle.u = (1-dx/h)*(1-dy/h)*u1+(dx/h)*(1-dy/h)*u2 \
            +(1-dx/h)*(dy/h)*u3 + (dx/h)*(dy/h)*u4
      dy = math.ceil(y) - y
      if x-math.floor(x) > 0.5:
        dx = x - math.floor(x) - 0.5
      else:
        dx = x - math.floor(x) + 0.5
      max_row = math.ceil(y)
      min_row = math.floor(y)
      max_col = math.ceil(x-0.5)
      min_col = math.floor(x-0.5)
      if max_col > cols-1:
        max_col = cols-1
      if min_col < 0:
        min_col = 0
      v4 = v_old[min_row][max_col]
      v3 = v_old[min_row][min_col]
      v2 = v_old[max_row][max_col]
      v1 = v_old[max_row][min_col]
      if pd.isnull(v4):
        if pd.isnull(v3):
          v4 = v2
        else:
          v4 = v3
      if pd.isnull(v3):
        if pd.isnull(v4):
          v3 = v1
        else:
          v3 = v4
      if pd.isnull(v2):
        if pd.isnull(v4):
          v2 = v1
        else:
          v2 = v4
      if pd.isnull(v1):
        if pd.isnull(v2):
          v1 = v3
        else:
          v1 = v2
      particle.v = (1-dx/h)*(1-dy/h)*v1+(dx/h)*(1-dy/h)*v2 \
            +(1-dx/h)*(dy/h)*v3 + (dx/h)*(dy/h)*v4
    if iter%skip_value == 0:
      abs_vel = np.zeros((rows,cols))
      for row in range(0,rows):
        for col in range(0,cols):
          if list_of_list_positions[row*cols+col] == None:
            abs_vel[row][col] = 'nan'
          else:
            average_u = 0.5*(u_old[row][col] + u_old[row][col+1])
            average_v = 0.5*(v_old[row][col] + v_old[row+1][col])
            abs_vel[row][col] = (average_u**2+average_v**2)**0.5
      save_images.append(abs_vel)
    density = np.zeros((rows,cols))
    for i, particle in enumerate(my_particles):
      x = particle.x
      y = particle.y
      col = math.floor(x)
      row = math.floor(y)
      if row > rows -1:
        row = rows-1
      if col > cols-1:
        col = cols-1
      density[row][col] = density[row][col]+1

  return density, save_images
