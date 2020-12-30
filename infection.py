import numpy as np
import matplotlib.pyplot as plt

# functions that map [0,inf) to [0,1) for duration probability it all maps p(d=1,x) = x
def p_dx1(d, x):
    return 1 - 1 / (x / (1 - x) * d + 1)

def p_dx2(d, x):
    return d * x / (1 + (d - 1) * x)

def p_dx3(d, x):
    return 1 - np.exp(d * np.log(1 - x))

def p_dx4(d, x):
    return d * x / (d * x + np.exp(d * np.log(1 - x)))

def p_dx5(d, x):
    return np.arctan(d * np.tan(np.pi / 2 * x)) / (np.pi / 2)

def infection(distance=1, duration = 1, spreader_dict = {'status' : 'SICK', 'spreading_factor': 1}, infection_probability =0.01 ):
    """
    :param distance: distance of subject from spreader in [m']
    :param duration: meeting duration in [hours]
    :param spreader_dict: dictionary that must include the follwoing keys:
                                                'status' - HEALTHY, INFECTED (infected), SICK
                                                'spreading_factor' - value that quantify the infection probability by the spreder in relevance to an average person
    :param infection_probability: mean probability for infection in an interaction from distance of less than 1m that last 1 hour float[0..1]
    :return: subject status post interaction with spreader
        True -  subject is infected from spreader
        False  - subject is not infected from spreader

    data about relation between distance from subject to spreader is taken from:
    The Conversation (Philip Russo) - https://theconversation.com/coronavirus-why-should-we-stay-1-5-metres-away-from-each-other-134029
    Wake Forest research abut Inflouenza spreading - https://www.ncbi.nlm.nih.gov/pubmed/23372182
    data about spreaders distribution is taken from pervious two plus:
    Nature article about 20-80 rule that 20% of petiontes usually spread 80% of the epidemic - https://www.ncbi.nlm.nih.gov/pubmed/16292292
    """
    INFECTED_spreading_factor = 0.5
    distance_decay = 4.5 # 4.5 times per meter
    distance_factor = float(distance<=1) + float(distance>1)/(distance_decay**(distance-1)) # post 1 m decay of 4.5 times per any aditional meter
    if spreader_dict['status'] == "HEALTHY" :
        spreading_factor = 0
    if spreader_dict['status'] == "INFECTED" :
        spreading_factor = spreader_dict['spreading_factor'] * INFECTED_spreading_factor * distance_factor
    if spreader_dict['status'] == "SICK" :
        spreading_factor = spreader_dict['spreading_factor'] * distance_factor

    p_d1 =  spreading_factor * infection_probability   # p(duration=1)
    interaction_infection_probability = p_dx3 (d = duration, x= p_d1) # flatten to 0..1
    infection_draw = np.random.uniform()
    is_infected =  infection_draw < interaction_infection_probability
    return is_infected

if __name__ == "__main__":
    count = 0
    n = 100000
    distance = 1 # 1 m
    duration = 0.25
    spreader_dict = {'status': 'SICK' , 'spreading_factor': 1}
    infection_probability = 0.01

    for i in range(n):
        inf = infection(distance, duration, spreader_dict , infection_probability )
        # if inf == True : print("i : {}, inf : {}".format(i, inf))
        count += inf
    print("maen inf:  {}".format(count / n))
    print("delta from expected:  {}".format(infection_probability* spreader_dict['spreading_factor']*duration/4.5**distance - count/n))

    pp = np.arange(0.001, 0.011, 0.001)

    n = 100
    d = np.logspace(-3, 3, num=n)

    i = 1
    for x in pp:
        plt.figure(i)
        i +=1
        p1 = p_dx1(d, x)
        p2 = p_dx2(d, x)
        p3 = p_dx3(d, x)
        p4 = p_dx4(d, x)
        p5 = p_dx5(d, x)

        plt.scatter(d, p1, label=["p1"])
        plt.scatter(d, p2, label=["p2"])
        plt.scatter(d, p3, label=["p3"])
        plt.scatter(d, p4, label=["p4"])
        plt.scatter(d, p5, label=["p5"])

        plt.xlabel("d")
        plt.ylabel("p")
        plt.title("p = {}".format(x))
        plt.legend(loc='upper left')
        plt.show()
