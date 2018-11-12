#!/usr/bin/env python3

from sys import stdin, stdout, stderr
from random import choice
from os import system


# def save_maze(data):
#     system("echo \"%s\" >> map.txt"%(data))


def update_maze():
    global start, Target, searched_road, output, pers, ephs
    maze.clear()
    while True:
        row = stdin.readline()
        if row == '\n':
            break
        maze.append(row[:-1])
    pers.clear()
    ephs.clear()
    for x, row in enumerate(maze):
        for y, value in enumerate(row):
            if value == letter:  # index of my IA in map
                start = (x, y)
            elif value == 'o':
                pers.append((x, y))
            elif value == '!':
                ephs.append((x, y))
    # Target = target(maze, start, ephs, pers)
    # searched_road = Astar_search(maze, start, Target)
    # output = move(maze, searched_road)
    # print('\n'.join(output))


def val(maze, x, y):  # could be '!', 'o', ' ', '#', None
    if x < 0 or x >= len(maze) or y < 0 or y >= len(maze[0]):
        return None
    return maze[x][y]


def check_valids(maze, index):
    valid_moves = []  # a list of nodes
    x = index[0]
    y = index[1]
    box = [(x-1, y), (x, y+1), (x+1, y), (x, y-1)]
    vals = [val(maze, x-1, y), val(maze, x, y+1),
            val(maze, x+1, y), val(maze, x, y-1)]
    for i in range(4):
        if vals[i] in ['!', 'o', ' ']:
            valid_moves.append(box[i])
    return valid_moves


def heuristic(start, goal):
    return abs(goal[0] - start[0]) + abs(goal[1] - start[1])


def target(maze, index, ephs, pers):
    if ephs != []:
        min = len(Astar_search(maze, index, ephs[0]))
        tar = ephs[0]
        for e in ephs:
            f = len(Astar_search(maze, index, e))
            if f < min:
                min = f
                tar = e
        return tar
    else:
        min = len(Astar_search(maze, index, pers[0]))
        tar = pers[0]
        for e in pers:
            f = len(Astar_search(maze, index, e))
            if f < min:
                min = f
                tar = e
        return tar


def Astar_search(maze, start, target):
    info = {}  # info[node] = [parent, g, h, f]
    info[start] = [None, 0, 0, 0]
    open_list = [start]
    closed_list = []

    # loop until find out target
    while len(open_list) > 0:

        # get the current node
        cur = open_list[0]  # current node
        cur_index = 0
        for index, item in enumerate(open_list):
            if info[item][3] < info[cur][3]:
                cur = item
                cur_index = index

        # pop current off open list, add to closed list
        open_list.pop(cur_index)
        closed_list.append(cur)

        # found the target
        if cur == target:
            road = [cur]
            c = cur
            while info[c][0] is not None:
                road.append(info[c][0])
                c = info[c][0]
            road.reverse()
            return road

        # valids
        valids = check_valids(maze, cur)
        for v in valids:
            if v in closed_list:
                continue

            # set the g, h, f values:
            par = cur
            g = info[cur][1] + 1
            h = heuristic(v, target)
            f = g + h
            if v in open_list and info[v][1] <= g:
                continue
            info[v] = [par, g, h, f]
            if v not in open_list:
                open_list.append(v)


def move(maze, searched):
    moves = ["MOVE UP\n", "MOVE RIGHT\n", "MOVE DOWN\n", "MOVE LEFT\n"]
    result = []
    for i in range(len(searched) - 1):
        s = searched[i]
        t = searched[i + 1]
        xx = t[0] - s[0]
        yy = t[1] - s[1]
        if xx > 0:
            result.append(moves[2])
        if xx < 0:
            result.append(moves[0])
        if yy > 0:
            result.append(moves[1])
        if yy < 0:
            result.append(moves[3])
    return result


input()  # VM: "HELLO\n"
input()  # VM: "\n"
print("I AM MAX\n")
letter = input()  # VM: "YOU ARE <letter>\n"
input()  # VM: "\n"
print("OK\n")
letter = letter[-1]  # get the <letter> from "YOU ARE <letter>"

maze = []
pers = []  # list of permanent resources
ephs = []  # list of ephemeral resources
line = stdin.readline()
while line != '':
    if line == 'MAZE\n':
        update_maze()
        Target = target(maze, start, ephs, pers)
        searched_road = Astar_search(maze, start, Target)
        output = move(maze, searched_road)
        # print('\n'.join(output))
        print(output[0])

    line = stdin.readline()
