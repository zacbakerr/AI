The first neural network lab is to ensure that a script can take the specification for a neural net and correctly implement it.  The command line input to a submitted script is:
weightFile.txt TransferFunctionSpec inputs ...

The TransferFunctionSpec is one of:
T1 for a linear function, f(x)=x
T2 for a ramp function (f(x)=x for x>=0)
T3 for a logistic function (f(x)=1/(1+e^-x))
T4 for twice the T3 logistic function less 1.

The weightFile.txt is a text file with a sequence of (space separated) numbers (floats) on each line.  The numbers on a line n (1-based) list the weights on each of the signals going from (0-based) layer n-1 to layer n, except that the final line is for the weights leading to the outputs from the final layer.  The organization of the numbers within a line is to have the major order be by the nodes on the right (the higher layer number), and the minor order is by the nodes on the left (the lower layer number).  For example, if nodes 1, 2, 3 feed into nodes 4 and 5, the corresponding weights order would be:
w14 w24 w34 w15 w25 w35

The inputs ... are numbers that specify the inputs presented to the neural net.

The output of the script should be a line where each output appears on that line.  They may be space and/or comma separated.  The grader script looks for the final line of the output with the correct amount of numbers on it.  Output values must be within 3/1000 of the correct value to be accepted as correct.
