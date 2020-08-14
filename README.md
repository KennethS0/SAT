# SAT
SAT Problem solved by using a genetic algorithm for the Analysis of Algorithms course.

This implementation of SAT takes each clause as a collection of OR's.

## Usage
The program takes as input a file that must be formatted in a specific way.

Each variable must be a number from 1 to (Amount of variables), to represent a NOT
simply put the same number but as a negative.

**Format**
- First Line: Amount of variables
- Second Line: Amount of clauses
- Next Lines: Clauses (Each variable must be separated by a space)


###Example
5<br />
4<br />
1 3 4<br />
-5 -2<br />
1 2<br />
-3<br />
**This translates to:**
  - 5 Variables (A, B, C, D, E)
  - 4 Clauses
  - A or C or D
  - (not E) or (not B)
  - A or B
  - not C
