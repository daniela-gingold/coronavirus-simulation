import matplotlib.pyplot as plt
import numpy as  np
import pygame
import pandas as pd
import random
from patient_dict import *
from infection import *
from age_dist import *
from dist_plot import *
from religious_prob_dist import *

class Resident:
    def __init__(self,homeLoc,city):
        ageRange = getAge(random.random(),city)
        self.age = random.randint(ageRange[0],ageRange[1])
        self.speed = 3 #max speed
        self.sick = HEALTHY
        self.sickDays = 0
        self.homeLoc = {'x':homeLoc[0],'y':homeLoc[1]}
        self.currLoc = {'x':homeLoc[0],'y':homeLoc[1]}
        self.infectionSource = INFECTION_SOURCE['healthy']
        sickParams = get_patinet_dict (self.age)
        self.survivel = sickParams['survivel']
        self.symptomatic = sickParams['symptomatic']
        self.incubationPeriod = sickParams['days_to_symptoms']
        self.daysToRecover = sickParams['days_to_exit']
        self.daysToQuarantine = sickParams['days_to_quarantine']
        self.spreading_factor = sickParams['spreading_factor']
        self.religious = getVoteProb(city)>random.random()
        
    def setCurrLoc(self,x=None,y=None):
        if x!=None:
            self.currLoc['x']=x
            self.currLoc['y']=y
        else:
            self.currLoc = self.homeLoc.copy()
    
    def atHome(self):
        return (self.currLoc['x'] == self.homeLoc['x'] 
                and self.currLoc['y'] == self.homeLoc['y'])
    
    def ageRestrictions(self):
        return not (ALLOWD_AGE[0]<=self.age<=ALLOWD_AGE[1])


class House:
    def __init__(self,residents,foodLeft):
        self.residents = residents
        self.foodLeft = foodLeft
        self.salary = 20
        self.superPeriod = np.random.randint(SUPER_PERIODS)
        
        
    def goToSuper(self):
        peopleGoing = np.random.randint(1,3)
        i = 0
        for p in range(len(self.residents)):
            if ( not self.residents[p].ageRestrictions() and
                ((self.residents[p].sick == DEAD and self.residents[p].daysToQuarantine > 0 ) 
                 or  self.residents[p].sick < DEAD and self.residents[p].atHome())):
                i+=1
                SUPER.addCustomer(self.residents[p])
                self.addFood(int(SUPER_TIMES/STEP_PERIOD))
                if i==peopleGoing : break
       
    def goPrey(self):
        peopleGoing = np.random.randint(1,3)
        i = 0
        for p in range(len(self.residents)):
            if (self.residents[p].religious and not self.residents[p].ageRestrictions() and
                ((self.residents[p].sick == DEAD and self.residents[p].daysToQuarantine > 0 ) 
                 or  self.residents[p].sick < DEAD and self.residents[p].atHome())):
                
                i+=1
                SYNAGOGUE.addBeliver(self.residents[p])
                if i==peopleGoing : break

        
    def addFood(self,quantity):
        self.foodLeft+=quantity
        
    def eatFood(self,superPeriod):
        if self.superPeriod == superPeriod:
            self.foodLeft -= min(self.foodLeft,np.random.randint(len(self.residents),3*len(self.residents)))
            if self.foodLeft<len(self.residents):
                self.goToSuper()
        
    def updateSick(self):
        for r1 in self.residents:
            if DEAD > r1.sick > HEALTHY:                    
                if r1.sickDays == 1:
                    for r2 in self.residents:
                        if r2.sick == HEALTHY:
                            r2.infectionSource = INFECTION_SOURCE['home_source']
                            r2.sick = INFECTED
                            r2.sickDays = 1   
                if r1.symptomatic:
                    if r1.sickDays > r1.incubationPeriod :
                        r1.sick=SICK
                if r1.sickDays > r1.daysToRecover:
                    if r1.survivel:
                        r1.sick=IMMUNED
                    else: 
                        r1.sick=DEAD
                    r1.sickDays=-1
                r1.sickDays += 1
            


class Super:
    def __init__(self,location):
        self.location = location
        self.customers = []
    
    def addCustomer(self,customer):
        loc = self.location
        customer.currLoc['x'] = np.random.randint(loc[0],loc[1])
        customer.currLoc['y'] = np.random.randint(loc[0],loc[2])
        stepLeft = SUPER_TIMES/STEP_PERIOD

        self.customers.append({'customer':customer,'stepsLeft':stepLeft}) # (customer ,  steps remaining befor returning home)
        
    def nextStep(self):
        nextCustomers = []
        for c in self.customers:
            c['stepsLeft'] -= 1
            if c['stepsLeft']<1:
                c['customer'].setCurrLoc()
            else: 
                stepX,stepY = [np.random.randint(-c['customer'].speed,c['customer'].speed+1),
                               np.random.randint(-c['customer'].speed,c['customer'].speed+1)]
                if stepX>0:
                    nextX = min(c['customer'].currLoc['x']+stepX,self.location[1])
                else:
                    nextX = max(c['customer'].currLoc['x']+stepX,self.location[0])
                if stepY>0:
                    nextY = min(c['customer'].currLoc['y']+stepY,self.location[2])
                else: 
                    nextY = max(c['customer'].currLoc['y']+stepY,self.location[0])
                c['customer'].setCurrLoc(nextX,nextY)
                nextCustomers.append(c)
        self.customers = nextCustomers
        self.updateSick()
        
        
    def updateSick(self):
        for c1 in self.customers:
            if DEAD>c1['customer'].sick >= INFECTED:
                for c2 in self.customers:
                    if c2['customer'].sick == HEALTHY:
                        d = ((c1['customer'].currLoc['x']-c2['customer'].currLoc['x'])**2 + 
                             (c1['customer'].currLoc['y']-c2['customer'].currLoc['y'])**2 )**(0.5)
                        
                        
                        spreader_dict = {'status' : ['INFECTED','SICK'][c1['customer'].sick-INFECTED],
                                         'spreading_factor': c1['customer'].spreading_factor}
                        infection_prob_scaled = INFECTION_PROB * STEP_MINUTES / 60
                        c2['customer'].sick = max(HEALTHY, infection(d, 1, spreader_dict, infection_prob_scaled) * INFECTED)
                        if c2['customer'].sick==INFECTED:
                            c2['customer'].infectionSource = INFECTION_SOURCE['super_source']
                            c2['customer'].sickDays = 1
                            

class Synagogue:
    def __init__(self,location):
        self.location = location
        self.believers = []
        self.emptySeats = self.getEmptySeats()
        random.shuffle(self.emptySeats)
        self.waitingList = []
        
    def addBeliver(self,believer):
        if len(self.emptySeats)>0:
            loc = self.emptySeats.pop()
        else: 
            self.waitingList.append(believer)
            return
        believer.setCurrLoc(loc[0], loc[1])
        
        self.believers.append({'believer':believer,'stepsLeft':PRAY_TIME}) 
        
    def getEmptySeats(self,space=2):
            return [(i,j) for i in range(1,self.location[1],SPACE+1) 
                               for j in range(self.location[0],self.location[2],SPACE+1)]
            
    
    def nextStep(self):
        nextBelievers = []
        for b in self.believers:
            b['stepsLeft'] -= 1
            if b['stepsLeft']<1: #return home
                self.emptySeats.append((b['believer'].currLoc['x'],b['believer'].currLoc['y']))
                b['believer'].setCurrLoc()
            else: 
                nextBelievers.append(b)
        self.believers = nextBelievers
        self.updateSick()
        

            
    def updateSick(self):
        for b1 in self.believers:
            if DEAD>b1['believer'].sick >= INFECTED:
                for b2 in self.believers:
                    if b2['believer'].sick == HEALTHY:
                        d = ((b1['believer'].currLoc['x']-b2['believer'].currLoc['x'])**2 + 
                             (b1['believer'].currLoc['y']-b2['believer'].currLoc['y'])**2 )**(0.5)
                        
                        
                        spreader_dict = {'status' : ['INFECTED','SICK'][b1['believer'].sick-INFECTED],
                                         'spreading_factor': b1['believer'].spreading_factor}
                        infection_prob_scaled = INFECTION_PROB * STEP_MINUTES / 60
                        b2['believer'].sick = max(HEALTHY, infection(d, 1, spreader_dict, infection_prob_scaled) * INFECTED)
                        if b2['believer'].sick==INFECTED:
                            b2['believer'].infectionSource = INFECTION_SOURCE['synagogue_source']
                            b2['believer'].sickDays = 1
            


class Corona:            
    def updateData(self,data, stats, progress):
        data = data.append(pd.Series(), ignore_index=True)
        data['immuned'][stats[5]] = stats[0]
        data['healthy'][stats[5]] = stats[1]
        data['infected'][stats[5]] = stats[2]
        data['sick'][stats[5]] = stats[3]
        data['dead'][stats[5]] = stats[4]
        progress[0].append(stats[0]) 
        progress[1].append(stats[1]) 
        progress[2].append(stats[2]) 
        progress[3].append(stats[3]) 
        progress[4].append(stats[4])
        stats[5]+=1
        
        return data , stats ,progress
                                
    def creatBaseMap(self,size=5,residents=False,synagogue=True): # draw residents? True only at initilization
        HOME = np.zeros((5,5))
        HOME[0,:]=WALL
        HOME[:,0]=WALL
        if residents:
            HOME[2:4,2:4]=HEALTHY
        
        MAP = np.ones(((size * (len(HOME)+2)) + 1,(size * len(HOME)) + 1)) * WALL
        
        for i in range(0,len(MAP)-1,len(HOME)):
            for j in range(0,len(MAP[0])-1,len(HOME)):
                MAP[i:i+len(HOME),j:j+len(HOME)]=HOME
        
        synagogueSize = int(size*len(HOME)/2)
        if synagogue:
            SYNAGOGUE = np.zeros((11,synagogueSize))
            SYNAGOGUE[[0,-1],:]=WALL
            SYNAGOGUE[:,[0,-1]]=WALL

        SUPER = np.zeros((11,size*len(HOME) + 1 - synagogueSize))
        SUPER[[0,-1],:]=WALL
        SUPER[:,[0,-1]]=WALL
        
        
        MAP[:len(SUPER),:len(SUPER[0])]=SUPER
        MAP[:len(SYNAGOGUE),len(SUPER[0]):len(MAP[0])] = SYNAGOGUE
    
        return MAP, SUPER , SYNAGOGUE
    
    
    def creatMap(self,houses=5,initialSicks=1,city='general',synagogue=True,foodSupply=50):    
        MAP, SUPER , SYNAGOGUE = self.creatBaseMap(houses,True,synagogue)
        houses=[]
        for x in range(1,len(MAP)-1):
            for y in range(1,len(MAP[0])-1):
                if MAP[x][y]==HEALTHY and MAP[x-1][y]==0 and MAP[x][y+1]==0:
        
                    residents = [Resident((x,y-1),city),
                                 Resident((x,y),city),
                                 Resident((x+1,y-1),city),
                                 Resident((x+1,y),city)]
                    
                    houses.append(House(residents,np.random.randint(5,50)))
        
        random.shuffle(houses)
        for i in range(int(len(houses)/2)):
            if i > initialSicks: break
            res = random.randint(0,len(houses[i].residents)-1)
            houses[i].residents[res].sick = SICK
            houses[i].residents[res].sickDays = 1
            houses[i].residents[res].infectionSource = INFECTION_SOURCE['unknown_source']
            
        return MAP, houses, Super([1,len(SUPER)-2,len(SUPER[0])-2]) , Synagogue([len(SUPER[0])+1,len(SYNAGOGUE)-1,len(MAP[0])-1])
    
    
    
    def countSources(self,shape):
        sources = np.zeros(shape=shape)
        for h in HOUSES:
            for r in h.residents:
                sources[r.infectionSource]+=1
        return sources
    
    def updateMap(self,houses):
        MAP, SUPER, SYNAGOGUE = self.creatBaseMap(houses)
        stats = np.zeros(shape=5)
        for h in HOUSES:
            for r in h.residents:
                MAP[r.currLoc['x']][r.currLoc['y']]=r.sick
                stats[r.sick-IMMUNED]+=1
        return MAP , stats
                
  
    def loadParams(self,path,index=0):
        data = pd.read_csv(path)
        if index==len(data):
            return None
        paramDict = {}
        paramDict['initial_sicks'] = data['initial_sicks'][index]
        paramDict['num_of_houses']  = data['num_of_houses'][index]
        paramDict['step_period']  = data['step_period'][index]          
        paramDict['day_period']  = data['day_period'][index]   
        paramDict['working_hours']  = data['working_hours'][index]        
        paramDict['infection_prob']  = data['infection_prob'][index]        
        paramDict['super_period'] = data['super_period'][index]
        paramDict['synagogue_open'] = data['synagogue_open'][index]
        paramDict['space'] = data['space'][index]
        paramDict['prey_time'] = data['prey_time'][index]
        paramDict['allowed_age'] = [float(data['allowed_age'][index].split(',')[j]) for j in range(2)]
        return paramDict
     


if __name__ == '__main__':
    # Constants
    EMPTY = 0
    WALL = 10
    IMMUNED = 1
    HEALTHY = 2
    INFECTED = 3
    SICK = 4
    DEAD = 5
    COLORS = {EMPTY:(255, 255, 255),SICK:(255, 0, 0),HEALTHY:(0, 255, 0),
              INFECTED:(255,255,0),WALL:(0, 0, 0),DEAD:(100,100,100),IMMUNED:(0,0,255)}
    INFECTION_SOURCE = {'unknown_source' :0 , 'super_source':1, 
                        'home_source':2,'synagogue_source':3,'healthy':4}
    
    corona = Corona()
    #corona.countSources(5)
    
    quarantineStage = 0 # index of param file
    CITIES = ['general','bnei_brak','tel_aviv','jerusalem']
    params = {}
    for c in CITIES[:1]: # delete '[:1] when finished
        params[c] = corona.loadParams(c+'.csv',quarantineStage)
    
    '''temp'''
    #createCSV('',CITIES[0]) # create example CSV
    CITY = CITIES[0] # set CITY to be 'general'
    
    
    
    '''Parameters'''
    # static params
    INITIAL_SICKS = params[CITY]['initial_sicks'] # quantity of sick at initialization
    NUM_OF_HOUSES = params[CITY]['num_of_houses'] # square root of number of houses in simulation
    
    
    # changed params with each index
    SPACE = params[CITY]['space']
    STEP_PERIOD = params[CITY]['step_period'] #milliseconds
    DAY_PERIOD = params[CITY]['day_period']
    WORKING_HOURS = params[CITY]['working_hours']
    INFECTION_PROB = params[CITY]['infection_prob'] #propobility of infection used in 'infection' function
    SUPER_PERIODS = params[CITY]['super_period'] # number of periods people can go to the super
    ALLOWD_AGE = params[CITY]['allowed_age'] 

    
    # calculated params
    SUPER_STEPS = int(DAY_PERIOD/STEP_PERIOD)
    HOUR = DAY_PERIOD/WORKING_HOURS #milliseconds
    STEP_MINUTES = HOUR/STEP_PERIOD #  minutes in each step
    SUPER_TIMES = int(DAY_PERIOD/SUPER_PERIODS) # length of period visiting the super 
    
    PRAY_TIME = int(DAY_PERIOD/(params[CITY]['prey_time']*STEP_PERIOD))
    SYNAGOGUE_OPEN = bool(params[CITY]['synagogue_open'])
    
    

    
    # Events to progress the simulation
    WEEK_EVENT = pygame.USEREVENT + 5
    PREY_EVENT = pygame.USEREVENT + 4
    SUPEREVENT = pygame.USEREVENT + 3
    DAYEVENT   = pygame.USEREVENT + 2
    STEPEVENT  = pygame.USEREVENT + 1
    
    pygame.time.set_timer(WEEK_EVENT, 7*DAY_PERIOD)
    pygame.time.set_timer(PREY_EVENT, DAY_PERIOD)
    pygame.time.set_timer(SUPEREVENT, SUPER_TIMES)
    pygame.time.set_timer(STEPEVENT, STEP_PERIOD)
    pygame.time.set_timer(DAYEVENT, DAY_PERIOD)
    
    # This sets the WIDTH and HEIGHT of each cell
    WIDTH = HEIGHT = 10
    PLOT_HEIGHT = 0
    PLOT_WIDTH = 20
    
    
    # margin between cells
    MARGIN = 1
    
    pygame.init()
    
    
    MAP,HOUSES,SUPER ,SYNAGOGUE = corona.creatMap(NUM_OF_HOUSES,INITIAL_SICKS,CITY)
    WINDOW_SIZE = [(WIDTH+1+PLOT_WIDTH) * (len(MAP[0])+MARGIN)  , (HEIGHT+1+PLOT_HEIGHT) * (len(MAP)+MARGIN)]
    # WINDOW_SIZE = [(WIDTH+1) * (len(MAP[0])+MARGIN)  , (HEIGHT+1) * (len(MAP)+MARGIN)]
    
    screen = pygame.display.set_mode(WINDOW_SIZE)
     
    pygame.display.set_caption("Corona Simulation")
    done = False
    clock = pygame.time.Clock()
    
    DAILY_STATS = np.zeros(shape=6)
    MAP, DAILY_STATS[:-1] = corona.updateMap(NUM_OF_HOUSES)
    #countSources(len(INFECTION_SOURCE))
       
    # MAIN
    data = pd.DataFrame(columns=['immuned','healthy','infected','sick','dead'])

    PEOPLE_COUNT = np.sum(DAILY_STATS[:-1])
    
    progress = [[DAILY_STATS[i]] for i in range(len(DAILY_STATS)-1) ]
        
    quarantineStage = 1
    superPeriod = 0  
    
    
    # ----------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  # If user clicked close
                done = True
            
            elif event.type == WEEK_EVENT:
                print("WEEK"+str(quarantineStage))
                for c in CITIES[:1]: # delete '[:1] when finished
                    params[c] = corona.loadParams(c+'.csv',quarantineStage)
                if params[CITIES[0]] == None:
                    done = True
                    break
                
                
    
                quarantineStage+=1
                
                '''temp'''
                #createCSV('',CITIES[0]) # create example CSV
                CITY = CITIES[0] # set CITY to be 'general'
                # changed params with each index
                SPACE = params[CITY]['space']
                STEP_PERIOD = params[CITY]['step_period'] #milliseconds
                DAY_PERIOD = params[CITY]['day_period']
                WORKING_HOURS = params[CITY]['working_hours']
                INFECTION_PROB = params[CITY]['infection_prob'] #propobility of infection used in 'infection' function
                SUPER_PERIODS = params[CITY]['super_period'] # number of periods people can go to the super
                
                
                # calculated params
                SUPER_STEPS = int(DAY_PERIOD/STEP_PERIOD)
                HOUR = DAY_PERIOD/WORKING_HOURS #milliseconds
                STEP_MINUTES = HOUR/STEP_PERIOD #  minutes in each step
                SUPER_TIMES = int(DAY_PERIOD/SUPER_PERIODS) # length of period visiting the super 
                
                
                PRAY_TIME = int(DAY_PERIOD/(params[CITY]['prey_time']*STEP_PERIOD))
                SYNAGOGUE_OPEN = bool(params[CITY]['synagogue_open'])
                
                pygame.time.set_timer(WEEK_EVENT, 7*DAY_PERIOD)
                pygame.time.set_timer(PREY_EVENT, DAY_PERIOD)
                pygame.time.set_timer(SUPEREVENT, SUPER_TIMES)
                pygame.time.set_timer(STEPEVENT, STEP_PERIOD)
                pygame.time.set_timer(DAYEVENT, DAY_PERIOD)
                
            elif event.type == DAYEVENT:
                
                data, DAILY_STATS, progress = corona.updateData(data,DAILY_STATS,progress)

                # Plot
                # dist_plot('glow_lines', progress, PEOPLE_COUNT, data)
                dist_all_plots(progress, PEOPLE_COUNT)

                plotImg = pygame.image.load('fig.png')
                screen.blit(plotImg, (WIDTH * (len(MAP)+1),0))
                pygame.display.update()

                if SYNAGOGUE_OPEN:
                    for h in HOUSES:
                        h.updateSick()
                        h.goPrey()
            
                pygame.time.wait(STEPEVENT) # for clearer days separation
                
            elif event.type == SUPEREVENT:
                superPeriod = (superPeriod+1)%SUPER_PERIODS
                for h in HOUSES:
                    if h.superPeriod==superPeriod:
                        h.updateSick()
                        h.eatFood(superPeriod)
            elif event.type == STEPEVENT:
                SUPER.nextStep()
                SYNAGOGUE.nextStep()
    
                    
            MAP, DAILY_STATS[:-1] = corona.updateMap(NUM_OF_HOUSES)
     
        
        # # Plot
        # dist_plot('glow_lines', progress, PEOPLE_COUNT, data)
        # dist_all_plots(progress, PEOPLE_COUNT)
        #
        # plotImg = pygame.image.load('fig.png')
        # screen.blit(plotImg, (WIDTH * (len(MAP)+1),0))
        # pygame.display.update()


        # Draw MAP
        for row in range(len(MAP)):
            for column in range(len(MAP[0])):
                color = COLORS[MAP[row][column]]
               
                pygame.draw.rect(screen,
                                  color,
                                  [(MARGIN + WIDTH) * column + MARGIN,
                                  (MARGIN + HEIGHT) * row + MARGIN,
                                  WIDTH,
                                  HEIGHT])
     
        clock.tick(30)
        pygame.display.flip()

     
    
    pygame.quit()
    
    data.to_csv('out.csv')



# c = [np.random.randint(1,6) for i in range(500)]

# neg = plt.imread('map.jpg',1)
# plt.imshow(neg)

# SCATTER_RANGE = 5
# BNEI_BRAK = (370,300)

# x = [random.normalvariate(BNEI_BRAK[0],SCATTER_RANGE) for i in range(500)]
# y = [random.normalvariate(BNEI_BRAK[1],SCATTER_RANGE) for i in range(500)]
# plt.scatter(x,y,s=1,c=c)


# JERUSALEM = (410,340)

# x = [random.normalvariate(JERUSALEM[0],SCATTER_RANGE) for i in range(500)]
# y = [random.normalvariate(JERUSALEM[1],SCATTER_RANGE) for i in range(500)]
# plt.scatter(x,y,s=1,c=c)

# plt.show()


# plt.imshow(neg)


# heatmap, xedges, yedges = np.histogram2d(x, y, bins=50)
# extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

# plt.clf()
# plt.imshow(heatmap.T, extent=extent, origin='lower')
# plt.show()




