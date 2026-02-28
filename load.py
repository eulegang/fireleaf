import psycopg2
import os
import glob
import json

attr_trans = {
    'Attack': 'Attack',
    'Defense': 'Defense',
    'HP': 'HP',
    'Sp. Atk': 'Special Attack',
    'Sp. Def': 'Special Defense',
    'Speed': 'Speed'
}

def main():
    conn = psycopg2.connect(f"host=localhost user={os.getenv("USER")} password=foobar")

    with conn.cursor() as cur:
        cur.execute("select id, name from types")
        types = { name: id for id, name in cur.fetchall() }

    for file in glob.glob("data/pokemon/*.json"):
        with open(file, 'r') as fp:
            data = json.load(fp)
        print(data['name'])
        
        learned = []
        for move in data["moves"]["learned"]:
            with conn.cursor() as cur:
                try:
                    cur.execute("select id from moves where name = %s", (move["name"],))
                    move_id, = cur.fetchone()
                except:
                    cur.execute(
                        """
                            insert into moves
                            (name, ty, power, accuracy) 
                            values (%s, %s, %s, %s)
                            returning id
                        """,
                        (
                            move["name"],
                            types[move["type"]],
                            move["power"],
                            move["accuracy"]
                        )
                    )
                    move_id, = cur.fetchone()

                learned.append({"id": move_id, "level": move['level']})

        tms = []
        for move in data["moves"]["tm"]:
            with conn.cursor() as cur:
                try:
                    cur.execute("select id from moves where name = %s", (move["name"],))
                    move_id, = cur.fetchone()
                except:
                    cur.execute(
                        """
                            insert into moves
                            (name, ty, power, accuracy) 
                            values (%s, %s, %s, %s)
                            returning id
                        """,
                        (
                            move["name"],
                            types[move["type"]],
                            move["power"],
                            move["accuracy"]
                        )
                    )
                    move_id, = cur.fetchone()

                tms.append({"id": move_id, "tm": move['tm']})
        
        with conn.cursor() as cur:
            try:
                cur.execute("select id from pokemon where name = %s", (data["name"],))
                pokemon_id = cur.fetchone()[0]
            except:
                cur.execute(
                    """
                        insert into pokemon
                        (name, primary_type, secondary_type, growth, stats) 
                        values (%s, %s, %s, %s, (%s, %s, %s, %s, %s, %s))
                        returning id
                    """,
                    (
                        data["name"],
                        types[data["types"][0]],
                        types[data["types"][1]] if len(data["types"]) > 1 else None,
                        data["growth"],
                        data["stats"]["hp"],
                        data["stats"]["atk"],
                        data["stats"]["def"],
                        data["stats"]["spa"],
                        data["stats"]["spd"],
                        data["stats"]["sp"],
                    )

                )
                pokemon_id = cur.fetchone()[0]

        for move in learned:
            with conn.cursor() as cur:
                cur.execute("select * from pokemon_moves where pokemon_id = %s and move_id = %s and level = %s", (pokemon_id, move["id"], move["level"]))
                if not cur.fetchone():
                    cur.execute("insert into pokemon_moves (pokemon_id, move_id, level) values (%s, %s, %s) returning *", (pokemon_id, move["id"], move["level"]))

        for move in tms:
            with conn.cursor() as cur:
                cur.execute("select * from pokemon_moves where pokemon_id = %s and move_id = %s and tm = %s", (pokemon_id, move["id"], move["tm"]))
                if not cur.fetchone():
                    cur.execute("insert into pokemon_moves (pokemon_id, move_id, tm) values (%s, %s, %s) returning *", (pokemon_id, move["id"], move["tm"]))


        with conn.cursor() as cur:
            for ev in data["ev"]:
                value, attr = ev.split(' ', 1)
                value = int(value)
                attr = attr_trans[attr]

                cur.execute("select id from ev where amount = %s and attribute = %s", (value, attr))

                if row := cur.fetchone():
                    ev_id = row[0]
                else:
                    cur.execute("insert into ev (amount, attribute) values (%s, %s) returning id", (value, attr))
                    ev_id = cur.fetchone()[0]

                cur.execute("select * from pokemon_ev where pokemon_id = %s and ev_id = %s", (pokemon_id, ev_id))
                if not cur.fetchone():
                    cur.execute("insert into pokemon_ev (pokemon_id, ev_id) values (%s, %s)", (pokemon_id, ev_id))


    conn.commit()

if __name__ == "__main__":
    main()
