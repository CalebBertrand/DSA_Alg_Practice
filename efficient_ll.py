# Not a leetcode problem, but this is a neat trick you can use to get very space efficient linked lists!
# Great if you know the size of the linked list ahead of time
# This particular implementation also allows you to get a node in O(1) time if you know the value

from typing import Iterable, Protocol


class Comparable(Protocol):
    def __lt__(self, other, /) -> bool: ...


def init_ll[TVal: Comparable](vals: Iterable[TVal], sort=False):
    i = 0
    i_by_val = {}
    values = []
    next_i = []

    def next_of(val: TVal):
        val_i = i_by_val.get(val)
        if val_i is None:
            raise ValueError("That value does not exist in this list")
        i = next_i[val_i]
        if i is not None:
            return values[i]
        return None

    def set_next_of(val: TVal, next_val: TVal):
        next_val_i = i_by_val.get(next_val)
        if next_val_i is None:
            raise ValueError("That next value is not in this list")
        val_i = i_by_val.get(val)
        if val_i is None:
            raise ValueError("That value is not in the list")
        next_i[val_i] = next_val_i

    if sort:
        iterator = iter(vals)
        root = next(iterator)
        values.append(root)
        i_by_val[root] = 0
        next_i.append(None)

        for v in iterator:
            new_i = len(values)
            values.append(v)
            i_by_val[v] = new_i
            next_i.append(None)

            if v < root:
                next_i[new_i] = i_by_val[root]
                root = v
            else:
                curr_i = i_by_val[root]
                while next_i[curr_i] is not None and values[next_i[curr_i]] < v:
                    curr_i = next_i[curr_i]
                next_i[new_i] = next_i[curr_i]
                next_i[curr_i] = new_i

        return root, next_of, set_next_of
    else:
        for i, v in enumerate(vals):
            values.append(v)
            i_by_val[v] = i
            if i > 0:
                next_i.append(i)
        next_i.append(None)

        # root, get next given value, set next of value
        return values[0], next_of, set_next_of


if __name__ == "__main__":
    root, next_of, set_next_of = init_ll([1, 2, 3, 4, 5])
    print(f"Expect 1: {root}")
    print(f"Expect 2: {next_of(root)}")

    set_next_of(3, 5)

    print(f"Expect 5: {next_of(3)}")
