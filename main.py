from flask import Flask, render_template, request, redirect

import math
import random
import copy

app = Flask(__name__)
app.config['DEBUG'] = True

def evaluate_equation(equa_str):
    parts = equa_str.split(' ')
    for index in range(len(parts)):
        if parts[index].isdigit():
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
        elif parts[op_index] == '/':
            parts[op_index-1:op_index+2] = [parts[op_index-1] / parts[op_index+1]]
        elif parts[op_index] == '+':
            parts[op_index-1:op_index+2] = [parts[op_index-1] + parts[op_index+1]]
        elif parts[op_index] == '-':
            parts[op_index-1:op_index+2] = [parts[op_index-1] - parts[op_index+1]]
    return parts[0] == parts[2]

def parse_raw_data(entry):
    ops = []
    nums = []
    for char in entry:
        if char in '+-*/=':
            ops.append(char)
        else:
            nums.append(int(char))
    ops.sort()
    nums.sort()
    return ops.copy(), nums.copy()
    
def build_equation(template, digits):
    # No operator can go in position 1 or 8 (index 0 or 7).
    # The '=' sign must be to the right of all other operators.
    # 2 operators cannot be next to each other in the string.
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
            if index == known[0] and known[1].isdigit():
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

def check_options(equations, orders):
    soln = ''
    for equation in equations.values():
        for order in orders:
            temp = build_equation(equation, order.copy())
            if evaluate_equation(temp):
                soln = temp
    return soln

def validate_entry(position, entries):
    message = ''
    if position < 0 or position > 7:
        message = 'Click the radio button under the one known position.'
        return message

    if '=' not in entries:
        message = "You must include an '=' sign."
    elif '+' not in entries and '-' not in entries and '*' not in entries and '/' not in entries:
        message = "You must include at least one operation (+, -, *, /)."
    else:
        for entry in entries:
            if not entry.isdigit() and entry not in '+-*/=':
                message = f"{entry} is not a valid character. Enter only 0 - 9 and '+ - * / =' ."

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
        message = validate_entry(correct_char, boxes)
        if message == '':
            raw_str = ''.join(boxes)
            known_spot = (correct_char, raw_str[correct_char])

            operations, digits = parse_raw_data(raw_str)
            options = build_op_dict(operations, known_spot)
            equations = place_ops(options.copy(), operations.copy(), known_spot)
            orders = make_digit_orders(digits, known_spot)
            solution = check_options(equations, orders)
            if solution == '':
                operations[0], operations[1] = operations[1], operations[0]
                equations = place_ops(options.copy(), operations.copy(), known_spot)
                solution = check_options(equations, orders)
        
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