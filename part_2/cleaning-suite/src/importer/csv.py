from checker.db import RowFactory
import csv


def read_csv[T](filename: str, *, row_factory: RowFactory[T]) -> list[T]:
    print(f"loading from {filename}")
    with open(filename, "r") as f:
        rdr = csv.DictReader(f, delimiter=",")
        vals: list[T] = []
        for idx, row in enumerate(rdr):
            try:
                val = row_factory(row)
                vals.append(val)
            except Exception as e:
                print(f"couldn't load item {idx+1}: {e}")
                raise
        print(f"loaded {len(vals)} from {filename}")
        return vals
