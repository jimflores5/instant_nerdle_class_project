import math
import random
import copy

def evaluate_equation(equa_str):
    parts = equa_str.split(' ')
    for index in range(len(parts)):
        if parts[index].isdigit():
            parts[index] = int(parts[index])
    
    while len(parts) > 3:
        if parts[1] == '*':
            parts[0:3] = [parts[0] * parts[2]]
        elif parts[1] == '/':
            parts[0:3] = [parts[0] / parts[2]]
        elif parts[1] == '+':
            parts[0:3] = [parts[0] + parts[2]]
        elif parts[1] == '-':
            parts[0:3] = [parts[0] - parts[2]]

    return parts[0] == parts[2]

def parse_raw_data(entry):
    ops = []
    nums = []
    for char in entry:
        if char in '+-*/=':
            ops.append(char)
        else:
            nums.append(int(char))

    nums.sort()
    ops = sort_ops(ops)
    return ops.copy(), nums.copy()

def sort_ops(operations):
    ops_order = []
    if '*' in operations:
        ops_order.append('*')
    if '/' in operations:
        ops_order.append('/')
    if '+' in operations:
        ops_order.append('+')
    if '-' in operations:
        ops_order.append('-')
    ops_order.append('=')

    return ops_order.copy()
    
def build_equation(template, digits):
    # No operator can go in position 1 or 8 (index 0 or 7).
    # The '=' sign must be to the right of all other operators.
    # 2 operators cannot be next to each other in the string.
    # The operators list is already sorted into the proper order.
    # For 3 operators (counting '='), acceptable postions include
    # (2, 4, 6), (2, 4, 7), (2, 5, 7), (3, 5, 7).
    # Index values (1, 3, 5), (1, 3, 6), (1, 4, 6), (2, 4, 6).
    # For 2 operators, acceptable positions include
    # (2, 6), (3, 6), (4, 6), (4, 7), (2, 5), (3, 5).
    # Index values (1, 5), (2, 5), (3, 5), (3, 6), (1, 4), (2, 4).
    equation = ''
    for char in template:
        if char == 'X':
            equation += str(digits[0])
            digits.pop(0)
        else:
            equation += char
    
    for char in equation:
        if char in '+-*/=':
            equation = equation.replace(char, ' ' + char + ' ')
    return equation

def place_ops(formats, ops, known):
    for format in formats:
        equation = ''
        op_index = 0
        for index in range(8):
            if index == known[0]:
                equation += known[1]
            elif index in format:
                equation += ops[op_index]
                op_index += 1
            else:
                equation += 'X'
        formats[format] = equation
    return formats.copy()

def build_op_dict(ops, known):
    formats_3_ops = [(1, 3, 5), (1, 3, 6), (1, 4, 6), (2, 4, 6)]
    formats_2_ops = [(1, 5), (2, 5), (3, 5), (3, 6), (1, 4), (2, 4)]
    op_options = {}
    if known[1] not in '+-*/=':
        nix_this_position = known[0]
    else:
        nix_this_position = 0
    if len(ops) == 2:
        for option in formats_2_ops:
            if nix_this_position not in option:
                op_options[option] = ''
    else:
        for option in formats_3_ops:
            if nix_this_position not in option:
                op_options[option] = ''
    return op_options.copy()

def make_digit_orders(digits, known):
    orders = []
    for digit in digits:
        if str(digit) == known[1]:
            digits.remove(digit)
    num_digits = len(digits)
    num_permutations = math.factorial(num_digits)
    while len(orders) < num_permutations:
        temp_list = digits.copy()
        random.shuffle(temp_list)
        if temp_list not in orders:
            orders.append(temp_list.copy())
    orders.sort()
    return copy.deepcopy(orders)

def main():
    raw_str = '13+/958='
    correct_ans = '18 / 9 + 3 = 5'
    known_spot = (0, '1')
    other_str = '=5+89/34'
    other_ans = '45 / 9 + 3 = 8'
    other_known = (1, '5')

    operations, digits = parse_raw_data(other_str)
    options = build_op_dict(operations, other_known)
    equations = place_ops(options.copy(), operations.copy(), other_known)
    orders = make_digit_orders(digits, other_known)
    solution = ''
    for equation in equations.values():
        for order in orders:
            temp = build_equation(equation, order.copy())
            if evaluate_equation(temp):
                solution = temp
    print(f"{other_str} ---> {solution}")
    print('---')
    operations, digits = parse_raw_data(raw_str)
    options = build_op_dict(operations, known_spot)
    equations = place_ops(options.copy(), operations.copy(), known_spot)
    orders = make_digit_orders(digits, known_spot)
    for equation in equations.values():
        for order in orders:
            temp = build_equation(equation, order.copy())
            if evaluate_equation(temp):
                solution = temp
    print(f"{raw_str} ---> {solution}")

if __name__ == '__main__':
    main()