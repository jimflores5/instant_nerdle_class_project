import math
import random
import copy

def evaluate_equation(equa_str): # This function accepts a string equation and solves it.
    # Split the equation into a list. Each element is either a number or an operator.
    parts = equa_str.split(' ')
    
    # The last entry in the list represents the answer to the equation.
    # We need to see if the equation produces this answer!

    # Iterate through the list and convert string numbers to integers.
    # Return False for any string like '031'.
    for index in range(len(parts)):
        if parts[index].isdigit() and parts[index] != str(int(parts[index])):
            return False
        elif parts[index].isdigit():
            parts[index] = int(parts[index])

    # Solve the equation by following the order of operations.
    while len(parts) > 3: # The final 3-item list contains two values and the '=' sign, like [value_1, '=', value_2].
        # Check for the * and / operators.
        # If present, solve those operations first.
        if '*' in parts:
            # Return the index for the operator.
            op_index = parts.index('*')
        elif '/' in parts:
            op_index = parts.index('/')
        else:
            # If no * or /, then either + or - will be at index 1.
            op_index = 1

        # Combine the numbers on either side of the operator, then use
        # a slice to replace the 3 elements with the resulting value.
        if parts[op_index] == '*':
            parts[op_index-1:op_index+2] = [parts[op_index-1] * parts[op_index+1]]
        elif parts[op_index] == '/' and parts[op_index+1] != 0:
            parts[op_index-1:op_index+2] = [parts[op_index-1] / parts[op_index+1]]
        elif parts[op_index] == '+':
            parts[op_index-1:op_index+2] = [parts[op_index-1] + parts[op_index+1]]
        elif parts[op_index] == '-':
            parts[op_index-1:op_index+2] = [parts[op_index-1] - parts[op_index+1]]
        else:
            return False
    
    # Compare the result of the equation with the suggested answer and 
    # return True or False.
    return parts[0] == parts[2]

def parse_raw_data(entry):
    # This function takes the 8 characters from the puzzle input and separates
    # them into a list of the operators (+-*/=) and a list of single digits.
    ops = []
    nums = []
    for char in entry:
        if char in '+-*/=':
            ops.append(char)
        else:
            nums.append(char)
    ops.sort()  # .sort() places '=' after '+-*/'. (NICE!)
    nums.sort() # There's no need to sort the digits, but I like to put them in order anyway.
    return ops.copy(), nums.copy()
    
def build_equation(template, digits):
    # 'template' has a form similar to 'X+XX/X=X', where each X holds the
    # position for a digit. The template may also contain a known digit.
    # The positions and symbols for the operators will vary, but '=' is
    # always the last operator.
    equation = ''
    for char in template:
        if char == 'X':
            # Replace each 'X' with one of the digits in the puzzle.
            equation += str(digits[0])
            digits.pop(0)
        elif char in '+-*/=':
            # The equation will later be split into a list. To make this
            # easier, add a space on either side of the operators.
            equation += ' ' + char + ' '
        else:
            # Keep any digits and operators already present in the template.
            equation += char
    
    return equation

def place_ops(op_positions, ops, known):
    # This function assigns string values to each key in the 'op_positions'
    # ('op_placements') dictionary.
    # Each string is a template for an equation.
    # Different templates have the operators at different positions
    # within the string.
    for entry in op_positions:
        # 'entry' is a collection of operator positions, like (2, 4, 6).
        template = ''
        op_index = 0

        # If the correct postion for an operator is already known, remove
        # that operator from the ops list.
        if known[1] in ops:
            ops.remove(known[1])    

        # Each equation consists of 8 characters.
        for index in range(8):
            if index == known[0]:
                # Add the known character to the string.
                template += known[1]
            elif index in entry:
                # If the current position is in the collection, add the
                # next operator in the ops list to the string.
                template += ops[op_index]
                op_index += 1
            else:
                # Otherwise, add X as a placeholder in the equation.
                template += 'X'
        # Assign the new template to the relevant key in the dictionary.
        op_positions[entry] = template
    return op_positions.copy()

def build_op_dict(ops, known):
    # This function identifies the possible operator positions and assigns
    # them as keys in a dictionary.
    # The 8 positions in the Nerdle equation have index values 0 - 7.
    # No operator can go in positions 0 or 7.
    # The '=' sign must be to the right of all other operators.
    # 2 operators cannot be next to each other.
    # For 3 operators (counting '='), possible index combinations include
    # (1, 3, 5), (1, 3, 6), (1, 4, 6), and (2, 4, 6).
    # For 2 operators, acceptable positions include index values of
    # (1, 5), (2, 5), (3, 5), (3, 6), (1, 4), and (2, 4).
    positions_3_ops = [(1, 3, 5), (1, 3, 6), (1, 4, 6), (2, 4, 6)]
    positions_2_ops = [(1, 5), (2, 5), (3, 5), (3, 6), (1, 4), (2, 4)]
    op_options = {}

    if known[1] not in '+-*/=':
        # If the known charater is a digit, then its position may
        # remove one or more of the possible operator placements.
        nix_position = True
        include_position = False
    else:
        # If the known charater is an operator, then its position
        # mandates specific index combinations.
        nix_position = False
        include_position = True
        
    if len(ops) == 2:
        # Build a dictionary using the entries of positions_2_ops as keys.
        # The boolean values for nix_position and incldue_position limit
        # which position combinations we need to consider.
        for option in positions_2_ops:
            if include_position and known[0] in option:
                # Select only combinations that include the known index value.
                # Assign the empty string to each key.
                op_options[option] = ''
            elif nix_position and known[0] not in option:
                # Select combinations that do NOT include the known index value.
                op_options[option] = ''
    else:
        # Build a dictionary using the entries of positions_3_ops as keys.
        for option in positions_3_ops:
            if include_position and known[0] in option:
                op_options[option] = ''
            elif nix_position and known[0] not in option:
                op_options[option] = ''
    return op_options.copy()

def make_digit_orders(digits, known):
    # Logic and reasoning can be used to identify the correct placement
    # for some or all of the digits (e.g. x / y must be an integer).
    # OR...
    # We can just brute-force the solution by trying all possible
    # combinations of digits in each tempate.
    # The number of possibilities is small enough that we don't need to
    # worry about bogging the program down.

    # 'orders' will be a list of lists. Each element represents one
    # left-to-right arrangement of the puzzle digits.
    orders = []

    # If the known postion holds a number, remove that value from
    # the digits list.
    if known[1].isdigit() and int(known[1]) in digits:
        digits.remove(known[1])
    
    # Next, we need to know how many different ways there are to arrange
    # the digits in the puzzle. 4 digits can be arranged 24 different ways.
    # 5 digtis = 120 different ways, and 6 digits gives 720.
    # BUT that assumes all the digits are different.
    # So, let's check for repeated digits.

    num_digits = len(digits)
    num_repeats = count_repeats(digits)

    # This if/else statement is overkill. Line 201 works by itself.
    # However, breaking up the math explanation into smaller pieces may
    # help your students.
    if num_repeats == 0:
        num_permutations = math.factorial(num_digits)  # 5! = 120, etc.
    else:
        # Each repeated digit reduces the number of possible configurations.
        # The reduction factor is another factorial! (Math folks, there's 
        # probably a better way. Any tips?)
        num_permutations = math.factorial(num_digits) // math.factorial(1 + num_repeats) # This reduces to line 196 when num_repeats = 0.

    while len(orders) < num_permutations:
        # Eventually, repeated random shuffles generate all possible
        # permutations.
        # I'm not happy with this approach, but it was quick to code.
        temp_list = digits.copy()
        random.shuffle(temp_list)
        if temp_list not in orders:
            orders.append(temp_list.copy())
    orders.sort()
    return copy.deepcopy(orders)

def count_repeats(dig_list):
    # The 'set()' function creates a collection of unique entries,
    # which can be used to quickly determine the number of repeated
    # numbers in dig_list.
    return len(dig_list) - len(set(dig_list))
    # Since set() is not discussed in the LCHS curriculum, here's an
    # alternative that accomplishes the same thing:
    # temp = []
    # for digit in dig_list:
    #   if digit not in temp:
    #       temp.append(digit)
    # return len(dig_list) - len(temp) 

def query_user():
    # This function collects the puzzle characters and the one correct
    # character from the user.
    num_errors = 8
    while num_errors > 0:
        # Collect the 8 characters for the puzzle.
        raw_data = input("Enter Instant Nerdle characters: ")

        # Some basic input validation follows, but there are holes.
        # Encourage your students to do a better job!
        if len(raw_data) != 8:
            print("You must enter 8 characters.")
        elif raw_data.count('=') != 1:
            print("You must include exactly one '=' sign.")
        elif '+' not in raw_data and '-' not in raw_data and '*' not in raw_data and '/' not in raw_data:
            print("You must include at least one operator (+, -, *, /).")
        else:
            for char in raw_data:
                if not char.isdigit() and char not in '+-*/=':
                    print(f"{char} is not a valid character.")
                    print("Enter only 0 - 9 and '+ - * / ='.")
                else:
                    num_errors -= 1
    
    valid_char = False
    while not valid_char:
        # Collect the character known to be in the correct position.
        known_char = input("Which character is in the correct spot? ")
        if known_char in raw_data:
            valid_char = True
        else:
            print(f"{known_char} isn't in {raw_data}")
    return raw_data, known_char

def check_templates(templates, orders):
    # This function puts digits into the prepared templates and evaluates
    # the resulting equations.
    soln = ''
    for template in templates.values():
        # 'template' is a string with operators but no numbers.
        for order in orders:
            # Call 'build_equation' to fill in the digits from 'order'.
            equation = build_equation(template, order.copy())

            # Evaluate the equation and store it if correct.
            if evaluate_equation(equation):
                soln = equation
    return soln

def main():
    # Prompt the user to enter the Nerdle puzzle and to identify the correctly placed character.
    raw_str, correct_char = query_user()
    # For example: '9=47+/21'
    # correct_char = '7'

    # Assign the index and identity of the correctly placed character.
    known_spot = (raw_str.index(correct_char), correct_char)

    # Extract the operators and digits from the Nerdle puzzle input.
    operations, digits = parse_raw_data(raw_str)

    # Identify the possible arrangements for the operators.
    op_placements = build_op_dict(operations, known_spot)

    # Construct templates for the possible equations.
    templates = place_ops(op_placements.copy(), operations.copy(), known_spot)

    # Identify the possible left-to-right arrangements of the digits in the puzzle.
    dig_orders = make_digit_orders(digits.copy(), known_spot)

    # Place the digits into each template, then evaluate the equations.
    solution = check_templates(templates, dig_orders)

    # When the equation has 2 operators besides '=', one is arbitrarily
    # placed first. If this arrangement doesn't generate a solution,
    # flip the 2 operators and try again.
    if solution == '':
        operations[0], operations[1] = operations[1], operations[0]
        templates = place_ops(op_placements.copy(), operations.copy(), known_spot)
        solution = check_templates(templates, dig_orders)
    
    # Display the original puzzle and the solution!
    print(f"{raw_str} ---> {solution}")

if __name__ == '__main__':
    main()