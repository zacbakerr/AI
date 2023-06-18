import sys; args = sys.argv[1:]

def main():
   val = args[1].split("*y")[1]
   arg = val[0]
   if val[1].isnumeric(): val = val[1:]
   else: val = val[2:]
   val = float(val)**0.5

   weights = []
   with open(args[0]) as file:
      for line in file:
         if line[0].isnumeric() or line[0] == "-":
            tempWeights = []
            for weight in line.split(" "):
               tempWeights.append(float(weight.replace(",", "")))
            weights.append(tempWeights)
   
   layerCounts = [1 for i in range(len(weights)+1)]
   layerCounts[0] = 2
   for i in range(1, len(layerCounts)):
      if i == len(weights): layerCounts[i] = 1
      else: layerCounts[i] = len(weights[i-1])//layerCounts[i-1]
   
   layerCounts[0] = 3
   tempWeightList = []
   for i, weight in enumerate(weights[0]):
      tempWeightList.append(weight)
      if i % 2 == 0: tempWeightList.append(0)
   tempWeightList.append(0)
   for i, weight in enumerate(weights[0]):
      tempWeightList.append(weight)
      if ((i-1) % 2 == 0) and i != len(weights[0])-1: tempWeightList.append(0)
   weights[0] = tempWeightList

   for i in range(1, len(weights)):
      tempWeightList = []
      nodes = layerCounts[i]
      for j, weight in enumerate(weights[i]):
         tempWeightList.append(weight)
         if len(tempWeightList) % nodes == 0:
            for k in range(nodes): tempWeightList.append(0)
      for j, weight in enumerate(weights[i]):
         if len(tempWeightList) % nodes == 0:
            for k in range(nodes): tempWeightList.append(0)
         tempWeightList.append(weight)
      weights[i] = tempWeightList
      layerCounts[i] = layerCounts[i]*2
   
   for i in range(len(weights[0])): 
      weights[0][i] = weights[0][i] / val
   layerCounts.append(1)

   if arg == ">": weights.append([0.68394])
   else: weights.append([1.85914])

   tempWeightList = []
   for weight in weights[-2]:
      if weight != 0: tempWeightList.append(weight)
   weights[-2] = tempWeightList

   for i in range(len(weights[-2])):
      if "<" in args[1]: weights[-2][i] = weights[-2][i] * -1

   layerString = "Layer Counts: "
   layerString += str(layerCounts)
   print(layerString)
   for weight in weights:
      tempString = ""
      for w in weight:
         tempString += str(w) + " "
      print(tempString)

if __name__ == "__main__": main()

# Zachary Baker, Pd. 4, 2024