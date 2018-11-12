#!/usr/bin/env python3

from sys import stdin, stdout, stderr
from random import choice
from os import system


def update_maze():
    global start, pers, ephs, others
    maze.clear()  # list of rows in map
    while True:
        row = stdin.readline()
        if row == '\n':
            break
        maze.append(row[:-1])
    pers.clear()  # positions of 'o'
    ephs.clear()  # positions of '!'
    for x, row in enumerate(maze):
        for y, value in enumerate(row):
            if value == letter:  # index of my IA in map
                start = (x, y)
            elif value == 'o':
                pers.append((x, y))
            elif value == '!':
                ephs.append((x, y))
            elif value not in ['#', ' ']:
                others.append((x, y))


def value(maze, x, y):  # value of position(x, y) in maze
    if x < 0 or x >= len(maze) or y < 0 or y >= len(maze[0]):
        return None
    return maze[x][y]  # could be '!', 'o', ' ', '#'


def check_valids(maze, index):
    valid_moves = []  # a list of the nodes that IA can turn to
    x = index[0]
    y = index[1]
    box = [(x-1, y), (x, y+1), (x+1, y), (x, y-1)]
    vals = [value(maze, x-1, y), value(maze, x, y+1),
            value(maze, x+1, y), value(maze, x, y-1)]
    for i in range(4):
        if vals[i] in ['!', 'o', ' ']:
            valid_moves.append(box[i])
    return valid_moves


def Astar_search(maze, start, target):
    # return a list of nodes in the shortest road from start to target
    road = []
    info = {}  # info[node] = [parent, g, h, f]
    info[start] = [None, 0, 0, 0]
    open_list = [start]
    closed_list = []

    # loop until find out target
    while len(open_list) > 0:

        # get the next current node
        cur = open_list[0]  # current node
        cur_index = 0  # index of current in open_list
        for index, item in enumerate(open_list):
            if info[item][3] < info[cur][3]:  # if f-value of item is lower
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

            # get the parent, g, h, f values:
            par = cur  # the node before current
            g = info[cur][1] + 1  # shortest road from start to current
            # heuristic distance:
            h = abs(target[0] - v[0]) + abs(target[1] - v[1])
            f = g + h

            # if v has lower f-value, pass
            if v in open_list and info[v][1] <= g:
                continue

            # set the parent, g, h, f values of v, then add v to open_list
            info[v] = [par, g, h, f]
            if v not in open_list:
                open_list.append(v)
    # if there's no road to target:
    if road == []:
        return [start, choice(check_valids(maze, start))]


def target(maze, index, ephs, pers):  # find the closest resource
    min = 21
    if ephs != []:  # there are '!' in map
        for e in ephs:
            s = Astar_search(maze, index, e)
            f = len(s)
            if f < min:
                min = f
                closest = s
    if min == 21:  # there is no reachable '!' in map, get an 'o'
        closest = Astar_search(maze, index, pers[0])
        min = len(closest)
        for e in pers:
            s = Astar_search(maze, index, e)
            f = len(s)
            if f < min:
                min = f
                closest = s
    # if others != []:
    return closest  # return the road from index to target


def move(maze, searched):  # list of moves for the searched road
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
others = []  # list of other IAs
line = stdin.readline()
while line != '':
    if line == 'MAZE\n':
        update_maze()
        searched_road = target(maze, start, ephs, pers)
        output = move(maze, searched_road)
        print(output[0])  # move the first step than update maze

    line = stdin.readline()
