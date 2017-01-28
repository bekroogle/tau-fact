import math
from collections_extended import bag


# a Factorization object contains:
#   a list of factors: factorList[], where factorList[m] ≡ factorList[n] (mod  τ),
#   a function returning the value of the first factor (mod  τ).
#   a function returning the length of the factor list.
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
# method isAtom(): bool returns True if number has no τ-factorizations.
# method get_mod_value(τ): int returns the number's value (mod τ).
class Number:
    def __init__(self, name):
        self.name = name
        self.factorizations = []
        self.k_max = 0
        self.k_min = 0
        self.maxFactor = Factorization([])
        self.minFactor = Factorization([])

    def add_factorization(self, factorization):
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
    def get_longest_fact(self):
        return self.maxFactor.getLength()
    # identifies the shortest factorization and returns its length.
    # WARNING: This mutates the attribute: self.minFactor!
    def get_shortest_fact(self):
        return self.minFactor.getLength()

    def get_elasticity(self):
        if not self.is_atom():
            return self.get_longest_fact() / self.get_shortest_fact()

    def is_atom(self):
        return bool(len(self.factorizations) < 1)

    def set_mod_value(self, τ):
        self.modValue = self.name % τ

    def get_mod_value(self):
        return self.modValue

    def __str__(self):
        outString = "{:>5} ".format(str(self.name) + ':')
        outString += ' τ{:<2}= {:<5}'.format(tau, str(self.modValue))

        hasFactorsIndicatorString = "Atom" if self.is_atom() else "===>"
        outString += '{:>5}  '.format(hasFactorsIndicatorString)

        if self.is_atom() == False:
            for f in self.factorizations:
                outString += str(f)
                if f != self.factorizations[-1]:
                    outString += ', '

        return outString


def get_user_values():
    tau = int(input("Enter the τ-divisor: "))
    maxN = int(input("Enter the upper limit: "))
    return tau, maxN


def get_empty_number_list(maxNum, tau):
    nList = []

    for i in range(0, maxNum):
        nList.append(Number(i))
        nList[i].set_mod_value(tau)

    return nList


# Returns a list of all values up to sqrt(num) that divide num evenly.
def get_divisors(num):
    divisors = []
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            divisors.append(i)
    return divisors


# Given the list of all of a numbers factors up to sqrt(num), finds
# the complement to each factor. If the factor ≡ complement (mod τ-number),
# the pair are counted as a factorization, otherwise, no factorization is
# added to the list of factorizations.
def factorize(divisors, num, tau):
    factorizations = []
    for divisor in divisors:
        rem = divisor % tau
        alt_rem = (-1 * divisor) % tau
        comp = int(num / divisor)

        if numberList[comp].is_atom():
            if comp % tau == rem:
                factorizations.append([divisor] + [comp])
            if (-1 * comp) % tau == rem:
                factorizations.append([divisor] + [-1 * comp])
            if comp % tau == alt_rem:
                factorizations.append([-1 * divisor] + [comp])
            if (-1 * comp) % tau == alt_rem:
                factorizations.append([-1 * divisor] + [-1 * comp])
        else:
            fzs = numberList[comp].factorizations

            for fz in fzs:
                if fz.getTauValue() == rem:
                    factorizations.append([divisor] + fz.factorList)
                if fz.getTauValue() == alt_rem:
                    factorizations.append([-1*divisor] + fz.factorList)
    return factorizations



def is_congruent(numbers):
    remainder = numbers[0] % tau
    for number in numbers:
        if number % tau != remainder:
            return False
    return True


# Factors a single number, adding its factorization to the number list.
def factor(number):
    # Get the simple list of factors:
    divisors = get_divisors(number)

    if len(divisors) > 0:
        # Generate completed factorizations for each factor in the list, if possible,
        # and add to the list of completed factorizations:
        factorizationList = factorize(divisors, number, tau)

    # If there are any successful factorizations, add them to the Number object:
        if len(factorizationList) > 0:
            for factorization in factorizationList:
                numberList[number].add_factorization(Factorization(factorization))


# Runs the program for numbers in range(2:maxNum)
def do_batch_factor(tau, maxNum):
    # For each number in the range:
    for number in range(2, maxNum):
        factor(number)


def show_results():
    for n in numberList:
        print(n)


def get_longest_factorization():
    k_max = 0
    owner = 0
    for n in numberList:
        for f in n.factorizations:
            if f.getLength() > k_max:
                k_max = f.getLength()
                owner = n.name
    return owner, k_max


def get_shortest_factorization():
    owner, k_min = get_longest_factorization()
    for n in numberList:
        for f in n.factorizations:
            if f.getLength() < k_min:
                k_min = f.getLength()
                owner = n.name
    return owner, k_min


def show_elasticities():
    for n in numberList:
        print("{:>5}: e = {}".format(n.name, n.get_elasticity()))


def display_menu():
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
    print("{:>4} Enter REPL".format('(7)'))
    print("{:>4} Quit".format('(q)'))

    print("\n (XXX indicates a feature that is not functioning properly.)")
    print("\n>", end='')


def do_new_job():
    tau, maxNum = get_user_values()
    numberList = get_empty_number_list(maxNum, tau)
    do_batch_factor(tau, maxNum)
    return numberList

tau, maxNum = get_user_values()
maxNum = maxNum + 1     # To make ranges inclusive

numberList = get_empty_number_list(maxNum, tau)
do_batch_factor(tau, maxNum)

display_menu()

#Let users access REPL
def repl():
    print("Entering Python Read-Eval-Print Loop (Type 'quit' when done.)")
    while True:
        command = input("#>")
        if command == 'quit': break
        eval(command)

userChoice = input()
while userChoice != 'q' and userChoice != 'Q':
    if userChoice == '1':
        do_new_job()
    elif userChoice == '2':
        show_results()
    elif userChoice == '3':
        owner, k_max = get_longest_factorization()
        print("{} has k_max of {}".format(owner, k_max))
    elif userChoice == '4':
        ower, k_min = get_shortest_factorization()
        print("{} has k_min of {}".format(owner, k_min))
    elif userChoice == '5':
        show_elasticities()
    elif userChoice == '6':
        owner = 0
        maxE = 0
        for n in numberList:
            nElast = n.get_elasticity()
            if type(nElast) == float:
                if nElast > maxE:
                    maxE = nElast
                    owner = n.name

        print("{} has e = {}".format(str(owner), maxE))
    elif userChoice == '7':
        repl()
    display_menu()
    userChoice = input()