#!/usr/bin/env python3

from sys import stdin, stdout, stderr
from random import choice
from os import system


def get_maze():  # return a list of str(rows)
    maze = []
    while True:
        row = stdin.readline()
        if row == '\n':
            break
        maze.append(row[:-1])
    return maze


def guess_kind_is_maze(maze):  # guess if shape of the map is maze
    walls = []
    for x, row in enumerate(maze):
        for y, value in enumerate(row):
            if value == '#':
                walls.append((x, y))
    size = len(maze) * len(maze[0])
    t = len(walls)/size
    return (size > 200 and t > 0.5 and t < 0.8)


def get_pos(maze, letter):  # get position of my IA
    for x, row in enumerate(maze):
        for y, value in enumerate(row):
            if value == letter:
                return (x, y)


def list_coins(maze):  # return list position of 'o'
    coins = []
    for x, row in enumerate(maze):
        for y, value in enumerate(row):
            if value == 'o':
                coins.append((x, y))
    return coins


def list_bonus(maze):  # return list position of '!'
    bonuses = []
    for x, row in enumerate(maze):
        for y, value in enumerate(row):
            if value == '!':
                bonuses.append((x, y))
    return bonuses


def list_other_IAs(maze, letter):  # return list of other IAs
    others = []
    for x, row in enumerate(maze):
        for y, value in enumerate(row):
            if value not in [' ', '!', 'o', '#', letter]:
                others.append((x, y))
    return others


def check_valids(maze, pos):  # check if 4 positions around pos are reachable
    valid_moves = []
    x = pos[0]
    y = pos[1]
    box = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
    for b in box:
        if b[0] in range(len(maze)) and b[1] in range(len(maze[0])):
            value = maze[b[0]][b[1]]  # value of position b
            if value == '!':  # if b is bonus, add to head of list
                valid_moves.insert(1, b)
            elif value != '#':
                valid_moves.append(b)
    return valid_moves


def heuristic_distance(start, goal):  # heuristic distance between 2 positions
    return abs(goal[0] - start[0]) + abs(goal[1] - start[1])


def choose_target(maze, myIA, exception=()):
    # choose a target of IA in maze which is not "exception"
    valids = check_valids(maze, myIA)

    # lists of coins and bonuses, the exception unincluded
    temp_bonus = []
    temp_coins = []
    for e in Coins:
        if e != exception:
            temp_coins.append(e)
    for e in Bonus:
        if e != exception:
            temp_bonus.append(e)
    if len(valids) == 1:
        return valids[0]
    for v in valids:
        if v in temp_bonus + temp_coins:
            return v

    # if there are '!' in map, find which is reachable in 20 turns
    shortest_distance = 21
    target = temp_coins[0]
    if temp_bonus != []:  # there are '!' in map
        for e in temp_bonus:
            h = heuristic_distance(myIA, e)
            if h < shortest_distance:
                shortest_distance = h
                target = e

    # if there is no reachable '!' in map, get an 'o'
    if shortest_distance == 21:
        shortest_distance = heuristic_distance(myIA, target)
        for e in temp_coins:
            h = heuristic_distance(myIA, e)
            if h < shortest_distance:
                shortest_distance = h
                target = e

    return target


def Astar_search(maze, start, target):
    # return a list of nodes in the shortest road from target to start
    road = []
    info = {}  # info[node] = [parent, g, h, f]
    info[start] = [None, 0, 0, 0]
    open_list = [start]
    closed_list = []

    # loop until find out target
    while open_list:

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
            road.append(cur)
            c = cur
            while info[c][0] is not None:
                road.append(info[c][0])
                c = info[c][0]
            road.reverse()
            return road

        # valids
        valids = check_valids(maze, cur)
        if cur == start:
            for v in valids:
                if v in other_IAs:
                    valids.remove(v)

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
    return road


def move(pos, next_pos):  # move 1 step from current position to the next
    moves = ["MOVE UP\n\n", "MOVE RIGHT\n\n", "MOVE DOWN\n\n", "MOVE LEFT\n\n"]
    xx = next_pos[0] - pos[0]
    yy = next_pos[1] - pos[1]
    if xx > 0:
        return moves[2]
    elif xx < 0:
        return moves[0]
    elif yy > 0:
        return moves[1]
    elif yy < 0:
        return moves[3]


def another_target(maze, myIA, Target, Road, is_maze):
    # function to find a better target

    another = choose_target(maze, myIA, Target)
    if heuristic_distance(myIA, another) < len(Road):
        new_road_maybe = Astar_search(maze, myIA, another)
        if len(new_road_maybe) < len(Road):
            Target = another

    # if len(Road) == 2:
    #     around_target = check_valids(maze, Target)
    #     for a in around_target:
    #         if a in other_IAs:
    #             Target = another

    # in the last 10 turns to Target, if anyother is nearer than my IA
    elif len(Road) < 10:
        for o in other_IAs:
            h_of_o = heuristic_distance(o, Target)
            if h_of_o < len(Road):
                # change the target if it was unreachable
                if is_maze:
                    road_of_o = Astar_search(maze, o, Target)
                    if len(road_of_o) < len(Road):
                        Target = another
                else:
                    Target = another
    return Target


def main():
    global Coins, Bonus, other_IAs, Target
    myIA = ()
    Road = [myIA]
    Target = ()
    moves = ["MOVE UP\n\n", "MOVE RIGHT\n\n", "MOVE DOWN\n\n", "MOVE LEFT\n\n"]
    stdin.readline()  # VM: "HELLO\n"
    stdin.readline()  # "\n"
    stdout.write("I AM MAX\n\n")
    letter = stdin.readline()[-2]  # get the letter from "YOU ARE <letter>\n"
    stdin.readline()  # "\n"
    stdout.write("OK\n\n")
    line = stdin.readline()
    Maze = get_maze()
    Coins = list_coins(Maze)
    Bonus = list_bonus(Maze)
    myIA = get_pos(Maze, letter)
    other_IAs = list_other_IAs(Maze, letter)
    is_maze = guess_kind_is_maze(Maze)
    while line != '':
        if len(Road) <= 1:
            Target = choose_target(Maze, myIA, Target)
            Road = Astar_search(Maze, myIA, Target)

        Another = another_target(Maze, myIA, Target, Road, is_maze)
        if Another != Target:
            Target = Another
            Road = Astar_search(Maze, myIA, Target)

        if len(Road) == 0:
            Valids = check_valids(Maze, myIA)
            for v in Valids:
                if v in other_IAs:
                    Valids.remove(v)
            Target = choice(Valids)
            Road = [myIA, Target]

        if len(Road) > 1:
            s = Road.pop(0)
            t = Road[0]
            # if the next position is an other IA, don't hit him
            if t in other_IAs:
                Valids = check_valids(Maze, s)
                for v in Valids:
                    if v in other_IAs:
                        Valids.remove(v)
                Target = choice(Valids)
                Road = [myIA]
                stdout.write(move(myIA, Target))
            else:
                stdout.write(move(s, t))
        line = stdin.readline()
        if line == "MAZE\n":
            Maze = get_maze()
            Coins = list_coins(Maze)
            Bonus = list_bonus(Maze)
            myIA = get_pos(Maze, letter)
            other_IAs = list_other_IAs(Maze, letter)


if __name__ == "__main__":
    main()
