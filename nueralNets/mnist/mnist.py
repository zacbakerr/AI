import sys; args = sys.argv[1:]
import math
import random
import time
import numpy as np

global ALPHA, EPOHCS
ALPHA = [0.1]
EPOCHS = [1000]

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
        print('overflow error')
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
        for i,layer in enumerate(self.layers):
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
        negativeGradients = []
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
        # numInputs = np.array(inputs)
        # numWeights = np.array(self.weights)
        # return T3(np.matmul(numInputs, numWeights))

def testNetwork(numOfTests, model):
    testIndices = [random.randint(1, 9998) for i in range(numOfTests+30)]
    correct = 0
    with open('archive/mnist_test.csv') as file:
        for i, line in enumerate(file):
            if i in testIndices:
                currInput = line.split(',')
                expectedOutput = int(currInput[0])
                currInput = currInput[1:]
                currInput = [float(input)/255 for input in currInput] + [1]
                output = model.moveForward(currInput)
                observedOutput = output.index(max(output))+1
                if expectedOutput == observedOutput: correct += 1
    return correct/(numOfTests+30)
    
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
    startTime = time.time()
    for epoch in range(EPOCHS[0]):
        currError = 0
        for i in range(len(inputs)):
            if i % 1000 == 0:
                accuracy = testNetwork(200, model)
                print("Accuracy: " + str(accuracy))
                with open("data.txt", "a") as file:
                    file.write("\n" + str(accuracy) + " " + str(time.time()-startTime))
            p = model.moveForward(inputs[i])
            model.backPropagation([outputs[i][j] - p[j] for j in range(len(p))])
            finalLayerErrors = [outputs[i][j] - p[j] for j in range(len(p))]
            currError += sum([abs(value) for value in finalLayerErrors])
        if currError < error:
            error = currError
    return model, error

def main():
    inputs = []
    outputs = []

    with open('archive/mnist_train.csv') as file:
        for i, line in enumerate(file):
            if i != 0:
                currInput = line.split(',')
                outputI = int(currInput[0])-1
                currOutput = [0 for i in range(10)]
                currOutput[outputI] = 1
                currInput = currInput[1:]
                currInput = [float(input)/255 for input in currInput] + [1]
                inputs.append(currInput)
                outputs.append(currOutput)
                
    inputLength = len(inputs[0])
    outputLength = len(outputs[0])
    weights = []
    currSize = inputLength
    for numOfNodes in [300, 100, outputLength]:
        weights.append([random.uniform(-1,1) for i in range(currSize*numOfNodes)])
        currSize = numOfNodes
    weights.append([random.uniform(-0.05,0.05) for i in range((outputLength))])
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