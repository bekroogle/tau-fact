import math
from collections_extended import bag


class Factorization:
    def __init__(self, factorList):
        self.factorList = factorList

    def getTauValue(self):
        remainder = self.factorList[0] % tau
        return remainder

    def getLength(self):
        return len(self.factorList)

    def __str__(self):
        return '{}: |{}|'.format(str(self.factorList), str(self.getLength()))


# Number object contains a list of all the τ-factorizations for that number.
# method isAtom():bool returns True if number has no τ-factorizations.
# method getModValue(τ) returns the number's value (mod τ).
class Number:
    def __init__(self, name):
        self.name = name
        self.factorizations = []
        self.k_max = 0
        self.k_min = 0
        self.maxFactor = Factorization([])
        self.minFactor = Factorization([])

    def addFactorization(self, factorization):
        for f in self.factorizations:
            if bag(f.factorList) == bag(factorization.factorList):
                return

        # Update the maxFactor if the new factorization is longer than previous max.
        if factorization.getLength() > self.maxFactor.getLength():
            self.maxFactor = factorization

        # Update the minFactor if the new factorization is shorter than previous min.
        if self.minFactor.getLength() == 0 or factorization.getLength() < self.minFactor.getLength():
            self.minFactor = factorization

            # Add the new factorization to the list of factorizations.
        self.factorizations.append(factorization)

    # identifies the longest factorization and returns its length.
    # WARNING: This mutates the attribute: self.maxFactor!
    def calculateKmax(self):
        return self.maxFactor.getLength()
    # identifies the shortest factorization and returns its length.
    # WARNING: This mutates the attribute: self.minFactor!
    def calculateKmin(self):
        return self.minFactor.getLength()

    def getElasticity(self):
        if self.isAtom() == False:
            return self.calculateKmax() / self.calculateKmin()

    def isAtom(self):
        return bool(len(self.factorizations) < 1)

    def setModValue(self, τ):
        self.modValue = self.name % τ

    def getModValue(self):
        return self.modValue

    def __str__(self):
        outString = "{:>5} ".format(str(self.name) + ':')
        outString += ' τ{:<2}= {:<5}'.format(tau, str(self.modValue))

        hasFactorsIndicatorString = "Atom" if self.isAtom() else "===>"
        outString += '{:>5}  '.format(hasFactorsIndicatorString)

        if self.isAtom() == False:
            for f in self.factorizations:
                outString += str(f)
                if f != self.factorizations[-1]:
                    outString += ', '

        return outString


def getUserValues():
    tau = int(input("Enter the τ-divisor: "))
    maxN = int(input("Enter the upper limit: "))
    return tau, maxN


def getEmptyNumberList(maxNum, tau):
    nList = []

    for i in range(0, maxNum):
        nList.append(Number(i))
        nList[i].setModValue(tau)

    return nList


# Returns a list of all values up to sqrt(num) that divide num evenly.
def getFactors(num):
    factors = []
    for i in range(2, math.floor(num ** 0.5) + 1):
        if num % i == 0:
            factors.append(i)
    return factors


def subFactor(factor, length):
    # if factor is an atom, return it,
    # otherwise, return a list of its decomposition:
    if numberList[factor].isAtom():
        return [factor]
    else:
        if length == "short":
            return numberList[factor].minFactor.factorList
        elif length == "long":
            return numberList[factor].maxFactor.factorList

# Given the list of all of a numbers factors up to sqrt(num), finds
# the complement to each factor. If the factor ≡ complement (mod τ-number),
# the pair are counted as a factorization, otherwise, no factorization is
# added to the list of factorizations.
def factorize(factors, num, tau):
    factorizations = []
    currentFactorization = []
    lengths = ["short", "long"]
    for factor in factors:
        rem = factor % tau
        comp = int(num / factor)

        for l in lengths:
            lhs = subFactor(factor, l)
            rhs = subFactor(comp, l)

            if isCongruent(lhs + rhs):
                factorizations.append(lhs + rhs)

    return factorizations


def isCongruent(numbers):
    remainder = numbers[0] % tau
    for number in numbers:
        if number % tau != remainder:
            return False
    return True


# Runs the program for numbers in range(2:maxNum)
def doCount(tau, maxNum):
    # For each number in the range:
    for number in range(2, maxNum):

        # Add a representative Number object to the master list:

        # Reset the current list of factors:doCount(tau, maxNum)
        ourFactors = []

        # Reset the list of factorizations:
        ourFactorizations = []

        # Get the simple list of factors:
        ourFactors = getFactors(number)

        # Generate completed factorizations for each factor in the list, if possible,
        # and add to the list of completed factorizations:
        ourFactorizations = factorize(ourFactors, number, tau)

        # If there are any successful factorizations, add them to the Number object:
        if len(ourFactorizations) > 0:
            for f in ourFactorizations:
                numberList[number].addFactorization(Factorization(f))


                # Print the results to the screen:


def showResults():
    for n in numberList:
        print(n)


def getKmax():
    k_max = 0
    owner = 0
    for n in numberList:
        for f in n.factorizations:
            if f.getLength() > k_max:
                k_max = f.getLength()
                owner = n.name
    return owner, k_max


def getKmin():
    owner, k_min = getKmax()
    for n in numberList:
        for f in n.factorizations:
            if f.getLength() < k_min:
                k_min = f.getLength()
                owner = n.name
    return owner, k_min


def showElasticities():
    for n in numberList:
        print("{:>5}: e = {}".format(n.name, n.getElasticity()))


def displayMenu():
    print("\nτ-factorization Toolkit:")
    print("========================")
    print("         MENU           ")
    print("========================")
    # print("{:>4} XXXXX BROKEN XXXXX".format('(1)'))
    print("{:>4} Begin new job.".format('XXX'))
    print("{:>4} Show resulting list of factorizations.".format('(2)'))
    print("{:>4} Show k_max".format('(3)'))
    print("{:>4} Show k_min".format('XXX'))
    print("{:>4} Show elasticities".format('(5)'))
    print("{:>4} Show max elacsticity".format('(6)'))
    print("{:>4} Quit".format('(q)'))

    print("\n (XXX indicates a feature that is not functioning properly.)")
    print("\n>", end='')


def doNewJob():
    tau, maxNum = getUserValues()
    numberList = getEmptyNumberList(maxNum, tau)
    doCount(tau, maxNum)
    return numberList


tau, maxNum = getUserValues()
numberList = getEmptyNumberList(maxNum, tau)
doCount(tau, maxNum)

displayMenu()

userChoice = input()
while userChoice != 'q' and userChoice != 'Q':
    if userChoice == '1':
        doNewJob()
    elif userChoice == '2':
        showResults()
    elif userChoice == '3':
        owner, k_max = getKmax()
        print("{} has k_max of {}".format(owner, k_max))
    elif userChoice == '4':
        ower, k_min = getKmin()
        print("{} has k_min of {}".format(owner, k_min))
    elif userChoice == '5':
        showElasticities()
    elif userChoice == '6':
        owner = 0
        maxE = 0
        for n in numberList:
            nElast = n.getElasticity()
            if type(nElast) == float:
                if nElast > maxE:
                    maxE = nElast
                    owner = n.name

        print("{} has e = {}".format(str(owner), maxE))
    displayMenu()
    userChoice = input()