#!/usr/bin/env python3

from sys import stdin, stdout, stderr
from random import choice
from os import system


def update_maze():
    global start, pers, ephs
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


def value(maze, tuple):  # value of position(x, y) in maze
    x = tuple[0]
    y = tuple[1]
    if x < 0 or x >= len(maze) or y < 0 or y >= len(maze[0]):
        return None
    return maze[x][y]  # could be '!', 'o', ' ', '#' or an other letter


def check_valids(maze, index):
    valid_moves = []  # a list of the nodes that IA can turn to
    x = index[0]
    y = index[1]
    box = [(x-1, y), (x, y+1), (x+1, y), (x, y-1)]
    vals = [value(maze, box[0]), value(maze, box[1]),
            value(maze, box[2]), value(maze, box[3])]
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


def choose_target(maze, start, ephs, pers):  # find the closest resource
    valids = check_valids(maze, start)
    for v in valids:
        if value(maze, v) == '!' or value(maze, v) == 'o':
            return [start, v]
    min = 21
    if ephs != []:  # there are '!' in map
        for e in ephs:
            road_to_e = Astar_search(maze, start, e)
            f = len(road_to_e)
            if f < min:
                min = f
                closest = road_to_e
    if min == 21:  # there is no reachable '!' in map, get an 'o'
        closest = Astar_search(maze, start, pers[0])
        min = len(closest)
        for e in pers:
            road_to_e = Astar_search(maze, start, e)
            f = len(road_to_e)
            if f < min:
                min = f
                closest = road_to_e
    return closest  # return the road from start to target


def move(maze, searched):  # return the first move for the searched road
    moves = ["MOVE UP\n\n", "MOVE RIGHT\n\n", "MOVE DOWN\n\n", "MOVE LEFT\n\n"]
    result = ''
    s = searched[0]
    t = searched[1]
    xx = t[0] - s[0]
    yy = t[1] - s[1]
    if xx > 0:
        return moves[2]
    if xx < 0:
        return moves[0]
    if yy > 0:
        return moves[1]
    if yy < 0:
        return moves[3]


maze = []
pers = []  # list of permanent resources
ephs = []  # list of ephemeral resources
letter = 'A'


def main():
    global maze, pers, ephs, letter
    input()  # VM: "HELLO\n"
    input()  # VM: "\n"
    print("I AM MAX\n")
    letter = input()  # VM: "YOU ARE <letter>\n"
    input()  # VM: "\n"
    print("OK\n")
    letter = letter[-1]  # get the <letter> from "YOU ARE <letter>"

    line = stdin.readline()
    while line != '':
        if line == 'MAZE\n':
            update_maze()
            searched_road = choose_target(maze, start, ephs, pers)
            output = move(maze, searched_road)
            stdout.write(output)  # move the first step then update maze

        line = stdin.readline()


if __name__ == "__main__":
    main()
