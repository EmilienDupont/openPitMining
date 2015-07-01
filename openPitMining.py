#!/usr/bin/env python
from gurobipy import *

# Model data
cost = [];
for i in range(18):
    if (i < 8):
      cost.append(100)
    elif (i < 14 and i >= 8):
      cost.append(200)
    else:
      cost.append(300)

cost[8] += 1000; cost[13] += 1000; cost[14] += 1000;
cost[15] += 1000; cost[17] += 1000;

value = [];
for i in range(18):
    value.append(0)

value[0] = 200; value[6] = 300; value[9] = 500;
value[11] = 200; value[16] = 1000; value[17] = 1200;

edges = [];

for i in range(8,14):
    edges.append([i,i-8])
    edges.append([i,i-7])
    edges.append([i,i-6])

for i in range(14,18):
    edges.append([i,i-14])
    edges.append([i,i-13])
    edges.append([i,i-12])

# Optimization

m = Model()

n = len(cost) # number of blocks

# Indicator variable for each block
xb = {}
for i in range(n):
    xb[i] = m.addVar(vtype=GRB.BINARY, name="x%d" % i)

m.update()

# Set objective
m.setObjective(quicksum((value[i] - cost[i])*xb[i] for i in range(n)), GRB.MAXIMIZE)

# Add constraints
for edge in edges:
    u = edge[0]
    v = edge[1]
    m.addConstr(xb[u] <= xb[v])

m.optimize()

for v in m.getVars():
        print v.x