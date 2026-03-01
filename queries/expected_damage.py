import argparse
import psycopg2
import os
import csv
import sys

parser = argparse.ArgumentParser(
    prog="expected_damage", description="Calcuated expected value of pokemon moves"
)


def main():
    args = parser.parse_args()

    conn = psycopg2.connect(f"host=localhost user={os.getenv("USER")} password=foobar")

    with conn.cursor() as cur:
        cur.execute("""
select 
    moves.name, types.name, power, accuracy, 
    power * accuracy / 100 as expected_power 
from "moves" 
    join "types" on moves.ty = types.id 
where power is not null and accuracy is not null 
order by (power * accuracy) desc;
            """)
        out = csv.writer(sys.stdout)
        out.writerow(("Move", "Type", "Power", "Accuracy", "Expected Damage"))
        for move, ty, power, accuracy, expected in cur:
            out.writerow((move, ty, power, accuracy, expected))


if __name__ == "__main__":
    main()
