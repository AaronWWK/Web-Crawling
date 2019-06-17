from math import factorial
import numpy as np
import matplotlib.pyplot as plt


## the change to win a round is variable, to get the probability of winning the game with 4:k 
wins = np.arange(0,1.05,0.005)

def probability(wins):
    probs = []
    for win in wins:
        prob = 0
        for k in range(4):
            prob += (win**4)*(factorial(k+3)/(factorial(3)*factorial(k)))*((1-win)**k)
        probs.append(prob)
    return probs

plt.figure(figsize=(10,9))
plt.plot(wins, probability(wins), c = '#009ACD')
plt.xlim(0,1)
plt.ylim(0,1)
plt.xticks(np.arange(0,1.05,0.05))
plt.yticks(np.arange(0,1.05,0.05))
plt.grid(c='#00BFFF', linewidth = 0.2)
ax = plt.gca()
ax.spines['right'].set_color('#009ACD')
ax.spines['top'].set_color('#009ACD')
ax.spines['left'].set_color('#009ACD')
ax.spines['bottom'].set_color('#009ACD')
plt.xlabel('probability of winning point')
plt.ylabel('probability of winning game')
plt.title('Tennis Game Probability')
plt.show()



## the change to win a round is 0.6, to get the probability of winning with time:k
times = np.arange(1,101,1)
def probability2(times):
    win = 0.6
    probs = []
    for time in times:
        prob = 0
        for k in range(time):
            prob += (win**time)*(factorial(k+time-1)/(factorial(time-1)*factorial(k)))*((1-win)**k)
        probs.append(prob)
    return probs
p =probability2(times)

plt.figure(figsize=(10,9))
plt.plot(times, probability2(times), c = '#009ACD')
plt.xlim(0,100)
plt.ylim(0.55,1)
plt.xticks(np.arange(0,101,5))
plt.yticks(np.arange(0.55, 1, 0.05))
plt.grid(c='#00BFFF', linewidth = 0.2)
ax = plt.gca()
ax.spines['right'].set_color('#009ACD')
ax.spines['top'].set_color('#009ACD')
ax.spines['left'].set_color('#009ACD')
ax.spines['bottom'].set_color('#009ACD')
plt.xlabel('number of points to win game')
plt.ylabel('probability of winning game')
plt.title('Tennis Game Probability')
plt.show()



binom = {}
for n in range(0, 1000):
    for k in range(0, n + 1):
        if k == 0 or k == n:
            binom[(n, k)] = 1
        else:
            binom[(n, k)] = binom[(n - 1, k)] + binom[(n - 1, k - 1)]
binom
# Compute Win Probability
def prob(n, p):
    total = 0
    for x in range(0, n):
        total += ((1 - p) ** x) * binom[(n - 1 + x, x)]
    total *= (p ** n)
    return total

prob(4,0.6)
