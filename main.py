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
    

def main():
    raw_str = '13+/958='
    correct_ans = '18 / 9 + 3 = 5'
    
    operations, digits = parse_raw_data(raw_str)
    print(evaluate_equation(correct_ans))

if __name__ == '__main__':
    main()