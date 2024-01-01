from constraint import Problem, AllDifferentConstraint


def parse_sodoku(file_name):
    """
    Example input
    7....98..
    3.2.8.1..
    .....4...
    5......9.
    .64...38.
    .9......5
    ...2.....
    ..3.6.2.4
    ..93....8

    Example output
    [7, 0, 0, 0, 0, 9, 8, ...]
    """
    sodoku = []
    with open(file_name) as f:
        for line in f:
            line = line.strip()
            for c in line:
                if c == '.':
                    sodoku.append(0)
                else:
                    sodoku.append(int(c))
    return sodoku


def print_sodoku(sodoku):
    for i in range(9):
        for j in range(9):
            value = sodoku[i * 9 + j]
            print(value if value != 0 else ' ', end=' ')
        print()


def build_sodoku_problem():
    problem = Problem()
    problem.addVariables(range(81), range(1, 10))
    for i in range(9):
        problem.addConstraint(AllDifferentConstraint(), range(i * 9, i * 9 + 9))
        problem.addConstraint(AllDifferentConstraint(), range(i, 81, 9))

    for a in range(3):
        for b in range(3):
            problem.addConstraint(
                AllDifferentConstraint(),
                [27 * a + 9 * i + 3 * b + j for i in range(3) for j in range(3)]
            )

    return problem


def constrain_sodoku_start(problem, sodoku):
    for i in range(81):
        if sodoku[i] != 0:
            problem.addConstraint(lambda x, y=sodoku[i]: x == y, [i])


def solve_problem(problem):
    """Solve a sodoku problem."""
    solution = problem.getSolution()
    if solution is None:
        print("No solution found")
    else:
        print("Solution:")
        print_sodoku(solution)


def main(filename):
    sodoku_start = parse_sodoku(filename)
    print_sodoku(sodoku_start)
    sodoku_problem = build_sodoku_problem()
    constrain_sodoku_start(sodoku_problem, sodoku_start)
    solve_problem(sodoku_problem)


if __name__ == '__main__':
    main('test.txt')
