import json
import argparse
from timeit import default_timer as timer
import time

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
        return '{}:\t|{}|'.format(str(self.factorList), str(self.getLength()))


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
            if sorted(f.factorList) == sorted(factorization.factorList):
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
        else:
            return 0

    def is_atom(self):
        return bool(len(self.factorizations) < 1)

    def set_mod_value(self, τ):
        self.modValue = self.name % τ

    def get_mod_value(self):
        return self.modValue

    def inspect(self):
        # out_string = "==========================\n"

        out_string = "{} ≡ {} (mod {})\t".format(str(self.name), str(self.modValue), tau)
        out_string += "ε: {:<4}\n\n".format("NAF" if self.is_atom() else self.get_elasticity())

        if not self.is_atom():
            # out_string += "==========================\n"
            out_string += "Longest Factorization:" + str(self.maxFactor.factorList) + "\n"
            out_string += "Shortest Factorization:" + str(self.minFactor.factorList) + "\n\n"
            # out_string += "==========================\n"
            out_string += "Factorizations:\n"

            for f in self.factorizations:
                out_string += str(f)
                if f != self.factorizations[-1]:
                    out_string += '\n'

        return out_string


    def __str__(self):
        return str(self.name) + ": ε = {}".format(str(self.get_elasticity()))

def get_elastics():
    return [n.name for n in numberList if n.get_elasticity() > 1.0]


def get_user_values():
    tau = int(input("Enter the τ-divisor: "))
    maxN = int(input("Enter the upper limit: "))
    return tau, maxN


def get_empty_number_list(tau, maxNum):
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

# Returns all possible representations of the number provided...
# If the number is an atom, this will be num and λ*num, where λ = 1 or -1
# Otherwise, it returns all factorizations of num.
def get_representations_of(num: int, n, tau):
    # If it's an atom, return atom * +/- unit:
    if numberList[num].is_atom():
        return [[num],[-1*num]]
    # Otherwise, return all factorizations:
    else:
        returnVal = []
        for fz in numberList[num].factorizations:
            returnVal.append(fz.factorList)
        return returnVal


# Return the value of a number or congruent list (mod tau):
def get_tau_val(item, tau):
    if type(item) == int:
        return item % tau
    else:
        return item[0] % tau

# For all divisors of num up to sqrt(num), creates a factorizations
# comprising each possible representation of the divisor, d (if d is an atom:
# d, -d; otherwise it's all atomic factorizations of d) and each representation
# of the quotient, in all possible combinations.
# Each congruent factorization is added to the list to be returned; the
# rest are discarded.
def factorize(divisors, num, tau):
    factorizations = []
    non_atomic_fz = []
    for divisor in divisors:
        quotient = int(num / divisor)
        for divisor_rep in get_representations_of(divisor, num, tau):
            for quotient_rep in get_representations_of(quotient, num, tau):
                if is_congruent(divisor_rep, quotient_rep):
                    factorizations.append(divisor_rep + quotient_rep)
    return factorizations


def is_congruent(lhs, rhs):
    return get_tau_val(lhs, tau) == get_tau_val(rhs, tau)


# Factors a single number, adding its factorization to the number list.
def factor(number):
    # Get the simple list of factors:
    divisors = get_divisors(number)

    if len(divisors) > 0:
        # Generate completed factorizations for each factor in the list, if possible,
        # and add to the list of completed factorizations:
        num_factorization_list = factorize(divisors, number, tau)

    # If there are any successful factorizations, add them to the Number object:
        if len(num_factorization_list) > 0:
            for factorization in num_factorization_list:
                numberList[number].add_factorization(Factorization(factorization))


# Runs the program for numbers in range(2:maxNum)
def do_batch_factor(tau, maxNum):
    start = timer()
    # For each number in the range:
    for number in range(2, maxNum):
        factor(number)
    end = timer()
    print("Time elapsed: {}".format(end-start))
    write_to_file(build_json())


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
    eList = []
    for n in numberList:
        eList.append(n.get_elasticity())
        # print("{:>5}: e = {}".format(n.name, n.get_elasticity()))
    print(eList)


def display_menu():
    print("\nτ-factorization Toolkit:")
    print("========================")
    print("         MENU           ")
    print("========================")
    print("{:>4} Begin new job.".format('(1)'))
    print("{:>4} Show list of factorizations.".format('(2)'))
    print("{:>4} Show k_max.".format('(3)'))
    print("{:>4} Show ε > 1.0.".format('(4)'))
    print("{:>4} Show all ε.".format('(5)'))
    print("{:>4} Show max ε.".format('(6)'))
    print("{:>4} JSONify.".format('(7)'))
    print("{:>4} Write to file.".format('(w)'))
    print("{:>4} Read from file.".format('(r)'))
    print("{:>4} Inspect a number in detail.".format('(i)'))
    print("{:>4} Quit.".format('(q)'))

    print("\n (XXX indicates a feature that is not functioning properly.)")
    print("\n>", end='')

# tau, maxNum = get_user_values()
# maxNum = maxNum + 1     # To make ranges inclusive
#
 # numberList = get_empty_number_list(maxNum, tau)
# do_batch_factor(tau, maxNum)


#Let users access REPL
def build_json():
    json_rep = []
    for n in numberList:
        thisNumber = {}
        thisNumber['name'] = n.name
        longest = []
        shortest = []
        factz = []
        if len(n.factorizations) > 0:
            for fz in n.factorizations:
                length = len(fz.factorList)
                if length > len(longest):
                    longest = fz.factorList
                if len(shortest) == 0 or len(fz.factorList) < len(shortest):
                    shortest = fz.factorList
                factz.append(fz.factorList)
        if len(factz) > 0:
            thisNumber['factz'] = factz
            thisNumber['longest'] = longest
            thisNumber['shortest'] = shortest
            thisNumber['elasticity'] = len(longest) / len(shortest)
        json_rep.append(thisNumber)
    # print(json_rep)
    return json_rep


# print("Entering Python Read-Eval-Print Loop (Type 'quit' when done.)")

def write_to_file(str):
    if args.filename == "-1":
        filename = "tau{}-max{}".format(tau,maxNum)
        filename += time.strftime("%b%d%H%M", time.localtime())
    else:
        filename = args.filename
    f = open(filename, 'w')
    json.dump(str, f);
    print("JSON written to {:<} .".format(filename))
    f.close()

def read_from_file():
    filename = input("Please enter file name:")
    with open(filename, 'r') as f:
        from_file = json.load(f)
        numberList = []
        for item in from_file:
            name = item['name']
            numberList.append(Number(name))
            if 'factz' in item:
                for f in item['factz']:
                    numberList[name].add_factorization(Factorization(f))
        print(json.dumps(from_file, sort_keys = False, indent = 2))
        return numberList
#
# parser = argparse.ArgumentParser()
# parser.add_argument("-t", dest="tau", default="6", type=int)
# parser.add_argument("-m", dest="maxNum", default="1000", type=int)
# parser.add_argument("-f", dest="filename", default="-1")
# args = parser.parse_args()
# print("tau: {}, max: {}".format(args.tau, args.maxNum))
# display_menu()
# tau = args.tau
# maxNum = args.maxNum + 1
numberList = get_empty_number_list(tau, maxNum)
do_batch_factor(tau, maxNum)
userChoice = input()

while userChoice != 'q' and userChoice != 'Q':

    # Do new job
    if userChoice == '1':
        del numberList
        tau, maxNum = get_user_values()
        maxNum += 1
        numberList = get_empty_number_list(maxNum, tau)
        do_batch_factor(tau, maxNum)
    # Show results
    elif userChoice == '2':
        show_results()
    # Show only ε > 1.0
    elif userChoice == '3':
        owner, k_max = get_longest_factorization()
        print("{} has k_max of {}".format(owner, k_max))
    # Show ε
    elif userChoice == '4':
        for n in get_elastics():
            print('ε({}) = {}'.format(n, numberList[n].get_elasticity()))
    elif userChoice == '5':
        show_elasticities()
    # Show max ε
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

    # JSONify
    elif userChoice == '7':
        print(json.dumps(build_json(), sort_keys = True, indent=4))

    # Inspect
    elif userChoice == 'i':
        whichNum = input("Which number would you like to inspect? ")
        print('\n')
        print(numberList[int(whichNum)].inspect())
    elif userChoice == 'w':
        write_to_file(build_json())
    elif userChoice == 'r':
        numberList = read_from_file()

    display_menu()
    userChoice = input()
