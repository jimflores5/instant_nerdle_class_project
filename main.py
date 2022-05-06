def evaluate_equation(equa_str):
    parts = equa_str.split(' ')
    for index in range(len(parts)):
        if parts[index].isdigit():
            parts[index] = int(parts[index])
    
    while len(parts) > 3:
        if parts[1] == '*':
            parts[0:3] = [parts[0] * parts[2]]
        elif parts[1] == '/':
            parts[0:3] = [parts[0] // parts[2]]
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
    
def build_equation(operators, digits):
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

    pass

def main():
    raw_str = '13+/958='
    correct_ans = '18 / 9 + 3 = 5'
    known_spot = (0, '1')
    other_str = '=5+89/34'
    other_ans = '45 / 9 + 3 = 8'
    other_known = (1, '5')
    
    operations, digits = parse_raw_data(raw_str)
    print(operations, digits)

if __name__ == '__main__':
    main()