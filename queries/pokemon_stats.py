import argparse
import psycopg2
import os
import csv
import sys

parser = argparse.ArgumentParser(
    prog="bst",
    description="Analyse base stats of pokemon and order according to primmary offensive stat with best defensive stat",
)


def main():
    args = parser.parse_args()

    conn = psycopg2.connect(f"host=localhost user={os.getenv("USER")} password=foobar")

    with conn.cursor() as cur:
        cur.execute("""

select *, offense * defense power from (
select 
  pokemon.name, types.name, types.category,
  (pokemon.stats).atk, (pokemon.stats).spa,
  (pokemon.stats).def, (pokemon.stats).spd,
  case when types.category = 'Physical' then (pokemon.stats).atk else (pokemon.stats).spa end as offense,
  greatest((pokemon.stats).def, (pokemon.stats).spd) as defense
from pokemon 
join types on types.id = pokemon.primary_type
where pokemon.name not in ('Mewtwo', 'Mew', 'Zapdos', 'Moltres', 'Articuno'))
order by offense * defense desc;
            """)
        out = csv.writer(sys.stdout)
        out.writerow(
            (
                "Pokemon",
                "Type",
                "Attack",
                "Special Attack",
                "Defense",
                "Special Defense",
                "Offense",
                "Defense",
                "Power",
            )
        )
        for row in cur:
            out.writerow(row)


if __name__ == "__main__":
    main()
