from constraint import Problem, AllDifferentConstraint, InSetConstraint


def parse_sodoku(file_name: str):
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


def print_sodoku(sodoku: list[int]):
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


def constrain_sodoku_start(problem: Problem, sodoku: list[int]):
    for i in range(81):
        if sodoku[i] != 0:
            problem.addConstraint(lambda x, y=sodoku[i]: x == y, [i])


def constrain_diagonal(problem: Problem):
    problem.addConstraint(AllDifferentConstraint(), [i * 9 + i for i in range(9)])
    problem.addConstraint(AllDifferentConstraint(), [i * 9 + 8 - i for i in range(9)])


def constrain_odd_even(problem: Problem):
    clues = [[20, 19, 11], [42, 25, 15], [56, 55, 65], [60, 61, 69]]

    for clue in clues:
        if clue[0] % 2 == 0:
            problem.addConstraint(InSetConstraint([2, 4, 6, 8]), clue[1:])
        else:
            problem.addConstraint(InSetConstraint([1, 3, 5, 7, 9]), clue[1:])


def solve_problem(problem: Problem):
    """Solve a sodoku problem."""
    solution = problem.getSolution()
    if solution is None:
        print("No solution found")
    else:
        print("Solution:")
        print_sodoku(solution)


def main(filename: str):
    sodoku_start = parse_sodoku(filename)
    print_sodoku(sodoku_start)
    sodoku_problem = build_sodoku_problem()
    constrain_sodoku_start(sodoku_problem, sodoku_start)
    constrain_odd_even(sodoku_problem)
    solve_problem(sodoku_problem)


if __name__ == '__main__':
    main('test_data/even_odd.txt')
