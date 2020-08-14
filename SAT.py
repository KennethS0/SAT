import random
from collections import Counter

def readFile(pFileName):
    '''
        Reads a file with a specific format.
        
        pFileName: txt file in the same directory.

        Returns a list of lists with all the clauses that were given
        in the file, and the amount of variables found.
            
        File format:
            Line 1 - Number of variables.
            Line 2 - Number of clauses.
            Line 3 -> onward - Clauses
    '''
    with open(pFileName, "r") as file:
        
        lines = file.readlines()
    
        varAmount = int(lines[0])
        clauseAmount = int(lines[1])

        lines = lines[2:]
        
        variables = {}

        # Checks if the amount of clauses match.
        if (clauseAmount != len(lines)):
            raise Exception("The amount of clauses given doesn't match the amount of clauses given.")

        # Verifies the user input
        for i in range(len(lines)):
            lines[i] = lines[i].replace("\n", "")
    
            temp = lines[i].replace("-", "")        
            temp = temp.split(" ")
            
            # Loops through each variable in the clause
            for var in temp:
                variables[var] = 1

            # Raises exception if the amount of variables surpasses the amount given.
            if (len(variables) > varAmount):
                raise Exception("The amount of variables doesn't match the amount of variables given.")
                
            # Separates each variable
            lines[i] = lines[i].split(" ")

        return lines, varAmount


def generatePopulation(pSize, pVarAmount):
    '''
        Generates the population based on the size given by the user.
        
        pSize: Amount of individuals that will be created.
        pVarAmount: Amount of distinct variables present in the clauses.

        Returns a dictionary of binary numbers that represent the state of
        each variable as a key, its value will represent its fitness.
    '''   

    # A dictionary used to avoid duplicates
    population = {}

    for i in range(pSize):
        individual = generateGenes(pVarAmount)
        population[individual] = 0

    return population


def generateGenes(pVarAmount):
    '''
        Generates the genes of an individual.

        Returns a string of a binary number.
    '''
    maxNum = (2 ** pVarAmount) - 1

    num = random.randint(0, maxNum)

    return str(bin(num)).replace("0b", "").zfill(pVarAmount)


def calculateFitness(pPopulation, pClauses):
    '''
        Calculates the fitness of each individual
        for this particular problem.

        Returns the dictionary with the updated fitness values.
    '''
    # Loops through each individual
    for individual in pPopulation:
        
        if pPopulation[individual] != 0:
            continue

        pPopulation[individual] = evaluateIndividual(individual, pClauses)    

    return pPopulation


def evaluateIndividual(pIndividual, pClauses):
    '''
        Evaluates the fitness of a specific individual.
    '''
    fitness = 0.0
    fitnessIncrement = 1 / len(pClauses)

    for clause in pClauses:
        
        condition = False
        
        for variable in clause:
            value = int(variable)
            
            if value > 0:
                condition = bool(int(pIndividual[value - 1]))
            
            else:
                condition = not bool(int(pIndividual[(value + 1) * -1]))

            # The clause turns out to be true
            if condition:
                fitness += fitnessIncrement
                break

    return fitness


def crossOver(pPopulation):
    '''
        Crosses the best two genes and adds them to the population.
    '''

    if (len(pPopulation) == 1): 
        return pPopulation

    selection = [wheelSelection(pPopulation), wheelSelection(pPopulation)]
    crossoverPoint = random.randint(1, len(selection[0])) - 1

    newGene = ""
    newGene += selection[0][:crossoverPoint]
    newGene += selection[1][crossoverPoint:]

    if newGene not in pPopulation:
        pPopulation[newGene] = 0

    return pPopulation


def wheelSelection(pPopulation):
    '''
        Makes a weighted random selection.
    '''
    maxVal = sum(pPopulation.values())
    randomPick = random.uniform(0, maxVal)
    current = 0
    for key, value in pPopulation.items():
        current += value
        if current > randomPick:
            return key


def mutate(pPopulation, pProbability):
    '''
        Mutates genes and adds them to the population.
    '''
    tempPopulation = {}

    for gen in pPopulation:
        newGene = ''

        for char in gen:
            if random.randint(1,100) <= pProbability:
                if not int(char):
                    newGene += "1" 

                else:
                    newGene += "0"

            else:
                newGene += char

        if newGene not in pPopulation and len(newGene) != 0:
            tempPopulation[newGene] = 0

    return {**pPopulation, **tempPopulation}


def logInput(pPopulationSize, pGenAmount, pMutationRatio):
    '''
        Writes the user input into the results file.
    '''
    message = " --- USER INPUT --- \n"
    message += "Initial population size: " + str(pPopulationSize) + "\n"
    message += "Amount of generations: " + str(pGenAmount) + "\n"
    message += "Mutation ratio: " + str(pMutationRatio) + "%\n"

    with open("Results.txt", "w") as file:
        file.write(message)


def logGeneration(pPopulation, pGen):
    '''
    Logs the information of each generation
    '''
    message = "\n--- GENERATION " + str(pGen) + " ---\n"
    message += "AMOUNT OF GENES: " + str(len(pPopulation)) + "\n\n"

    for individual in Counter(pPopulation).most_common():
        message += "GENE: " + individual[0] + " FITNESS: " + str(individual[1]) + "\n"

    with open("Results.txt", "a") as file:
        file.write(message)


if __name__ == '__main__':
    file = input("Type the name of the file: \n")
    clauses, varAmount = readFile(file)

    populationSize = int(input("Type the size of the population: \n"))
    generations = int(input("Type the amount of generations: \n"))
    mutationRatio = int(input("Type the mutation ratio (Between 0 and 100): \n"))

    logInput(populationSize, generations, mutationRatio)

    population = generatePopulation(populationSize, varAmount)

    for i in range(generations):
        population = calculateFitness(population, clauses)
        logGeneration(population, i)
        population = mutate(crossOver(population), mutationRatio)