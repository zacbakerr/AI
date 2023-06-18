import sys; args = sys.argv[1:]
import math, random

global LEARNING_RATE
LEARNING_RATE = 0.05
def hProduct(l1,l2):
    return [l1[i]*l2[i] for i in range(len(l1))]
def dotProduct(l1,l2):
    if not type(l1) is list:
        l1 = [l1]
    if not type(l2) is list:
        l2 = [l2]
    #making sure 1 item things are made into 1d
    return sum(hProduct(l1,l2))

class Node():
    def __init__(self, weights, activation_function):
        #weights is a list
        self.weights = weights
        self.activation_function = activation_function
    def forward(self, inputs):
        output = dotProduct(inputs, self.weights)
        output = self.activation_function(output)
        return output
class Layer():
    def __init__(self, nodes, flag=False):
        #nodes is a list of nodes
        self.nodes = nodes
        self.last_outputs = None #stores most recent outputs
        self.values_hitting = None
        self.e_values = None
        self.neg_gradients = None
        self.flag = flag
    def forward(self, inputs):
        outputs = []
        self.values_hitting = inputs
        for node in self.nodes:
            out = node.forward(inputs)
            outputs.append(out)
        self.last_outputs = outputs
        return outputs
    def backprop(self,forward_weights, forward_es):
        #calc e values
        #PROBLEM -- ORDERING OF WEIGHTS MAKING DOT PRODUCT DIFFICULT; will create reordered
        reordered_fw = []
        if type(forward_weights[0]) is list:
            for i in range(len(self.nodes)):
                temp=[]
                for node_weights in forward_weights:
                    temp.append(node_weights[i])
                reordered_fw.append(temp)
            forward_weights = reordered_fw
        e_values = []
        if self.flag:
            c = 0
            for i in range(len(self.nodes)):
                e_val = forward_weights[i]*forward_es[c] * logistic_deriv(self.last_outputs[i])
                e_values.append(e_val)
                c+=1
        else:
            for i in range(len(self.nodes)):
                e_val = dotProduct(forward_weights[i], forward_es)
                e_val = e_val * logistic_deriv(self.last_outputs[i])
                e_values.append(e_val)
        self.e_values = [e for e in e_values]
        #calculate neg gradients
        neg_gradients = []
        for i in range(len(self.nodes)):
            for q in range(len(self.values_hitting)):
                neg_grad = self.values_hitting[q]*self.e_values[i]
                neg_gradients.append(neg_grad)
        self.neg_gradients = neg_gradients
        #do weight updates -- need to check this, as gradients are in one list -- might need to make node level if doesnt work
        old_weights = [[v for v in node.weights] for node in self.nodes]
        grad_counter = 0
        for node in self.nodes:
            updated_weights = []
            for i in range(len(node.weights)):
                node.weights[i] = node.weights[i]+(self.neg_gradients[grad_counter]*LEARNING_RATE)
                grad_counter+=1
        return old_weights, e_values
        
class OutputLayer():
    def __init__(self,weights, activation_function):
        #in this case, weights is just a list
        self.activation_function = activation_function
        self.weights = weights
        self.last_outputs = None #stores most recent outputs
        self.e_values = None
        self.values_hitting = None
        self.neg_gradients = None
    def forward(self, inputs):
        outputs = []
        counter=0
        self.values_hitting = inputs
        for value in inputs:
            #value = self.activation_function(self.weights[counter]*value)
            value = self.weights[counter]*value
            outputs.append(value)
            counter+=1
        self.last_outputs = outputs
        return outputs
    def backprop(self, final_layer_errors):
        #update E values
        e_values = []
        e_values = final_layer_errors
        self.e_values = [val for val in e_values]
        #calculate negative gradients
        neg_gradients = []
        for i in range(len(self.weights)):
            neg_grad = final_layer_errors[i]*self.values_hitting[i]
            neg_gradients.append(neg_grad)
        self.neg_gradients = neg_gradients
        # go in the direction of negative gradients in weight update
        old_weights = [value for value in self.weights]
        for i in range(len(self.weights)):
            self.weights[i] = self.weights[i] + (self.neg_gradients[i]*LEARNING_RATE)
        return old_weights,e_values
        # need to use old weights for other layers, when finding deriv -- old or new E vals?

class Network():
    def __init__(self, layers, output_layer):
        #layers is a list of layers
        self.layers = layers
        self.output_layer = output_layer
    def forward(self, inputs):
        #inputs is a list of #s
        out = inputs
        for layer in self.layers:
            out = layer.forward(out)
        out = self.output_layer.forward(out)
        return out
    def summary(self):
        for layer in self.layers:
            print(len(layer.nodes))
        print(self.output_layer)
    def backprop(self, final_layer_errors):
        weights,e_values = self.output_layer.backprop(final_layer_errors)
        for layer in self.layers[::-1]:
            weights, e_values = layer.backprop(weights, e_values)
def t1(i):
    return i
def t2(i):
    if i <=0:
        return 0
    return i
def t3(i):
    return 1/(1 + math.exp(-i))
def t4(i):
    return (t3(i)*2)-1
def logistic_deriv(i):
    #t3 should be logistic
    return i*(1-i)
def makeNetworkOld(args,activation_function):
    weights = open(args[0])
    weights = weights.readlines()
    layer_sizes = []
    weights_list = []
    counter = 0
    print(weights[::-1])
    for line in weights[::-1]:
        line = line.split(' ')
        line = [item.strip() for item in line]
        #print(line)
        if counter == 0:
            layer_sizes.append(len(line))
            weights_list.append([float(val) for val in line])
        if counter == 1:
            layer_sizes.append(len(weights[::-1][0]))
            weights_list.append([float(val) for val in line])
        else:
            layer_sizes.append(len(weights_list[counter-1])/layer_sizes[counter-1])
            weights_list.append([float(val) for val in line])
        counter+=1
    layer_sizes = layer_sizes[::-1]
    weights_list = weights_list[::-1]

    #activation_function = eval(activation_function)
    if activation_function == 't1':
        activation_function=t1
    elif activation_function=='t2':
        activation_function=t2
    elif activation_function=='t3':
        activation_function=t3
    elif activation_function=='t4':
        activation_function=t4

    layers = []
    print(weights_list)
    print(layer_sizes)
    print('')
    for i in range(len(layer_sizes)):
        if i<len(layer_sizes)-1:
            weights = weights_list[i]
            l_size = layer_sizes[i]
            n_weights_per_node = len(weights)/l_size
            #print(n_weights_per_node)
            counter=1
            we=[]
            nodes = []
            for w in weights:
                we.append(w)
                if counter%n_weights_per_node==0:
                    node = Node([v for v in we],activation_function)
                    nodes.append(node)
                    we=[]
                counter+=1
            layer = Layer(nodes)
            layers.append(layer)
        else:
            #output layer
            output_layer = OutputLayer(weights_list[i],activation_function)
    model = Network(layers,output_layer)
    return model

def makeNetwork(args,activation_function,len_inputs):
    if activation_function == 't1':
        activation_function=t1
    elif activation_function=='t2':
        activation_function=t2
    elif activation_function=='t3':
        activation_function=t3
    elif activation_function=='t4':
        activation_function=t4

    weights = open(args[0])
    weights = weights.readlines()
    #print(weights)
    layer_sizes = []
    weights_list = []
    counter = 0
    n_nodes = len_inputs
    layers = []
    for weight_line in weights:
        weight_line = weight_line.split()
        ws = [float(item.strip()) for item in weight_line]
        n_nodes = len(ws)/n_nodes
        n_weights_per_node = len(ws)/n_nodes
        if counter == len(weights) -1:
            #output layer
            output_layer = OutputLayer(ws,activation_function)
            continue
        we = []
        nodes = []
        c=1
        for w in ws:
                we.append(w)
                if c%n_weights_per_node==0:
                    node = Node([v for v in we],activation_function)
                    nodes.append(node)
                    we=[]
                c+=1
        layer = Layer(nodes)
        layers.append(layer)
        counter+=1
    #activation_function = eval(activation_function)
    model = Network(layers,output_layer)
    return model

def makeNetworkSpecific(len_inputs,hidden_sizes,activation_function):
    #making network not working correctly
    if activation_function == 't1':
        activation_function=t1
    elif activation_function=='t2':
        activation_function=t2
    elif activation_function=='t3':
        activation_function=t3
    elif activation_function=='t4':
        activation_function=t4

    #print(weights)
    layer_sizes = []
    weights_list = []
    counter = 0
    n_nodes = len_inputs
    layers = []
    weights = [[random.uniform(0,1) for q in range(hidden_sizes[i])] for i in range(len(hidden_sizes))]
    #print(weights)
    for weight_line in weights:
        ws = weight_line
        n_nodes = len(ws)/n_nodes
        n_weights_per_node = len(ws)/n_nodes
        if counter == len(weights) -1:
            output_layer = OutputLayer(ws,activation_function)
            continue
        we = []
        nodes = []
        c=1
        for w in ws:
                we.append(w)
                if c%n_weights_per_node==0:
                    node = Node([v for v in we],activation_function)
                    nodes.append(node)
                    we=[]
                c+=1
        #print(len(nodes))
        layer = Layer(nodes)
        layers.append(layer)
        counter+=1
    layers[-1].flag = True
    model = Network(layers,output_layer)
    return model
def loss_function(preds, true_values):
    l = [(true_values[i]-preds[i]) for i in range(len(preds))]
    #l= [(((true_values[i]-preds[i])**2)/2) for i in range(len(preds))]
    return l
def train_epoch(model,X,y):
    epoch_error=0
    for batch_idx in range(len(X)):
        inputs = X[batch_idx]
        y_true = y[batch_idx]
        preds = model.forward(inputs)
        #preds = [int(p) for p in preds]
        final_layer_errors = loss_function(preds, y_true)
        model.backprop(final_layer_errors)#need to write the backprop method, to do process and update
        err =  sum([abs(val) for val in final_layer_errors])
        err = (err**2)/2
        epoch_error+=err
    return epoch_error

def weightSpecBuilder(layer_sizes, input_size, output_size):
    #layer_sizes is a list of hidden layers -- just hidden layers - no outputs
    #last of hidden size should be same as output_size
    size = input_size
    weights_list = []
    for hidden_size in layer_sizes:
        n_weights = size*hidden_size
        weights_list.append(n_weights)
        size = hidden_size
    weights_list.append(output_size)
    return weights_list
def createDataset(value, operator, size):
    X = []
    y = []
    less_counter = 0
    great_counter = 0
    while less_counter<size:
        x_val = random.uniform(-1.5,1.5)
        y_val = random.uniform(-1.5,1.5)
        res = (x_val**2) + (y_val**2)
        if res < value:
            less_counter+=1
        if operator == '<':
            y.append([int(res<value)])
        if operator == '<=':
            y.append([int(res<=value)])
        if operator == '>':
            y.append([int(res>value)])
        if operator == '>=':
            y.append([int(res>=value)])
        X.append([x_val, y_val, 1]) #include bias
    while great_counter<size:
        x_val = random.uniform(-1.5,1.5)
        y_val = random.uniform(-1.5,1.5)
        res = (x_val**2) + (y_val**2)
        if res < value:
            great_counter+=1
        if operator == '<':
            y.append([int(res<value)])
        if operator == '<=':
            y.append([int(res<=value)])
        if operator == '>':
            y.append([int(res>value)])
        if operator == '>=':
            y.append([int(res>=value)])
        X.append([x_val, y_val, 1]) #include bias
    return X,y
def train_model(model, epochs, X, y):
    error=0
    for epoch in range(epochs):
        error = train_epoch(model, X, y)
    return error

def findBestModel(X,y,len_inputs,len_outputs,weights_list,activation_function,hl_sizes):
    global LEARNING_RATE
    if len_outputs == 1:
        LR_RATES = [0.1]
        EPOCHS = [30000]
    else:
        LR_RATES = [0.1]
        EPOCHS = [20000]
    models = []
    best_error = 100000
    best_idx=0
    idx=0
    #assume just 1 LR and EPOCH combo total
    #for lr in LR_RATES:
    #    for epochs in EPOCHS:
    while best_error > 0.03:
        #LEARNING_RATE = lr
        LEARNING_RATE=LR_RATES[0]
        epochs = EPOCHS[0]
        model = makeNetworkSpecific(len_inputs,weights_list,activation_function)
        error = train_model(model, epochs, X, y)
        models.append(model)
        if error < best_error:
            best_error = error
            best_idx=idx
            #print('Error: ',best_error)
            printOutputs(len_inputs, len_outputs, hl_sizes, model)
        idx+=1
        if idx >= 5: #shouldn't take too many tries, if backprop is correct
            return models[best_idx], best_error
    return models[best_idx], best_error
    #try all options
def printOutputs(input_size, output_size, hidden_layer_sizes, model):
    layer_str='Layer counts '
    layer_str = layer_str+ str(input_size) +" "
    for size in hidden_layer_sizes:
        layer_str = layer_str + str(size)+" "
    layer_str = layer_str + str(output_size) + " "
    layer_str = layer_str.strip()
    print(layer_str)

    for layer in model.layers:
        weights_str = ''
        for node in layer.nodes:
            weights_str = weights_str+ ' '+ ' '.join([str(v) for v in node.weights])
        print(weights_str.strip())
    weights_str = ''
    for w in model.output_layer.weights:
        weights_str = weights_str + str(w) + " "
    print(weights_str.strip())
def main():
    activation_function = 't3'
    #process inputs
    inputs = args[0]
    if '<=' in inputs:
        operator = '<='
    elif '<' in inputs:
        operator = '<'
    elif '>=' in inputs:
        operator = '>='
    elif '>' in inputs:
        operator = '>'
    
    value = float(inputs.split(operator)[-1])
    len_inputs = 3
    len_outputs = 1
    dataset_size = 300
    epochs = 400
    hidden_layer_sizes = [3,3,2,len_outputs]
    weights_list = weightSpecBuilder(hidden_layer_sizes, len_inputs, len_outputs)
    model = makeNetworkSpecific(len_inputs,weights_list,activation_function)

    X,y = createDataset(value, operator, dataset_size)
    error = train_model(model, epochs, X, y)
    printOutputs(len_inputs, len_outputs, hidden_layer_sizes, model)
    print('Error: ',error)
   # print(output)

if __name__=='__main__':
    main()
# try: just train until error below 0.01, if after certain epoch limit (ex; 40k) hasnt worked, create model/start training again