import numpy as np
import matplotlib.pyplot as plt

# matching penny!!
# player match wants same. player miss wants opposite
# two populations x, and y. Both have types who want to play head, and types who want to play tails.

# payoff matrix A
#pay_off_match = np.array([[1, -1], [-1, 1]]) #matching pennies
#pay_off_match = np.array([[1,0],[0,1]]) #matching pennies 2.0
#pay_off_match = np.array([[10,0],[11,12]]) #subsidy game
pay_off_match = np.array([[3,0],[0,2]]) #battle of the sexes
print("A: " + str(pay_off_match))
# payoff matrix B
#pay_off_miss = np.array([[-1, 1], [1, -1]]) #matching pennies
#pay_off_miss = np.array([[0,1],[1,0]]) #matching pennies 2.0
#pay_off_miss = np.array([[10,11],[0,12]]) #subsidy game
pay_off_miss = np.array([[2,0],[0,3]]) #battle of the sexes
print("B: " + str(pay_off_miss))

for i in range(0, 11):
    for r in range(0,11):
        # probability player match playing heads x[0]
        prob_head_match = i/10
        # probability player miss playing heads y[0]
        prob_head_miss = r/10

        # population match x [x[0], x[1]] (column)
        prob_match = np.array([[prob_head_match], [1 - prob_head_match]])
        # population miss y [y[0], y[1]] (column)
        prob_miss = np.array([[prob_head_miss], [1 - prob_head_miss]])
        print("--------ROUND" + str(i) + "--" + str(r) + "--------")
        # player match:
        # expected fitness of population match x: Ay
        fitness_match = np.matmul(pay_off_match, prob_miss)
        print("Ay: " + str(fitness_match))
        # average population fitness match: xTAy
        mean_fitness_match = np.matmul(prob_match.transpose(), fitness_match)[0][0]
        print("xTAy: " + str(mean_fitness_match))
        # xi*((Ay)i - xTAy)
        change_match_heads = (prob_match[0]*(fitness_match[0] - mean_fitness_match))[0]
        print("dx heads: " + str(change_match_heads))
        # x = x + dx
        new_prob_match = prob_match + np.array([[change_match_heads], [-change_match_heads]])
        print("x: " + str(new_prob_match))

        # player miss:
        # expected fitness of population miss y: Bx
        fitness_miss = np.matmul(pay_off_miss, prob_match)
        print("Bx: " + str(fitness_miss))
        # average population fitness miss: yTBx
        mean_fitness_miss = np.matmul(prob_miss.transpose(), fitness_miss)[0][0]
        print("yTBx: " + str(mean_fitness_miss))
        # yi*((Bx)i - yTBx)
        change_miss_heads = (prob_miss[0]*(fitness_miss[0] - mean_fitness_miss))[0]
        print("dy heads: " + str(change_miss_heads))
        # y = y + dy
        new_prob_miss = prob_miss + np.array([[change_miss_heads], [-change_miss_heads]])
        print("y: " + str(new_prob_miss))

        plt.arrow(prob_match[0][0], prob_miss[0][0], change_match_heads, change_miss_heads)


plt.rcParams["figure.figsize"] = [7.50, 7.50]
plt.rcParams["figure.autolayout"] = True

plt.title("Matching pennies")
plt.xlabel("Probability player1 playing heads")
plt.ylabel("Probability player2 playing heads")

plt.show()