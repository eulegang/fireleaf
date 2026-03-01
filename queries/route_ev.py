import argparse
import psycopg2
import os
import csv
import sys

parser = argparse.ArgumentParser(
    prog="route_ev",
    description="Look up pokemon for routes for ev planning",
)


def main():
    args = parser.parse_args()

    conn = psycopg2.connect(f"host=localhost user={os.getenv("USER")} password=foobar")

    with conn.cursor() as cur:
        cur.execute("""
with locations as (
  select pokemon.id, pokemon.name pokemon, locations.name location
  from pokemon 
    join pokemon_locations on pokemon_locations.pokemon_id = pokemon.id
    join locations on locations.id = pokemon_locations.location_id
), evs as (
  select pokemon.id, amount, attribute 
  from pokemon
    join pokemon_ev on pokemon.id = pokemon_ev.pokemon_id
    join ev on pokemon_ev.ev_id = ev.id
) 
  select pokemon, location, amount, attribute from locations 
    join evs on evs.id = locations.id
    order by attribute;
            """)
        out = csv.writer(sys.stdout)
        out.writerow(("Pokemon", "Location", "Amount", "Attribute"))
        for row in cur:
            out.writerow(row)


if __name__ == "__main__":
    main()
