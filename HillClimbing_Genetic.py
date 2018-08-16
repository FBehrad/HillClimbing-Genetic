from random import *
import time

#--------------------------------------------------------- H -------------------------------------------

def get_h_cost(board):
    n = len(board)
    h = 0
    for i in range( n - 1 ):  # به ازای هرکدوم از مهره ها در هر ستون بررسی میکنیم

        for j in range(i + 1, n ): # این برای ستون هایی که داریم چک میکنیم (با مهره های ستون های بعدی چک میکنیم)

            offset = j - i # اختلاف ستونی که داخلشم و ستونی که داره چک میکنه رو به دست میاره

            if board[i]!= board[j] and board[i] != board[j] - offset and board[i] != board[j] + offset:  # بررسی میکنیم که آیا ئر یک سطرن یا نه
                h += 1
    return h


#--------------------------------------------------- Make Initial State  -------------------------------


def make_initial_state (numberOfQueen) :
    InitialBoard = []
    for i in range (numberOfQueen) :
        rowValue = randint(0,numberOfQueen-1)
        InitialBoard.append(rowValue)
    return InitialBoard

#--------------------------------------------------- Make Neighbour -------------------------------------

def make_neighbour (initialboard ) :

    x = []
    for i in range (len(initialboard)) :

        if initialboard[i] == 0:
            initialboard[i] = initialboard[i] + 1
            x.append(list(initialboard))
            initialboard[i] = initialboard[i] - 1
        elif initialboard[i] == (len(initialboard)-1 ):
            initialboard[i] = initialboard[i] - 1
            x.append(list(initialboard))
            initialboard[i] = initialboard[i] + 1
        else :
            initialboard[i] = initialboard[i] - 1
            x.append(list(initialboard))
            initialboard[i] = initialboard[i] + 1
            initialboard[i] = initialboard[i] + 1
            x.append(list(initialboard))  # وقتی لیست به لیست اپند میکنی قبلش اینو باید بزنی
            initialboard[i] = initialboard[i] - 1
    return x


#--------------------------------------------------- Cross over  -------------------------------------------

def crossOver (father1 , father2 , children):
    pointOfCrossOver = 2
    temp = father1
    child1 = father1[:pointOfCrossOver] + father2[pointOfCrossOver:]
    child2 = father2[:pointOfCrossOver] + temp[pointOfCrossOver:]
    children.append(list(child1))
    children.append(list(child2))
    return children

#--------------------------------------------------- HillClimbing -------------------------------------------

def HillClimbing ():
    size = int(input("Enter the numbers of Queens : "))
    bestState = ((size - 1) * size) / 2  # در بهترین حالت فیتنس باید این بشه
    myBoard = make_initial_state(size)
    h = get_h_cost(myBoard)
    print("Initial State : %s   With h : %s " % (myBoard, h))
    for i in range(6000): #  while h!= bestState : # شرط خاتمه یامی تواند این باشد که بهترین تابع ارزیابی پیدا شود یا تعداد گامی را در نظر بگیریم
        neighbours = make_neighbour(myBoard)
        h_list = []
        for item in neighbours:
            h = get_h_cost(item)
            h_list.append(h)
        max_h = max(h_list)
        indexOfMaxH = h_list.index(max_h)
        myBoard = neighbours[indexOfMaxH]

    print("Final State : %s   With h : %s " % (neighbours[indexOfMaxH] , max_h ))

#--------------------------------------------------- GENETIC -------------------------------------------------

def Genetic ():
    size = int(input("Enter the numbers of Queens : "))
    sizeOfpopulation = 8
    population = []
    h_list = []
    h_listNormalized = []
    my_list = []


    for i in range(sizeOfpopulation):  # ایجاد جمعیت اولیه و محاسبه ی تابع ارزیابی شون
        state = make_initial_state(size)
        population.append(list(state))
        h = get_h_cost(state)
        my_list.append((state, h))
        h_list.append(h)

    def getKey(item):
        return item[1]

    SortedList = sorted(my_list, key=getKey, reverse=True)

    print("Initial Population : %s " % SortedList)

    for i in range(5000):

        children = []
        fathers = []

        numberOfFathers = round(sizeOfpopulation / 2)  # به تعداد نصف جمعیت بهترین بابا هارو انتخاب میکنیم

        for i in range(sizeOfpopulation):
            fathers.append(list(SortedList[i][0]))

        for i in range(round(numberOfFathers / 2) + 1):
            children = crossOver(fathers[i], fathers[i + 1], list(children))

     

        mutationChildren = []

        for i in range(round(len(children) / 2)):
            ChosenChild = randint(0, len(children) - 1)
         
            child = list(children[ChosenChild])
        
            pointOfMutation = randint(0, len(child) - 1)
           
            newValue = randint(0, len(child) - 1)
        
            child[pointOfMutation] = newValue
           
            mutationChildren.append(list(child))

      
        newChildren = children + mutationChildren
        allPopulation = fathers + newChildren
      

        newPopulation = []

        for item in allPopulation:
            h = get_h_cost(item)
            newPopulation.append((item, h))

        SortedList = sorted(newPopulation, key=getKey, reverse=True)
        SortedList = list(SortedList[:sizeOfpopulation])

    print("FinalPopulation : %s " % SortedList)


#--------------------------------------------------- Main ---------------------------------------------------

for i in range(100):
    Option = int(input("\nWhich algorithm do you wanna run ? \n1.HillClimbing 2.Genetic 3.Exit \n"))

    if Option == 1:
        start_time = time.clock()
        HillClimbing()
        endtime = time.clock()
        print("Time Of run  :  %s Seconds " % (endtime - start_time))
    elif Option == 2:
        start_time = time.clock()
        Genetic()
        endtime = time.clock()
        print("Time Of run  :  %s Seconds " % (endtime - start_time))
    elif Option == 3 :
        break
    else:
        print("Choose Rigth Option !!! ")
