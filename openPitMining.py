#!/usr/bin/env python

import sys
import StringIO
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

cost[8] = 1000; cost[13] = 1000; cost[14] = 1000;
cost[15] = 1000; cost[17] = 1000;

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
    edges.append([i,i-6])
    edges.append([i,i-5])
    edges.append([i,i-4])

def mycallback(model, where):
    if where == GRB.callback.MESSAGE:
        print >>model.__output, model.cbGet(GRB.callback.MSG_STRING),

# Optimization
def optimize(cost, value, edges, output=False):

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

    if not output:
        m.params.OutputFlag = 0

    m.setParam('TimeLimit', 10)

    output = StringIO.StringIO()
    m.__output = output

    m.optimize(mycallback)

    if (m.status != 2):
        return ["error"]

    solution = [];

    for v in m.getVars():
        solution.append(v.x)

    solution.append(m.objVal)

    return [solution, output.getvalue()]

def handleoptimize(jsdict):
    if 'cost' in jsdict and 'value' in jsdict and 'edges' in jsdict:
        solution = optimize(jsdict['cost'], jsdict['value'], jsdict['edges'])
        return {'solution': solution }


if __name__ == '__main__':
    import json
    jsdict = json.load(sys.stdin)
    jsdict = handleoptimize(jsdict)
    print 'Content-Type: application/json\n\n'
    print json.dumps(jsdict)
