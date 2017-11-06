import random

def read_sudoku(filename):
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(values):
    """ Привести в божеский вид """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(values[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def group(values, n):
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [values[i:i+n] for i in range(0, len(values), n)]


def get_row(values, pos):
    """ Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return values[pos[0]]


def get_col(values, pos):
    """ Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    return [values[i][pos[1]] for i in range(0, len(values))]


def get_block(values, pos):
    """ Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    block = []
    block_row = (pos[0] // 3) * 3
    block_column = (pos[1] // 3) * 3
    for i in range(3):
        for j in range(3):
            block.append(values[block_row + i][block_column + j])
    return block  


def find_empty_positions(grid):
    """ Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for row in range(len(grid)):
        for col in range(len(grid)):
            if grid[row][col] == ".":
                return (row, col)
    return None


def find_possible_values(grid, pos):
    """ Вернуть множество всех возможных значений для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> set(values) == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> set(values) == {'2', '5', '9'}
    True
    """
    number = set('123456789')
    row = set(get_row(grid, pos)) 
    col = set(get_col(grid, pos))
    block = set(get_block(grid, pos))
    return number - set.union(block, row, col)
 

def solve(grid):
    """Решение пазла, заданного в grid
    Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла


    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    pos = find_empty_positions(grid) 
    if pos is None: 
        return grid
    possible_values = find_possible_values(grid, pos)
    if possible_values == []:
        return None    
    for i in possible_values: 
        grid[pos[0]][pos[1]] = str(i)
        result = solve(grid)
        if result is not None:
            return result 
    grid[pos[0]][pos[1]] = '.'


def check_solution(solution):
    """ Если решение solution верно, то вернуть True, в противном случае False """
    for i in range(9):
        for j in range(9):
            pos = (i, j)
            row = get_row(solution, pos)
            for number in row:
                if row.count(number) != 1: 
                    return False
            col = get_col(solution, pos)
            for number in col:
                if col.count(number) != 1:
                    return False
            block = get_block(solution, pos)
            for number in block:
                if block.count(number) != 1:
                    return False
    return True


def generate_sudoku(n):
    """ Генерация судоку, заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    new_sudoku = []
    for row in range(9): 
        new_sudoku.append([])
        for col in range(9):
            new_sudoku[row].append(".") 
    new_sudoku[0][0] = str(random.randrange(1, 9)) 
    new_sudoku[1][8] = str(random.randrange(1, 9))
    new_sudoku[3][4] = str(random.randrange(1, 9))
    new_sudoku[6][1] = str(random.randrange(1, 9))
    new_sudoku[1][8] = str(random.randrange(1, 9))
    solve(new_sudoku) 
    point = 9*9 - n
    while point != 0:
        row = random.randrange(1, 9) 
        col = random.randrange(1, 9)
        if new_sudoku[row][col] != ".":
            new_sudoku[row][col] = "."
            point -= 1
    return new_sudoku


if __name__ == '__main__':
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        display(solution)      

    
