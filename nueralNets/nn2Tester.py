import sys; args = sys.argv[1:]
import math
import random

global ALPHA, EPOHCS
ALPHA = [0.1]
EPOCHS = [40000]

def hvalue(list1, list2):
    return [list1[i]*list2[i] for i in range(len(list1))]

def dotproduct(list1, list2):
    if not type(list1) is list: list1 = [list1]
    if not type(list2) is list: list2 = [list2]
    return sum(hvalue(list1, list2))

def T1(value):
    return value

def T2(value):
    return value if value >= 0 else 0

def T3(value, test=0):
    try:
        return 1/(1+math.exp(-value))
    except OverflowError:
        return 0

def logisticDerivitive(i):
    return i*(1-i)

def T4(value):
    return 2*T3(value) - 1

class Network():
    def __init__(self, layers):
        self.layers = layers[:-1]
        self.lastLayer = layers[-1]
    
    def moveForward(self, inputs):
        for layer in self.layers:
            inputs = layer.moveForward(inputs)
        return self.lastLayer.moveForward(inputs)
    
    def backPropagation(self, errors):
        oldWeights, lastErrors = self.lastLayer.backPropagate(errors)
        for i in range(len(self.layers)-1, -1, -1):
            oldWeights, lastErrors = self.layers[i].backPropagate(oldWeights, lastErrors)

class Layer():
    def __init__(self, numNodes, nodes):
        self.nodes = nodes
        self.errors = [0 for i in range(numNodes)]
        self.negativeGradients = [0 for i in range(numNodes)]
        self.incomingValues = [0 for i in range(numNodes)]
        self.lastOutput = ""

    def moveForward(self, inputs):
        self.incomingValues = inputs
        outputs = []
        self.incomingValues = inputs
        for node in self.nodes:
            outputs.append(node.moveForward(inputs))
        self.lastOutput = outputs
        return outputs
    
    def backPropagate(self, currWeights, errors):
        currWeightsReordered = currWeights
        errorsReordered = []
        negativeGradients = []
        if type(currWeights[0]) == list:
            currWeightsReordered = []
            for i in range(len(self.nodes)):
                for weight in currWeights:
                    currWeightsReordered.append(weight[i])
        for i in range(len(self.nodes)):
            if type(currWeights[0]) == list:
                weightsForNode = currWeightsReordered[i*(len(currWeightsReordered)//len(self.nodes)):(i*(len(currWeightsReordered)//len(self.nodes))+(len(currWeightsReordered)//len(self.nodes)))]
                errorSum = 0
                for j in range(len(errors)):
                    errorSum += errors[j]*weightsForNode[j]*logisticDerivitive(self.lastOutput[i])
                # errorsReordered.append(dotproduct(currWeightsReordered[i], errors) * logisticDerivitive(self.lastOutput[i]))
                errorsReordered.append(errorSum)
            else:
                errorsReordered.append(errors[i]*logisticDerivitive(self.lastOutput[i])*currWeightsReordered[i])
        self.errors = [error for error in errorsReordered]
        for i in range(len(self.nodes)):
            for j in range(len(self.incomingValues)):
                negativeGradients.append(self.incomingValues[j] * self.errors[i])
        self.negativeGradients = [gradient for gradient in negativeGradients]

        oldWeights = [[weight for weight in node.weights] for node in self.nodes]
        count = 0
        for node in self.nodes:
            for i in range(len(node.weights)):
                node.weights[i] = node.weights[i] + (ALPHA[0] * self.negativeGradients[count])
                count += 1
        return oldWeights, errorsReordered

class LastLayer():
    def __init__(self, weights):
        self.function = T3
        self.weights = weights
        self.errors = [0 for i in range(len(weights))]
        self.negativeGradients = [0 for i in range(len(weights))]
        self.incomingValues = [0 for i in range(len(weights))]
        self.lastOutput = ""

    def moveForward(self, inputs):
        self.incomingValues = inputs
        outputs = []
        for i in range(len(inputs)):
            outputs.append(self.weights[i]*inputs[i])
        self.lastOutput = outputs
        return outputs
    
    def backPropagate(self, errors):
        self.errors = errors
        errorsReordered = []
        negativeGradients = []
        # for i in range(len(self.weights)):
        #     errorsReordered.append(errors[i]*self.weights[i]*logisticDerivitive(self.lastOutput[i]))
        for i in range(len(self.weights)):
            negativeGradients.append(errors[i]*self.incomingValues[i])
        self.negativeGradients = negativeGradients

        oldWeights = [weight for weight in self.weights]
        for i in range(len(self.weights)):
            self.weights[i] = self.weights[i] + (ALPHA[0] * self.negativeGradients[i])
        return oldWeights, errors

class Node():
    def __init__(self, weights):
        self.function = T3
        self.weights = weights

    def moveForward(self, inputs):
        return T3(dotproduct(inputs, self.weights))
    
def createNetwork(inputs, outputs, weights, lenInputs):
    numOfNodes = lenInputs
    layerCount = 0
    layers = []
    for layer in weights:
        numOfNodes = int(len(layer)/numOfNodes)
        numOfWeightsEachNode = int(len(layer)/numOfNodes)
        if layerCount == len(weights) - 1:
            lastLayer = LastLayer(layer)
            continue
        weightsArray = []
        nodes = []
        temp = 1
        for weight in layer:
            weightsArray.append(weight)
            if temp % numOfWeightsEachNode == 0:
                nodes.append(Node([weight for weight in weightsArray]))
                weightsArray = []
            temp += 1
        layer = Layer(numOfNodes, nodes)
        layers.append(layer)
        layerCount += 1
    layers.append(lastLayer)

    model = Network(layers)

    error = 99999
    for epoch in range(EPOCHS[0]):
        currError = 0
        for i in range(len(inputs)):
            p = model.moveForward(inputs[i])
            model.backPropagation([outputs[i][j] - p[j] for j in range(len(p))])
            finalLayerErrors = [outputs[i][j] - p[j] for j in range(len(p))]
            currError += sum([abs(value) for value in finalLayerErrors])
        if currError < error:
            error = currError
        if error < 0.03:
            return model, error
    return model, error

def main():
    inputs = []
    outputs = []
    inputLength = 0
    outputLength = 0
    with open(args[0]) as file:
        for line in file:
            insAndOuts = line.split("=>")
            inputLength = len(insAndOuts[0].strip().split(' ')) + 1
            inputs.append([float(val) for val in insAndOuts[0].strip().split(' ')] + [1])
            outputLength = len(insAndOuts[1].strip().split(' '))
            outputs.append([float(val) for val in insAndOuts[1].strip().split(' ')])
    weights = []
    currSize = inputLength
    if len(outputs[0]) > 1:
        for numOfNodes in [3, outputLength]:
            weights.append([random.random() for i in range(currSize*numOfNodes)])
            currSize = numOfNodes
    else:
        for numOfNodes in [2, outputLength]:
            weights.append([random.random() for i in range(currSize*numOfNodes)])
            currSize = numOfNodes
    weights.append([random.random() for i in range((outputLength))])
    # weights = [[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5], [0.5, 0.5]]
    # weights = [[0.35729646982809526, 0.537037256907212, 0.32526984385198654, 0.36770327721578944, 0.794198926486814, 0.1564572297193254, 0.9367092442349267, 0.024464671245931546, 0.48787001599487234, 0.011275362266929378, 0.2489870641903824, 0.6892120442667327], [0.6254125106934862, 0.3666520457185767, 0.21868246801078084, 0.5594707699615421, 0.5717525657138497, 0.09786097008152705], [1.7341480504372917, 0.7346118504912303]]
    # weights = [[4, -3, -6, 5], [1.1, 1.2, -1.3, -1.4, 1.5, 1.6], [0.1, -0.2, 0.3, 0.4, 0.5, -0.6], [1, -2]]
    # if len(outputs[0]) > 1:
    #     ALPHA[0] = 0.5
    model, error = createNetwork(inputs, outputs, weights, inputLength)
    while error > 0.03:
        print("Error: " + str(error))
        counts = "Layer Counts: " + str(len(inputs[0])) + " "
        for layer in model.layers:
            counts += str(len(layer.nodes)) + " "
        counts += str(len(outputs[0]))
        print(counts)

        for layer in model.layers:
            weightString = ""
            for node in layer.nodes:
                for weight in node.weights:
                    weightString += str(weight) + " "
            print(weightString.strip())
        weightString = ""
        for weight in model.lastLayer.weights:
            weightString += str(weight) + " "
        print(weightString.strip())

        weights = []
        currSize = inputLength
        if len(outputs[0]) > 1:
            for numOfNodes in [3, outputLength]:
                weights.append([random.random() for i in range(currSize*numOfNodes)])
                currSize = numOfNodes
        else:
            for numOfNodes in [2, outputLength]:
                weights.append([random.random() for i in range(currSize*numOfNodes)])
                currSize = numOfNodes
        weights.append([random.random() for i in range((outputLength))])
        model, error = createNetwork(inputs, outputs, weights, inputLength)
    
    counts = "Layer Counts: " + str(len(inputs[0])) + " "
    for layer in model.layers:
        counts += str(len(layer.nodes)) + " "
    counts += str(len(outputs[0]))
    print(counts)

    for layer in model.layers:
        weightString = ""
        for node in layer.nodes:
            for weight in node.weights:
                weightString += str(weight) + " "
        print(weightString.strip())
    weightString = ""
    for weight in model.lastLayer.weights:
        weightString += str(weight) + " "
    print(weightString.strip())

if __name__ == "__main__": main()

# Zachary Baker, Pd. 4, 2024