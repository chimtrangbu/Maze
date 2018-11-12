#!/usr/bin/env python3

from sys import stdin, stdout, stderr
from random import choice
from os import system


def update_maze():
    global maze, ephemeral_resources, permanent_resources, other_IAs, myIA
    maze.clear()
    while True:
        row = stdin.readline()
        if row == '\n':
            break
        maze.append(row[:-1])
    ephemeral_resources.clear()
    permanent_resources.clear()
    other_IAs.clear()
    for x, row in enumerate(maze):
        for y, value in enumerate(row):
            if value == letter:
                myIA = (x, y)
            elif value == '!':
                ephemeral_resources.append((x, y))
            elif value == 'o':
                permanent_resources.append((x, y))
            elif value not in [' ', '#', letter]:
                other_IAs.append((x, y))


def check_valids(maze, pos):
    valid_moves = []
    x = pos[0]
    y = pos[1]
    box = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
    for b in box:
        if b[0] in range(len(maze)) and b[1] in range(len(maze[0])):
            value = maze[b[0]][b[1]]
            if value == '!':
                valid_moves.insert(1, b)
            elif value != '#':
                valid_moves.append(b)
    return valid_moves


def heuristic_distance(start, goal):
    return abs(goal[0] - start[0]) + abs(goal[1] - start[1])


def Astar_search(maze, start, target):
    # return a list of nodes in the shortest road from target to start
    # road = []
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
            h = heuristic_distance(v, target)
            f = g + h

            # if v has lower f-value, pass
            if v in open_list and info[v][1] <= g:
                continue

            # set the parent, g, h, f values of v, then add v to open_list
            info[v] = [par, g, h, f]
            if v not in open_list:
                if cur == start and v in other_IAs:
                    closed_list.append(v)
                else:
                    open_list.append(v)


def choose_target(maze, myIA):
    valids = check_valids(maze, myIA)
    if len(valids) == 1:
        return valids[0]
    for v in valids:
        if v in ephemeral_resources + permanent_resources:
            return v
    shortest_distance = 21
    target = permanent_resources[0]
    if ephemeral_resources != []:  # there are '!' in map
        for e in ephemeral_resources:
            h = heuristic_distance(myIA, e)
            if h < shortest_distance:
                shortest_distance = h
                target = e
        road = Astar_search(maze, myIA, target)
        if road is None or len(road) > 20:
            shortest_distance = 21
    if shortest_distance == 21:  # there is no reachable '!' in map, get an 'o'
        shortest_distance = heuristic_distance(myIA, permanent_resources[0])
        # target = permanent_resources[0]
        for e in permanent_resources:
            h = heuristic_distance(myIA, e)
            if h < shortest_distance:
                shortest_distance = h
                target = e
    return target


def something_around(maze, myIA):
    global Road, Target

    valids = check_valids(maze, myIA)
    for v in valids:
        if v not in other_IAs:
            movable = v

    if Road is None:
        Road = [myIA, movable]

    another_target = choose_target(maze, myIA)
    if heuristic_distance(myIA, another_target) < len(Road):
        new_road_maybe = Astar_search(maze, myIA, another_target)
        if new_road_maybe is not None:
            if len(new_road_maybe) < len(Road):
                Target = another_target
                Road = new_road_maybe

    for v in valids:
        if v in other_IAs and v in Road:
            Road = [myIA, movable]
            break


def main():
    global maze, ephemeral_resources, permanent_resources, \
           other_IAs, myIA, letter, Road, Target
    maze = []
    ephemeral_resources = []
    permanent_resources = []
    other_IAs = []
    Road = []
    moves = ["MOVE UP\n\n", "MOVE RIGHT\n\n", "MOVE DOWN\n\n", "MOVE LEFT\n\n"]
    stdin.readline()  # VM: "HELLO\n"
    stdin.readline()  # "\n"
    stdout.write("I AM MAX\n\n")
    letter = stdin.readline()[-2]  # get the letter from "YOU ARE <letter>\n"
    stdin.readline()  # "\n"
    stdout.write("OK\n\n")
    line = stdin.readline()
    while line != '':
        if line == "MAZE\n":
            update_maze()
        if len(Road) <= 1:
            Target = choose_target(maze, myIA)
            Road = Astar_search(maze, myIA, Target)
        if Target not in ephemeral_resources + permanent_resources:
            Target = choose_target(maze, myIA)
            Road = Astar_search(maze, myIA, Target)
        something_around(maze, myIA)
        if len(Road) > 1:
            s = Road.pop(0)
            t = Road[0]
            xx = t[0] - s[0]
            yy = t[1] - s[1]
            if xx > 0:
                stdout.write(moves[2])
            if xx < 0:
                stdout.write(moves[0])
            if yy > 0:
                stdout.write(moves[1])
            if yy < 0:
                stdout.write(moves[3])
            # check_dangerous()
        line = stdin.readline()


if __name__ == "__main__":
    main()
