import sys; args = sys.argv[1:]
import math
import random

class ForwardNode:
    def __init__(self, inputs=[], level=0):
        self.function = T3
        self.level = level
        self.inputs = inputs
        self.value = 0
        self.error = 0

class ForwardLayer:
    def __init__(self, numNodes, numWeights):
        self.nodes = [ForwardNode(level=i) for i in range(numNodes)]
        self.weights = [random.random() for i in range(numWeights)]

def hvalue(list1, list2):
    return [list1[i]*list2[i] for i in range(len(list1))]

def dotproduct(list1, list2):
    return sum(hvalue(list1, list2))

def T1(value):
    return value

def T2(value):
    return value if value >= 0 else 0

def T3(value, test=0):
    return 1/(1+math.exp(-value))

def logistic_deriv(i):
    return (T3(i))*(1-(T3(i)))

def T4(value):
    return 2*T3(value) - 1

def main():
    things = []
    with open(args[0]) as f:
        for line in f:
            inputs = line.split("=>")[0].strip().split()
            outputs = line.split("=>")[1].strip().split()
            for i in range(len(inputs)):
                inputs[i] = int(inputs[i])
            for i in range(len(outputs)):
                outputs[i] = int(outputs[i])
            things.append([inputs, outputs])
    inputs1 = things[0][0] + [1]
    inputs2 = things[1][0] + [1]
    previousLayerSize = len(inputs1)
    
    # weights = [[random.random(), random.random(), random.random(), random.random()], [random.random(), random.random()], [random.random()]]

    # for p in range(100000):
        # inputs = inputs1 if p%2 == 0 else inputs2
        # desired = things[0][1][0] if p%2 == 0 else things[1][1][0]
    inputs = inputs1
    desired = things[0][1][0]
    previousLayerSize = len(inputs)
    layers = []

    weights = [[random.random(), random.random(), random.random(), random.random()], [random.random(), random.random()], [random.random()]]

    for e in range(10000):
        previousLayerSize = len(inputs)
        layers=[]
        newLayer = ForwardLayer(2, int(len(inputs)/2*4))
        for j in range(len(newLayer.nodes)):
            subWeights = weights[0][j*previousLayerSize:(j+1)*previousLayerSize]
            newLayer.nodes[j].value = dotproduct(inputs, subWeights)
        layers.append(newLayer)
        previousLayerSize = len(newLayer.nodes)
        for l in range(len(layers[len(layers)-1].nodes)):
            layers[len(layers)-1].nodes[l].value = layers[len(layers)-1].nodes[l].function(layers[len(layers)-1].nodes[l].value)

        newLayer = ForwardLayer(1, len(layers[len(layers)-1].nodes))
        for j in range(len(newLayer.nodes)):
            newLayer.nodes[j].value = dotproduct([node.value for node in layers[len(layers)-1].nodes], weights[1])
        layers.append(newLayer)
        previousLayerSize = len(newLayer.nodes)
        for l in range(len(layers[len(layers)-1].nodes)):
            layers[len(layers)-1].nodes[l].value = layers[len(layers)-1].nodes[l].function(layers[len(layers)-1].nodes[l].value)


        newLayer = ForwardLayer(1, len(layers[len(layers)-1].nodes))
        for j in range(len(newLayer.nodes)):
            newLayer.nodes[j].value = dotproduct([node.value for node in layers[len(layers)-1].nodes], weights[2])
        layers.append(newLayer)
        previousLayerSize = len(newLayer.nodes)
        for l in range(len(layers[len(layers)-1].nodes)):
            layers[len(layers)-1].nodes[l].value = layers[len(layers)-1].nodes[l].function(layers[len(layers)-1].nodes[l].value)

        temp = []
        for node in newLayer.nodes:
            temp.append(node.value)
        print(0.5*(int(desired)-temp[0])**2)

        for w in range(len(layers)-1, -1, -1):
            if w == len(layers)-1:
                for l in range(len(layers[w].nodes)):
                    layers[w].nodes[l].error = (int(desired)-temp[0])
                weights[2] = [weights[2][i] + 0.1*layers[w].nodes[0].error*layers[w-1].nodes[0].value for i in range(len(weights[2]))]
            elif w == len(layers)-2:
                for l in range(len(layers[w].nodes)):
                    # subweights = layers[w].weights[l*len(layers[w].nodes):(l+1)*len(layers[w].nodes)]
                    layers[w].nodes[l].error = dotproduct([node.error for node in layers[w+1].nodes], layers[w+1].weights)*logistic_deriv(layers[w].nodes[l].value)
                weights[1] = [weights[1][i] + 0.1*layers[w-1].nodes[i].value*layers[w].nodes[0].error for i in range(len(weights[1]))]

            else:
                for l in range(len(layers[w].nodes)):
                    subweights = weights[1][l::len(layers[w].nodes)]
                    layers[w].nodes[l].error = dotproduct([node.error for node in layers[w+1].nodes], subweights)*logistic_deriv(layers[w].nodes[l].value)
                for c in range(len(weights[0])):
                    weights[0][c] = weights[0][c] + 0.1*inputs[c%2]*layers[w].nodes[int(c/2)].error
    
    #epochs
    # for e in range(100000):
    #     # inputs = inputs1 if e%2 == 0 else inputs2
    #     # desired = things[0][1][0] if e%2 == 0 else things[1][1][0]
    #     inputs = inputs1
    #     desired = things[0][1][0]

    #     for q in range(len(layers)):
    #         for r in range(len(layers[q].nodes)):
    #             if q == 0:
    #                 subweights = layers[q].weights[r*len(layers[q].nodes):(r+1)*len(layers[q].nodes)]
    #                 layers[q].nodes[r].value = dotproduct(inputs, subweights)
    #             else:
    #                 subweights = layers[q].weights
    #                 layers[q].nodes[r].value = dotproduct([node.value for node in layers[q-1].nodes], subweights)
    #             layers[q].nodes[r].value = layers[q].nodes[r].function(layers[q].nodes[r].value)

    #     temp = []
    #     for node in layers[len(layers)-1].nodes:
    #         temp.append(node.value)

    #     for q in range(len(layers)-1, -1, -1):
    #         if q == len(layers)-1:
    #             for l in range(len(layers[q].nodes)):
    #                 layers[q].nodes[l].error = (int(desired)-temp[0])
    #             layers[q].weights = [layers[q].weights[i] + 0.1*layers[q].nodes[0].error*layers[q-1].nodes[0].value for i in range(len(layers[q].weights))]
    #         elif w == len(layers)-2:
    #             for l in range(len(layers[w].nodes)):
    #                 # subweights = layers[w].weights[l*len(layers[w].nodes):(l+1)*len(layers[w].nodes)]
    #                 layers[w].nodes[l].error = dotproduct([node.error for node in layers[w+1].nodes], layers[w+1].weights)*logistic_deriv(layers[w].nodes[l].value)
    #             layers[w].weights = [layers[w].weights[i] + 0.1*layers[w-1].nodes[i].value*layers[w].nodes[0].error for i in range(len(layers[w].weights))]

    #         else:
    #             for l in range(len(layers[w].nodes)):
    #                 subweights = layers[w+1].weights[l::len(layers[w].nodes)]
    #                 layers[w].nodes[l].error = dotproduct([node.error for node in layers[w+1].nodes], subweights)*logistic_deriv(layers[w].nodes[l].value)
    #             # for c in range(len(layers[w].weights)):
    #             #     layers[w].weights[c] = layers[w].weights[c] + 0.1*inputs[c%2]*layers[w].nodes[int(c/2)].error
    #             layers[w].weights = [layers[w].weights[0] + 0.1*inputs[0]*layers[w].nodes[0].error, layers[w].weights[1] + 0.1*inputs[1]*layers[w].nodes[0].error, layers[w].weights[2] + 0.1*inputs[0]*layers[w].nodes[1].error, layers[w].weights[3] + 0.1*inputs[1]*layers[w].nodes[1].error]
        
    print("Layer Counts: 2 2 1 1")
    for i in range(len(layers)):
        curr = ""
        for j in range(len(layers[i].weights)):
            curr += str(layers[i].weights[j]) + " "
        print(curr.strip())

if __name__ == "__main__": main()

# Zachary Baker, Pd. 4, 2024