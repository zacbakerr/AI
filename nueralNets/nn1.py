import sys; args = sys.argv[1:]
import math

class Node:
    def __init__(self, function=args[1], inputs=[], level=0):
        self.function = T1 if function == "T1" else T2 if function == "T2" else T3 if function == "T3" else T4
        self.level = level
        self.inputs = inputs
        self.value = 0

class Layer:
    def __init__(self, numNodes):
        self.nodes = [Node(level=i) for i in range(numNodes)]

def hvalue(list1, list2):
    return [list1[i]*list2[i] for i in range(len(list1))]

def dotproduct(list1, list2):
    return sum(hvalue(list1, list2))

def T1(value):
    return value

def T2(value):
    return value if value >= 0 else 0

def T3(value):
    return 1/(1+math.exp(-value))

def T4(value):
    return 2*T3(value) - 1

def main():
    inputs = [float(i) for i in args[2:]]
    previousLayerSize = len(inputs)
    
    weights = []
    with open(args[0]) as f:
        for line in f:
            weights.append([float(i) for i in line.split()])

    layers = []
    newLayer = Layer(int(len(weights[0])/previousLayerSize))
    for j in range(len(newLayer.nodes)):
        subWeights = weights[0][j*previousLayerSize:(j+1)*previousLayerSize]
        newLayer.nodes[j].value = dotproduct(inputs, subWeights)
    layers.append(newLayer)
    previousLayerSize = len(newLayer.nodes)
    if len(weights) > 1:
        for l in range(len(layers[len(layers)-1].nodes)):
            layers[len(layers)-1].nodes[l].value = layers[len(layers)-1].nodes[l].function(layers[len(layers)-1].nodes[l].value)

    for i in range(1, len(weights)-1):
        newLayer = Layer(int(len(weights[i])/previousLayerSize))
        for j in range(len(newLayer.nodes)):
            subWeights = weights[i][j*previousLayerSize:(j+1)*previousLayerSize]
            newLayer.nodes[j].value = dotproduct([node.value for node in layers[len(layers)-1].nodes], subWeights)
        layers.append(newLayer)
        previousLayerSize = len(newLayer.nodes)
        for l in range(len(layers[len(layers)-1].nodes)):
            layers[len(layers)-1].nodes[l].value = layers[len(layers)-1].nodes[l].function(layers[len(layers)-1].nodes[l].value)

    if len(weights) > 1:
        newLayer = Layer(int(previousLayerSize))
        for j in range(len(newLayer.nodes)):
            newLayer.nodes[j].value = weights[len(weights)-1][j]*layers[len(layers)-1].nodes[j].value
        layers.append(newLayer)

    temp = []
    for node in newLayer.nodes:
        temp.append(node.value)
    print(temp)

if __name__ == "__main__": main()

# Zachary Baker, Pd. 4, 2024