def digits_to_numbers(eq):
    labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')', '+', '-', '/', 'x']
    eq_full = []

    i = 0
    while i < len(eq):
        tmp = ''
        while i < len(eq) and eq[i] < 10:
            tmp += labels[eq[i]]
            i += 1

        if tmp:
            eq_full.append(int(tmp))

        if i < len(eq):
            eq_full.append(labels[eq[i]])
        i += 1

    return eq_full


def priority(op):
    if op in ['x', '/']:
        return 2
    
    if op in ['+', '-']:
        return 1 
    
    return 0


def apply_op(b, a, op):
    if op == '+': return a + b
    if op == '-': return a - b
    if op == 'x': return a * b
    if op == '/': return a / b


def evaluate(eq):
    eq = digits_to_numbers(eq)
    streq = ''

    for i in eq:
        streq += str(i)
    streq += "="

    values = []
    ops = []

    i = 0
    while i < len(eq):
        if eq[i] == '(':
            ops.append(eq[i])

        elif isinstance(eq[i], int):
            values.append(eq[i])

        elif eq[i] == ')':
            while len(ops) > 0 and ops[-1] != '(':
                values.append(apply_op(values.pop(), values.pop(), ops.pop()))
            ops.pop()

        # operator.
        else:
            while len(ops) > 0 and priority(ops[-1]) >= priority(eq[i]):
                if len(values) < 2:
                    return "invalid expression"

                values.append(apply_op(values.pop(), values.pop(), ops.pop()))

            ops.append(eq[i])

        i += 1

    while len(ops) != 0:
        values.append(apply_op(values.pop(), values.pop(), ops.pop()))

    return streq + str(values[0])



