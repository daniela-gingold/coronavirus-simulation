import numpy as np
from scipy.special import factorial

def is_symptomatic(p_asymptomatic = 0.25):
    """
    :return:
    False - asymptomatic
    True - symptomatic

    defalt 25% is taken form rugth estimate by
    CDC - gym in Cheonan reprot (24.5%) https://www.cdc.go.kr/board/board.es?mid=a30501000000&bid=0031&list_no=366658&act=view#
    Estimating the asymptomatic proportion of coronavirus disease 2019 (COVID-19) cases on board the Diamond Princess cruise ship, Yokohama, Japan (17.9-33.3%)-
                                        https://www.dw.com/en/up-to-30-of-coronavirus-cases-asymptomatic/a-52900988
    CNN report  - https://edition.cnn.com/2020/03/14/health/coronavirus-asymptomatic-spread/index.html
    DW article - https://www.dw.com/en/up-to-30-of-coronavirus-cases-asymptomatic/a-52900988
    """

    x = np.random.uniform()  # uniform between 0..1
    symptomatic =  p_asymptomatic < x
    return symptomatic
        

def days_to_symptoms():
    """
    :return
    days to onset of symptoms, if return -1 asymptomatic and sympoms will not apear

         probability table:
         days after infection	p	       F	  F symptoms
            1	             0.0001	    0.000075	0.0001
            2	             0.018675	0.01875	    0.025
            3	             0.07125	0.09     	0.12
            4	             0.1425	    0.2325	    0.31
            5	             0.135	    0.3675	    0.49
            6	             0.13875	0.50625	    0.675
            7	             0.07875	0.585	    0.78
            8	             0.0525	    0.6375	    0.85
            9	             0.0375	    0.675	    0.9
            10	             0.0375	    0.7125	    0.95
            11	             0.015	    0.7275	    0.97
            12	             0.003	    0.7305	    0.974
            13	             0.018375	0.748875	0.9985
            14	             0.001125	0.75	    1
            Asymptomatic	 0.25	    1
    """
    F_symptoms = np.array([0.0001,
                   0.025,
                   0.12,
                   0.31,
                   0.49,
                   0.675,
                   0.78,
                   0.85,
                   0.9,
                   0.95,
                   0.97,
                   0.974,
                   0.9985,
                   1 ])
    p_asymptomatic = 0.25
    F = F_symptoms * (1-p_asymptomatic)
    x = np.random.uniform() # uniform between 0..1
    n = len(F)
    for i in range(n) : # run over all incubation days
        if x< F[i]:
            return i+1
    return -1    # we are asymptomatic


def survive_by_age (age=44):
    """
    :param
    age - human age in years
    :return
    0 - dead
    1 - live

    by statistics of
    Avg of presentage in china an korea
    Korea from CDC 1 Apr report https://www.cdc.go.kr/board/board.es?mid=a30402000000&bid=0030
    china from https://ourworldindata.org/coronavirus
    """
    death_by_decade = [
                        0,            # 0-10 precentage
                        0,            # 10-20 precentage
                        0.1,          # 20-30 precentage
                        0.148685492,  # 30-40 precentage
                        0.237792895,  # 40-50 precentage
                        0.918096515,  # 50-60 precentage
                        2.723694779,  # 60-70 precentage
                        7.495440729,  # 70-80 precentage
                        16.6920354    # 80+ precentage
                        ]

    decade_age = int( np.minimum (np.ceil(age / 10),8) ) # trim to 8
    p_death = death_by_decade[decade_age]/100
    x = np.random.uniform()  # uniform between 0..1
    survive =x < p_death
    return survive


def days_to_recovery(sympotmatic = True):
    """
    :param
    sympotmatic = True
    :return:
    # of days to recovery (corona is over) after syndroms onset

    for recovery form symptoms data by reaserch form the Lancet in march 30 https://www.thelancet.com/journals/laninf/article/PIIS1473-3099(20)30243-7/fulltext
    for asymptomatic data data is estimated by curve of the graph of # of dead vc # of survived in korea the proportion is stable ~ 12 days after
    """
    if (sympotmatic == False):
        mu  = 12
        std = 2 # assuming that 4 sigmma = 95% is in 4 days
        draw = std * np.random.randn() + mu
    else:
        mu = 24.7 # mean value
        split = np.random.uniform()<0.5 # random choise if we are on left side or right side of the distribution
        if split == 0 : #left side of the curve
            std = 0.45 #  95% is ~ 22.9 days so 4*sigma = 24.7-22.9
            draw = std * np.random.randn() + mu
            if draw > mu :
                draw = mu-(draw-mu)
            draw = np.maximum(draw,2) # trim in 2 no faster recovery
        elif split == 1: #right side of the curve
            std = 0.85   # 95% is ~ 28.1 days so 4*sigma = 28.1-24.7
            draw = std * np.random.randn() + mu
            if draw < mu:
                draw = mu + (mu - draw)
    days = np.round(draw)
    return days

def days_to_death():
    """
    :return:
    # of days to recovery (corona is over) after syndroms onset

    for recovery form symptoms data by reaserch form the Lancet in march 30 https://www.thelancet.com/journals/laninf/article/PIIS1473-3099(20)30243-7/fulltext
    """
    mu = 17.8 # mean value
    split = np.random.uniform()<0.5 # random choise if we are on left side or right side of the distribution
    if split == 0 : #left side of the curve
        std = 0.225 #  95% is ~ 22.9 days so 4*sigma = 17.8-16.9
        draw = std * np.random.randn() + mu
        if draw > mu :
            draw = mu-(draw-mu)
        draw = np.maximum(draw,2) # trim in 2 no faster recovery
    elif split == 1: #right side of the curve
        std = 0.35   # 95% is ~ 28.1 days so 4*sigma = 19.2-17.8
        draw = std * np.random.randn() + mu
        if draw < mu:
            draw = mu + (mu - draw)
    days = np.round(draw)
    return days

def get_spreading_factor():
    """
    :return: spreading_factor - random mutiplayer to avarage virus spreading capability  either 0.2 ,0.5 1.25, 2.5, 6.25, 8.75 by F_population probabilites

    data taken from the following sources :
    The Conversation (Philip Russo) - https://theconversation.com/coronavirus-why-should-we-stay-1-5-metres-away-from-each-other-134029
    Wake Forest research abut Inflouenza spreading - https://www.ncbi.nlm.nih.gov/pubmed/23372182
    Nature article about 20-80 rule that 20% of petiontes usually spread 80% of the epidemic - https://www.ncbi.nlm.nih.gov/pubmed/16292292
    """
    F_population  = np.array(       [0.576923077,0.807692308, 0.884615385, 0.923076923, 0.961538462, 1   ] )
    spreading_factor_vec = np.array([0.2        ,0.5        , 1.25       , 2.5        , 6.25       , 8.75 ] )
    x = np.random.uniform()  # uniform between 0..1
    n = len(F_population)
    for i in range(n):  # run over all incubation days
        if x <= F_population[i]:
            spreading_factor = spreading_factor_vec[i]
            break
    return spreading_factor

def days_to_quarantine (days_limit = 14, lamda = 1.5):
    """
    :param days_limit: integer max number of days to quarantine
    :param lamda:  lamda factor of Possion distribution p(k,lamda)= landa^k *exp(-lamda) / k!
    :return: the number of days from symptoms to quarantine by poisson distribution with lamda factor
                if the ramdom choise is >= days_limit then return -1 meaning no quarentine
    """
    days_limit = int(days_limit)
    draw = np.random.uniform()
    p_poi = 0
    days= -1 # deafult no quarentine, in case draw is bigger or equale days_limit
    for day in range (days_limit):
        p_poi += (lamda**day) * np.exp(-lamda) / factorial(day)
        if draw <p_poi :
            days = day
            break
    return days

def get_patinet_dict (age=44):
    """
    :param age: age of patient
    :return: patient_dict
    {
        "age" : pataint age
        "spreading_factor" : spreading factor by population statistics , mean sperading factor 1
        "survivel" : False - will die, True will survive
        "symptomatic" : False - Asymptomatic (no symptoms), True - symptoms apear and dessise may be tracked
        "days_to_symptoms" : number of days to symptoms
        "days_to_exit" : days to recovery if survivel = True , days to die if survivel = False }
    """
    spreading_factor = get_spreading_factor()
    symptomatic = is_symptomatic()
    if symptomatic == True:
        days_to_symptoms_ = days_to_symptoms()
        survivel = survive_by_age (age)
        if survivel == False:
            days_to_exit = days_to_death()
        elif survivel == True:
            days_to_exit = days_to_recovery(sympotmatic = True)
        days_to_quarantine_ = days_to_quarantine(days_limit=days_to_exit)
    elif symptomatic == False:
        survivel = True
        days_to_symptoms_ = -1
        days_to_exit = days_to_recovery(sympotmatic = False)
        days_to_quarantine_ = -1
    paitent_dict = {
        "age" : age ,
        "survivel" : survivel ,
        "symptomatic" : symptomatic ,
        "days_to_symptoms" : days_to_symptoms_ ,
        "days_to_exit" : days_to_exit ,
        "days_to_quarantine" : days_to_quarantine_ ,
        "spreading_factor" : spreading_factor
    }
    return paitent_dict


if __name__ == "__main__":

    count = 0
    n = 10000
    for i in range(n):
        dtq = days_to_quarantine(days_limit=1000)
        # print("i : {}, dtq : {}".format(i, dtq))
        count += dtq
    print("maen dtq:  {}".format(count / n))


    count = 0
    n = 1000
    for i in range(n):
        sf = get_spreading_factor()
        #if sf ==8.75 : print("i : {}, sf : {}".format(i, sf))
        count += sf
    print("maen sf:  {}".format(count / n ))


    count = 0
    n = 100000
    for i in range (n):
        symp = is_symptomatic()
        count += int(symp)
    print ("% symp {}".format(count/n*100))


    x1=days_to_symptoms()
    print("days_to_symptoms = {}".format(x1))
    s = survive_by_age(77)
    print("survive_by_age(77) = {}".format(s))
    days_to_recovery_res = days_to_recovery(sympotmatic = True)
    print("days_to_recovery(sympotmatic = True) = {}".format(days_to_recovery_res))
    days_to_death_res = days_to_death()
    print("days_to_death = {}".format(days_to_death_res))

    paitent_dict = get_patinet_dict(age=50)
    print("paitent_dict = {}".format(paitent_dict))
