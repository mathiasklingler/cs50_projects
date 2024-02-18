import sys

from crossword import *
import random

class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }
        self.assignment = dict()

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Iterate over all Variables
        for var in self.crossword.variables:
            # print(f'variable position and length: {var.i, var.j, var.direction, var.length}')
            # Iterate over all words over all variables
            for word in self.crossword.words:
                #print(f'Domain and length of words: {word, len(word)}')
                # filter out words that does not match variable length
                if var.length != len(word):
                    # print("No match. Can be removed from Domain for Variable.")
                    self.domains[var].remove(word)
            # print(f'Variable end: {var.i, var.j, var.direction, var.length}')
            # print(f'Domain of Variable: {self.domains}')

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        #print("############# revise function #########")
        #print(f'X: {x}')
        #print(f'Y: {y}')
        
        # check changes to return true or false depending of changes are made for variable x
        check_changes = self.domains[x].copy()

        # get overlapping letters between variable if they exist
        get_overlap = self.crossword.overlaps.get((x, y))
        
        # Check if there is an overlap between x,y
        if get_overlap is not None:
            # loop over words in domain[x]
            for x_words in self.domains[x].copy():
                #print(f'x_words: {x_words}')
                # loop over words in words list
                for y_words in self.domains[y]:
                    #print(f'x,y words: {x_words, y_words}')
                    # If x != y and length x,y is higher than overlap index
                    if x_words != y_words and len(x_words) >= get_overlap[0] + 1 and len(y_words) >= get_overlap[1] + 1:
                        # if x, y have the same letter on defined position overlap
                        if x_words[get_overlap[0]] == y_words[get_overlap[1]]:
                            # print(f'x,y words match: {x_words, y_words}')
                            break
                else:
                    # If there is no match remove word vom x domain
                    #print(f'No match between x,y: {x_words}')
                    self.domains[x].remove(x_words)
                    # print(f'self.domains x: {self.domains[x]}')            

        # Check if domain has changed
        if check_changes == self.domains[x]:
            # print("No changes in the domain")
            return False
        else:
            # print("Changes in the domain")
            return True
            
    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # get all overlapping variables 
        queue_temp = self.crossword.overlaps

        # print("############## ac3 ################")
        for key, value in queue_temp:
            # Filter out items with None values
            queue = {key: value for key, value in queue_temp.items() if value is not None}
        #print("############## ac3 - all arcs in queue ################")
        #for i in queue:
         #   print(i)
        
        while queue:
            # Pull the last item from the queue list
            a, b = queue.popitem()
            x = a[0]
            y = a[1]
            #print(f'x: {x}')
            #print(f'y: {y}')
            #print("############## queue after pop ################")
            #for i in queue:
            #    print(i)
        
            # x, y are arc consistent
            if self.revise(x, y):
                #print("domain changed from X")
                # variable x must have at least one word
                if self.domains[x] == 0:
                    return False
                # find neighbors from x
                neighbours = self.crossword.neighbors(x)
                #print(f'x neighbors: {neighbours}')
                # add all neighbours Z back to the queue exept y
                for Z in neighbours:
                    if Z != y:
                        #print(f'all other neigbours without y: {Z}')
                        queue[(Z,x)] = self.crossword.overlaps.get((Z, x))
                #print("############## queue after adding Z ################")
                #print(queue)
                #for i in queue:
                #    print(i)
        
        # add results for variables to the self.assignment data object
        for var in self.crossword.variables:
            #print(f'variable: {var}')
            #print(f'words: {self.domains[var]}')
            self.assignment[var] = self.domains[var]
        #print(f'assigment dict: {self.assignment}')

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        #print("############assignment_complete function ########################")
        #for key, value in assignment.items():
        #    print(key, value)
        #print(f'nbr. variables: {len(self.crossword.variables)}')
        
        # Check if all variables are present in the assignment
        if len(assignment) == len(self.crossword.variables):
            #print("Same length")
            # Iterate over all variables in the assignments
            for key, value in assignment.items():
                #print(f'key: {key}')
                # Check if key is not None
                if key is None:
                    #print("no Solution for variable {key}")
                    return False
            else:
                #print("Every variable has at least one Solution.")
                return True
        # Not every Variable present in the assignment
        else:
            #print("There are missing variables!")
            return False
        
    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        #print("############ consistent function ########################")
        
        used_variables = []

        for var_x in assignment:
            val_x = assignment[var_x]

            # If the assigned word is already used, not consistent:
            if val_x in used_variables:
                return False
            used_variables.append(val_x)

            # Check if variable is assigned its length is correct
            if len(val_x) != var_x.length:
                return False

            # Check if there are conflicts between neighboring variables:
            for var_y in self.crossword.neighbors(var_x):
                if var_y in assignment:
                    val_y = assignment[var_y]

                    # Check if neighbor variable is assigned and satisfies constraints
                    if not self.crossword.overlaps[var_x, var_y]:
                        return True
                    else:
                        x_index, y_index = self.crossword.overlaps[var_x, var_y]
                        if val_x[x_index] == val_y[y_index]:
                            return True
                        else:
                            return False

        # Otherwise all assignments are consistent
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        #print("############ order_domain_values ########################")
        #print(f'X_1 key: {var}')
        #print(f'X_1 Values: {self.domains[var]}')
        #print(f'assignment: {assignment}')
        #print(f'X_1 neighbors: {self.crossword.neighbors(var)}')
        
        unsorted_values = {}
        
        # Iterate over values in var
        for x_value in self.domains[var]:
            # Iterate over values in neighbors
            for neighbor in self.crossword.neighbors(var):
                #print(f'neighbor: {neighbor}')
                #print(f'neighbor words: {self.domains[neighbor]}')
                # Iterate over all words over neighbor variables
                for neighbor_word in self.domains[neighbor]:
                    #print(f'neighbor word: {neighbor_word}')
                    # Check if word_x is in neighbor variable
                    if x_value == neighbor_word:
                       #print(f'word match {x_value, neighbor_word}')
                       # If word_x is in neighbor variable count 1
                       unsorted_values[x_value] = unsorted_values.get(x_value, 0) + 1
        
        # Iterate over values in varr again to include values without matches in the output
        for x_value in self.domains[var]:
            if x_value not in unsorted_values:
                unsorted_values[x_value] = 0  # Set the count to 0 for values without matches
        
        # sort variables based on the nbr of words in neighbor variables
        sorted_values = dict(sorted(unsorted_values.items(), key=lambda item: item[1]))
        #print(f'unsorted_values: {unsorted_values}')
        #print(f'sorted_values: {sorted_values}')
        #print(f'sorted_values keys: {sorted_values.keys()}')
        ordered_list = list(sorted_values.keys())
        #print(f'list: {ordered_list}')
        return ordered_list
        


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        #print("############ select unassigned variable ########################")
        
        # Gets et of unassigned variables:
        unassigned = set(self.domains.keys()) - set(assignment.keys())
        
        # Create list of variables, sorted by MRV and highest degree
        result = [var for var in unassigned]
        result.sort(key = lambda x: (len(self.domains[x]), -len(self.crossword.neighbors(x))))

        return result[0]
        """        nbr = 100
        if variables is not None:
            min_variable = None
            #for variable in self.crossword.variables:
            for key, values in variables.items():
                if key not in assignment:
                    if len(values) < nbr:
                        print(f'length and nbr: {len(values), nbr}')
                        nbr = len(values)
                        min_variable = key
                        print(f'new var with less vars: {min_variable}')
            if min_variable is not None:
                print(f'min_variable:  {min_variable}')
                return min_variable
            else:
                return None
        return None    
        """     

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        #print("########### backtrack ##############")
        
        # If all variables are assigned, return assignment:
        if self.assignment_complete(assignment):
            return assignment

        # Otherwise select an unassigned variable:
        var = self.select_unassigned_variable(assignment)
        pre_assignment_domains = self.domains.copy()
        for val in self.order_domain_values(var, assignment):
            assignment[var] = val
            if self.consistent(assignment):
                # Update variable domain to be assigned value
                self.domains[var] = {val}
                # Use ac3 to remove inconcistent values from neighbouring variables
                self.ac3([(other_var, var) for other_var in self.crossword.neighbors(var)])
                result = self.backtrack(assignment)
                if result:
                    return result
            # If assignment does not produce solution, remove assignment and reset domains
            del assignment[var]
            self.domains = pre_assignment_domains
        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
