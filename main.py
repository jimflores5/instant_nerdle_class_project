from flask import Flask, render_template, request, redirect

import math
import random
import copy

app = Flask(__name__)
app.config['DEBUG'] = True

def evaluate_equation(equa_str):
    # See comments in the console-app branch.
    parts = equa_str.split(' ')
    for index in range(len(parts)):
        if parts[index].isdigit() and parts[index] != str(int(parts[index])):
            return False
        elif parts[index].isdigit():
            parts[index] = int(parts[index])

    while len(parts) > 3:
        if '*' in parts:
            op_index = parts.index('*')
        elif '/' in parts:
            op_index = parts.index('/')
        else:
            op_index = 1

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

    return parts[0] == parts[2]

def parse_raw_data(entry):
    # See comments in the console-app branch.
    ops = []
    nums = []
    for char in entry:
        if char in '+-*/=':
            ops.append(char)
        else:
            nums.append(char)
    ops.sort()
    nums.sort()
    return ops.copy(), nums.copy()
    
def build_equation(template, digits):
    # See comments in the console-app branch.
    equation = ''
    for char in template:
        if char == 'X':
            equation += str(digits[0])
            digits.pop(0)
        elif char in '+-*/=':
            equation += ' ' + char + ' '
        else:
            equation += char
    
    return equation

def place_ops(op_positions, ops, known):
    # See comments in the console-app branch.
    if known[1] in ops:
        ops.remove(known[1])  

    for entry in op_positions:
        template = ''
        op_index = 0

        for index in range(8):
            if index == known[0]:
                template += known[1]
            elif index in entry:
                template += ops[op_index]
                op_index += 1
            else:
                template += 'X'
        op_positions[entry] = template
    return op_positions.copy()

def build_op_dict(ops, known):
    # See comments in the console-app branch.
    positions_3_ops = [(1, 3, 5), (1, 3, 6), (1, 4, 6), (2, 4, 6)]
    positions_2_ops = [(1, 5), (2, 5), (3, 5), (3, 6), (1, 4), (2, 4)]
    op_options = {}

    if known[1] not in '+-*/=':
        nix_position = True
        include_position = False
    else:
        nix_position = False
        include_position = True
        
    if len(ops) == 2:
        for option in positions_2_ops:
            if include_position and known[0] in option:
                op_options[option] = ''
            elif nix_position and known[0] not in option:
                op_options[option] = ''
    else:
        for option in positions_3_ops:
            if include_position and known[0] in option:
                op_options[option] = ''
            elif nix_position and known[0] not in option:
                op_options[option] = ''
    return op_options.copy()

def make_digit_orders(digits, known):
    # See comments in the console-app branch.
    orders = []

    if known[1].isdigit() and known[1] in digits:
        digits.remove(known[1])

    num_digits = len(digits)
    num_repeats = count_repeats(digits)
    num_permutations = math.factorial(num_digits) // math.factorial(1 + num_repeats) # This reduces to line 196 when num_repeats = 0.

    while len(orders) < num_permutations:
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

def check_templates(templates, orders):
    # See comments in the console-app branch.
    soln = ''
    for template in templates.values():
        for order in orders:
            equation = build_equation(template, order.copy())

            if evaluate_equation(equation):
                soln = equation
    return soln

def validate_entry(position, entries):
    # This function performs some basic input validation, but there are
    # still holes that could crash the program.
    # Encourage your students to do a better job!
    message = ''
    if position < 0 or position > 7:
        message = 'Click the radio button under the known, correct character.'
        return message

    if len(entries) != 8:
        message = "Enter exactly 8 characters."
    elif entries.count('=') != 1:
        message = "Include exactly one '=' sign."
    elif '+' not in entries and '-' not in entries and '*' not in entries and '/' not in entries:
        message = "You must include at least one operation (+, -, *, /)."
    else:
        for entry in entries:
            if not entry.isdigit() and entry not in '+-*/=':
                message = f"{entry} is not a valid entry. Use only 0 - 9 and '+ - * / =' ."

    return message

@app.route('/', methods = ['GET', 'POST'])
def main():
    boxes = []
    if request.method == 'POST':
        if request.form['submit'].lower() != 'new_data':
            return redirect('/')
        checked = correct_char = int(request.form['known'])
        for index in range(8):
            boxes.append(request.form[f"box_{index}"])
        raw_str = ''.join(boxes)
        message = validate_entry(correct_char, raw_str)
        if message == '':
            known_spot = (correct_char, raw_str[correct_char])

            operations, digits = parse_raw_data(raw_str)
            op_placements = build_op_dict(operations, known_spot)
            templates = place_ops(op_placements.copy(), operations.copy(), known_spot)
            dig_orders = make_digit_orders(digits.copy(), known_spot)
            solution = check_templates(templates, dig_orders)
            if solution == '':
                operations[0], operations[1] = operations[1], operations[0]
                templates = place_ops(op_placements.copy(), operations.copy(), known_spot)
                solution = check_templates(templates, dig_orders)
        
            message = f"{raw_str} ---> {solution}"
            success = True
        else:
            success = False
        
    else:
        message = "Enter today's Instant Nerdle puzzle. Use only the digits 0 - 9 and the operators '+', '-', '*', '/' and '='."
        for index in range(8):
            boxes.append('')
        success = False
        checked = 0
    
    return render_template('index.html', boxes = boxes, message = message,
        success = success, checked = checked)

if __name__ == '__main__':
    app.run()