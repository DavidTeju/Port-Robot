import csv
import sys

from Bot import Bot

"""
z -> level (2D array)
y -> row (1D array)
x -> column (cell)
"""


# x, y number from origin
# z number from ground

def load_manifest():
    with open("manifest.csv", "r+", encoding='utf-8-sig') as manifest:
        manifest_data = list(csv.reader(manifest))

    header = manifest_data.pop(0)

    def get_from_manifest(header_name):
        to_return = row[header.index(header_name)]
        try:
            return int(to_return) if header_name == "Group" else int(to_return) - 1
        except ValueError:
            return ord(to_return) - 65

    to_fill = [[[0 for _ in range(col_size)] for _ in range(row_size)] for _ in range(lev_size)]
    for row in manifest_data:
        to_fill[get_from_manifest("Level")][get_from_manifest("Row")][get_from_manifest("Column")] \
            = get_from_manifest("Group")

    return to_fill


def offload_cargo(x, y, z):
    """
    :param x: the column index
    :param y: the row index
    :param z: the level index
    :return: None
    """
    for z_1 in reversed(range(z, len(grid))):
        if grid[z_1][y][x]:
            offload_sequence.append(((x, y, z_1), grid[z_1][y][x]))
            grid[z_1][y][x] = 0


# Memoize
max_above = 0


def calc_worth(x, y, z):
    global max_above
    curr = grid[z][y][x]
    max_above = max_above or max(
        sum(grid[i][j][k] for i in range(1, len(grid)) if grid[i][j][k] != curr) for j in range(row_size) for k in
        range(col_size))
    above = sum(grid[level][y][x] for level in range(z + 1, len(grid)))
    above_curved = 0 if max_above == 0 else above / max_above

    return curr + above_curved if curr else sys.maxsize


def optimal_offload_seq() -> list[tuple[tuple[int, int, int], int]]:
    global offload_sequence
    offload_sequence = []
    indices = [(x, y, z) for z in range(lev_size) for y in range(row_size) for x in range(col_size) if grid[z][y][x]]
    while indices:
        best = min(indices, key=lambda tup: calc_worth(*tup))
        offload_cargo(*best)
        indices.remove(best)
    return offload_sequence


def load_coords():
    with open("coordinates.csv", "r+", encoding='utf-8-sig') as file:
        coordinates = list(csv.reader(file))
    header_column = [row.pop(0) for row in coordinates]
    colsize = coordinates.pop(header_column.index("colsize"))[0]
    header_column.remove("colsize")
    coordinates = [[float(member) for member in inner] for inner in coordinates]

    return int(colsize), {header: tuple(coordinates[header_column.index(header)]) for header in header_column}


col_size, coords = load_coords()
row_size = len(coords["rows"])
lev_size = len(coords["levels"])
grid = load_manifest()

landing_locs = tuple([(i, j, k) for k in range(lev_size) for i in range(col_size, len(coords["columns"]))] for j in
                     range(row_size))

if __name__ == '__main__':
    for block in optimal_offload_seq():  # block[block-location, priority]
        Bot.move_to(coords["columns"][block[0][0]], coords["rows"][block[0][1]], coords["levels"][block[0][2]])

        landing_loc = landing_locs[block[1] - 1].pop(0)
        Bot.move_to(coords["columns"][landing_loc[0]], coords["rows"][landing_loc[1]], coords["levels"][landing_loc[2]])

        Bot.magnet_off(3)
