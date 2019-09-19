import numpy as np
import random

def get_input():
    row = list(map(int, input().split()))
    n = len(row)
    D = np.zeros((n, n))
    D[0] += row
    for i in range(1, n):
        D[i] += list(map(int, input().split()))
    return n, D

def get_next_node(current, nodes, posibilities):
    posib_list = []
    acc = 0

    # Считает границы вероятностей перехода в узлы
    # Пример: posib_list = [0.1, 0.4, 0.8, 1.0]
    # Первый узел - от 0 до 0.1, второй - от 0.1 до 0.4, и т.д. 
    for node in nodes:
        acc += posibilities[current, node]
        posib_list.append(acc)
    posib_list = np.array(posib_list)
    posib_list = posib_list / acc

    # Возврат случайного узла с использованием вероятностей
    # Пример: при r = 0.76 и posib_list = [0.1, 0.4, 0.8, 1.0]
    # вернет значение узла nodes[2] (т.к. 0.4 < 0.76 <= 0.8)
    r = random.random()
    for i in range(len(nodes)):
        if r <= posib_list[i]:
            return nodes[i]


def get_desirabilities(n, D):
    """Возвращает матрицу N размером n x n.

    Каждый элемент матрицы N[i, j] равен 1 / D[i, j]
    """
    N = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if D[i, j] != 0:
                N[i, j] = 1 / D[i, j]
            else:
                N[i, j] = 0
    return N

def update_pheromone_changes(nodes, Q, L, changes_list):
    """Добавляет в список changes_list матрицу с изменениями феромона.

    Args:
        nodes: список узлов в порядке посещения
        Q: постоянный параметр
        L: длина пути
    """
    n = len(nodes)
    changes = np.zeros((n, n))

    for i in range(n-1):
        changes[nodes[i], nodes[i+1]] = Q / L
    changes[nodes[-1], nodes[0]] = Q / L
    changes_list.append(changes)

def update_pheromone_values(pheromone, changes_list, P):
    """Обновляет матрицу со значениями феромона.

    Args:
        pheromone: матрица со значениями феромона
        changes_list: список, содержащий матрицы изменений феромона
        P: скорость выветривания феромона
        
    Returns:
        Матрица с новыми значениями феромона
    """
    pheromone = pheromone * (1 - P)
    for new_pher in changes_list:
        pheromone += new_pher
    return pheromone

def get_posibilities(PH, N, A, B):
    return (PH**A)*(N**B)

def get_path_length(D, nodes):
    n = len(nodes)
    L = 0
    for i in range(n-1):
        L += D[nodes[i], nodes[i+1]]
    L += D[nodes[n-1],nodes[0]]
    return L

def run(n, D, Q, P, A, B):
    """Реализует алгоритм муравьиного поиска.

    Args:
        n: количество узлов
        D: матрица длин переходов между узлами
        Q: константа, влияющая на величину добавки феромона
        P: скорость ослабления феромона
        A: коэффициент влияния феромона на переходе ("стадность")
        B: коэффициент влияния длины перехода ("жадность")

    Returns:
        Длина самого короткого маршрута
    """
    N = get_desirabilities(n, D)
    ants = 2 * n
    L_min = n * np.max(D)
    epochs = 5

    for cur_node in range(n):
        PH = np.ones((n, n))
        for e in range(epochs):
            pheromone_changes = []
            for i in range(ants):
                nodes = [cur_node]
                free_nodes = [j for j in range(n)]
                free_nodes.remove(cur_node)
                posibilities = get_posibilities(PH, N, A, B)
                for j in range(n-1):
                    node = get_next_node(nodes[-1], free_nodes, posibilities)
                    free_nodes.remove(node)
                    nodes.append(node)
                assert(free_nodes == [])
                L = get_path_length(D, nodes)
                if L < L_min:
                    L_min = L
                update_pheromone_changes(nodes, Q, L, pheromone_changes)
            PH = update_pheromone_values(PH, pheromone_changes, P)
    return L_min

if __name__ == '__main__':
    n, D = get_input()
    N = get_desirabilities(n, D)
    Q = 3
    P = 0.8
    A = 0.5
    B = 1.2
    L = run(n, D, Q, P, A, B)
    print(int(L))
