import cv2
import numpy as np
import time
import random

matrix = np.full((100, 100, 3), 255)
# print(matrix.show)
x_start = random.randrange(0, matrix.shape[0])
x_end = random.randrange(0, matrix.shape[0])
y_start = random.randrange(0, matrix.shape[1])
y_end = random.randrange(0, matrix.shape[1])
'''x_start=11
y_start=11

x_end=90
y_end=11'''
matrix[y_start, x_start] = (0, 0, 255)
matrix[y_end, x_end] = (0, 0, 255)

for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        prob = random.random()
        if prob >= 0.2 and prob <= 0.3:
            if (i != x_start and j != y_start) or (i != x_end and j != y_end):
                matrix[i, j] = 0

img = matrix
img = cv2.resize(img.astype(np.uint8), (400, 400), interpolation=cv2.INTER_AREA)
img_copy = img.copy()

pink = (255, 0, 255)
black = (255, 255, 255)

w, h, c = img.shape


class node():
    def __init__(self, parent, position):
        self.parent = parent
        self.position = position
        self.g = np.inf
        self.h = np.inf
        self.f = np.inf


def min_dist(open_list):
    min_dist = np.inf
    min_node = None
    for node in open_list:
        if open_list[node].f < min_dist:
            min_dist = open_list[node].f
            min_node = open_list[node]
    return min_node


def get_dist(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return (((x1 - x2) ** 2 + (y1 - y2) ** 2)) ** 0.5


def obstacle(position):
    x, y = position
    if img[y][x][0] == 0 and img[y][x][1] == 0 and img[y][x][2] == 0:
        return True
    return False


def goal(position):
    x, y = position
    if img[y][x][0] == 125 and img[y][x][1] == 125 and img[y][x][2] == 125:
        return True
    return False


def show_path(node):
    print('show path')
    current_node = node
    path = []
    path.append(current_node.position)
    current_node = current_node.parent
    while current_node.parent is not None:
        path.append(current_node.position)
        img_copy[current_node.position[1]][current_node.position[0]] = (0, 255, 0)
        current_node = current_node.parent
    path.reverse()
    #    for i in range(len(path)-1):
    #        cv2.line(img_copy.astype(np.uint8), path[i], path[i+1], (0, 255, 0), 5)
    cv2.namedWindow('final path', cv2.WINDOW_NORMAL)
    cv2.imshow("final path", img_copy.astype(np.uint8))
    cv2.imwrite("final_path.png", img_copy)
    if cv2.waitKey(1) == 'q':
        cv2.destroyAllWindows()
        return


def dijstra(start, end):
    print('astar called')
    open_list = {}
    closed_list = []
    start_node = node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    open_list[start] = start_node
    while len(open_list) > 0:
        # print("dict size = ", len(open_list))
        current_node = min_dist(open_list)
        img[current_node.position[1]][current_node.position[0]] = (255, 0, 0)
        open_list.pop(current_node.position)

        if current_node.position == end:
            print("Goal Reached")
            show_path(current_node)
            return

        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            if node_position[0] > (w - 1) or node_position[0] < 0 or node_position[1] > (h - 1) or node_position[1] < 0:
                continue
            if node_position in closed_list:
                continue
            if obstacle(node_position):
                continue

            img[node_position[1]][node_position[0]] = pink
            new_node = node(current_node, node_position)

            new_node.g = current_node.g + get_dist(current_node.position, new_node.position)
            new_node.h = get_dist(new_node.position, end)
            new_node.f = new_node.g + new_node.h

            if new_node.position in open_list:
                if new_node.g < open_list[new_node.position].g:
                    open_list[new_node.position] = new_node
            else:
                open_list[new_node.position] = new_node

        if current_node.position not in closed_list:
            closed_list.append(current_node.position)

        cv2.namedWindow('path_finding', cv2.WINDOW_NORMAL)
        cv2.imshow("path_finding", img.astype(np.uint8))
        cv2.waitKey(1)


if __name__ == '__main__':
    start = (x_start * 4, y_start * 4)
    end = (x_end * 4, y_end * 4)

    begin_ = time.time()
    dijstra(start, end)
    end = time.time()

    print("algorithm time = ", (end - begin_))

    cv2.namedWindow("path_finding", cv2.WINDOW_NORMAL)
    cv2.imshow("path_found", img.astype(np.uint8))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

