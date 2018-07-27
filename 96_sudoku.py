# -*- coding: utf-8 -*-
import math

from collections import defaultdict
from io import StringIO

import ipdb
import sys


class MissingCollection:
    def __init__(self):
        self.missing = []
        for i in range(9):
            self.missing.append({i: True for i in range(1, 10)})

    def populate(self, index, val):
        self.missing[index].pop(val, None)

    def unset(self, index, val):
        self.missing[index][val] = True

    def get_missing(self, index):
        return set(self.missing[index].keys())

    def __str__(self):
        return '{}'.format(self.missing)


class SudokuSolver:

    def __init__(self, grid):
        self.grid = grid
        self.row_missing = MissingCollection()
        self.col_missing = MissingCollection()
        self.box_missing = MissingCollection()
        self.missing_indices = {}
        self._setup()
        self.counter = 0
        print("No of missing: {}".format(len(self.missing_indices)))

    @staticmethod
    def get_box_index(i, j):
        return int(math.floor(i / 3) * 3 + math.floor(j / 3))

    def _setup(self):
        for i in range(9):
            for j in range(9):
                val = self.grid[i][j]
                if not val:
                    self.missing_indices[(i, j)] = None
                    continue

                self.row_missing.populate(i, val)
                self.col_missing.populate(j, val)
                box_index = self.get_box_index(i, j)
                self.box_missing.populate(box_index, val)

    def get_possible_solution(self, i, j):
        k = self.get_box_index(i, j)
        missing_row = self.row_missing.get_missing(i)
        missing_col = self.col_missing.get_missing(j)
        missing_box = self.box_missing.get_missing(k)
        return missing_row.intersection(missing_col).intersection(missing_box)

    def set_value(self, point, val):
        #print("Setting Value", point, val)
        i, j = point
        self.missing_indices.pop(point)
        self.grid[i][j] = val
        self.row_missing.populate(i, val)
        self.col_missing.populate(j, val)
        box_index = self.get_box_index(i, j)
        self.box_missing.populate(box_index, val)

    def unset_val(self, point):
        #print("Unsetting Value", point)
        i, j = point
        k = self.get_box_index(i, j)
        old_val = self.grid[i][j]
        self.grid[i][j] = 0
        self.missing_indices[(i, j)] = True
        self.row_missing.unset(i, old_val)
        self.col_missing.unset(j, old_val)
        self.box_missing.unset(k, old_val)

    def solve(self):
        # no_missing = len(self.missing_indices)
        # while len(self.missing_indices) > 0:
        #     print("No of missing", no_missing)
        #     missing_indices = list(self.missing_indices.keys())
        #     row_uniq = defaultdict(dict)
        #     col_uniq = defaultdict(dict)
        #     box_uniq = defaultdict(dict)
        #     for (i, j) in missing_indices:
        #         k = self.get_box_index(i, j)
        #         poss_values = self.get_possible_solution(i, j)
        #         print("Possible Values", (i, j), poss_values)
        #         for val in poss_values:
        #             point = (i, j)
        #             row_count = row_uniq[i].get(val, (None, 0))[1] + 1
        #             row_uniq[i][val] = (point, row_count)
        #
        #             col_count = col_uniq[j].get(val, (None, 0))[1] + 1
        #             col_uniq[j][val] = (point, col_count)
        #
        #             box_count = box_uniq[k].get(val, (None, 0))[1] + 1
        #             box_uniq[k][val] = (point, box_count)
        #
        #         if len(poss_values) == 1:
        #             self.set_value((i, j), poss_values.pop())
        #
        #     missing_indices = list(self.missing_indices.keys())
        #     for (i, j) in missing_indices:
        #         k = self.get_box_index(i, j)
        #         for val, (point, count) in row_uniq[i].items():
        #             if count == 1 and point in self.missing_indices:
        #                 self.set_value(point, val)
        #
        #         for val, (point, count) in col_uniq[j].items():
        #             if count == 1 and point in self.missing_indices:
        #                 self.set_value(point, val)
        #
        #         for val, (point, count) in box_uniq[k].items():
        #             if count == 1 and point in self.missing_indices:
        #                 self.set_value(point, val)
        #
        #     if no_missing == len(self.missing_indices):
        #         print("Unsolvable")
        #         sys.exit(1)
        #     else:
        #         no_missing = len(self.missing_indices)
        #

        if self.backtrack_solver():
            #print("Attempts: ", self.counter)
            return ''.join([str(i) for i in self.grid[0][0:3]])
        print("Unsolvable")

    def backtrack_solver(self):
        # self.counter += 1
        # if self.counter % 10000 == 0:
        #     print("Attempt No: ", self.counter)
        missing_indices = list(self.missing_indices.keys())
        #print("Missing Count: ", len(missing_indices))
        if not missing_indices:
            return True
        i, j = missing_indices[0]
        poss_values = self.get_possible_solution(i, j)
        for num in poss_values:
            self.set_value((i, j), num)
            if not self.backtrack_solver():
                self.unset_val((i, j))
            else:
                return True

        return False


def main():
    grids = []
    with open('files/96_sudoku.txt') as fd:
        lines = fd.readlines()
        index = -1
        i = 0
        for line in lines:
            if line.startswith('G'):
                index += 1
                i = 0
                grids.append([])
                continue

            grids[index].append([])
            for j in range(len(line) - 1):
                grids[index][i].append(int(line[j]))
            i += 1

    answer = StringIO()
    for (i, grid) in enumerate(grids):
        solver = SudokuSolver(grid)
        sol = solver.solve()
        print("Solution {}: {}".format(i, sol))
        answer.write(sol)

    print(answer.getvalue())


if __name__ == '__main__':
    main()
