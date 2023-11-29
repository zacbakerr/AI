# Bandits

A k-armed bandit is a list of Gaussian distributions, each with its own mean and standard deviation.  Each time the bandit is queried (called a "pull") with a specific arm, it will report a value for that Gaussian.  Submitted code will be given 10-armed bandits, and for each bandit the code will pull 1000 times, learning the response to each pull, and deciding which arm to pull next.  The goal is to maximize the sum of the values reported from each pull.

Submitted code is to implement a single function:

def bandit(testNum, armIdx, pullVal):
  
  #Bandit pull maximizer; if testNum ==0 => new bandit initialization; armIdx contains the number of arms (10); pullVal not used > 0 => 
  
  #testNum contains the pull number (from 1 to 999)
  
  #armIdx has the index of the arm that was requested to be pulled in the prior call
  
  #pullVal has the value that resulted from the pull
  
  #The return val is always the idx of the next arm to pull in [0, of arms)

The grader will throw 10,000 10-arm bandits at the code.  For each bandit, it will call the bandit() routine with an initialization directive.  Subsequently, for each arm that it receives, the grader will do a pull on that bandit arm and report the pull value with the next call.  The submitted code should use globals to update its understanding of the bandit so that it can select the best arm to pull.  The submitted code has no way to examine the bandit - it's only information about the bandit comes from the pulls that it requests.

A new bandit has the mean of each arm initialized with random.gauss(0,1) - a Gaussian with mean 0 and standard deviation 1.  Once the arm means are set, they do not vary for a given bandit.

The goal is to achieve a reward of near 1500.

There are no command line calls, so the only libraries which might have reason to be imported are math and possibly random.
