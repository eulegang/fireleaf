from store import Store
from re import compile
from itertools import islice
import json
import os

init_page = 'https://pokemondb.net/pokedex/game/firered-leafgreen'
base = 'https://pokemondb.net'

name_in_title = compile("(?P<name>.*) Pokédex")
where_to_find = compile("Where to find ")

moves = set()

store = Store()

def find_stats(url, page):
    data = {}
    title = page.find("title").string

    if m := name_in_title.match(title):
        data['name'] = m['name']

    data_section = page.find("h2", string = "Pokédex data").parent
    data['types'] = [t.string for t in data_section.find("th", string="Type").parent.find("td").select('a')]

    training_section = page.find("h2", string = "Training").parent
    data["ev"] = training_section.find("th", string="EV yield").parent.find("td").string.strip().split(", ")
    data["growth"] = training_section.find("th", string="Growth Rate").parent.find("td").string.strip()

    base_stats = page.find("h2", string = "Base stats").parent
    data["stats"] = {
        "hp": int(base_stats.find("th", string = "HP").parent.select('td')[0].string),
        "atk": int(base_stats.find("th", string = "Attack").parent.select('td')[0].string),
        "def": int(base_stats.find("th", string = "Defense").parent.select('td')[0].string),
        "spa": int(base_stats.find("th", string = "Sp. Atk").parent.select('td')[0].string),
        "spd": int(base_stats.find("th", string = "Sp. Def").parent.select('td')[0].string),
        "sp": int(base_stats.find("th", string = "Speed").parent.select('td')[0].string),
    }


    location_section = page.find("h2", string=where_to_find).parent
    data['locations'] = [{"name": loc.string, "href": loc["href"] } for loc in location_section.find("span", string=compile("Fire")).parent.parent.select("a")]

    moves_page = store.get(url + "/moves/3")

    learned = []
    learn_table = moves_page.select("#tab-moves-6")[0].find("h3", string="Moves learnt by level up").find_next("table")
    for move in learn_table.select('tr')[1:]:
        [level, name, ty, cat, power, acc] = [e.string or e['data-filter-value'] for e in move.select('td')]
        learned.append({
            "level": level,
            "name": name,
            "type": ty,
            "category": cat,
            "power": power,
            "accuracy": acc,
        })

    tms = []
    tm_table = moves_page.select("#tab-moves-6")[0].find("h3", string="Moves learnt by TM").find_next("table")
    for move in tm_table.select('tr')[1:]:
        [tm, name, ty, cat, power, acc] = [e.string or e['data-filter-value'] for e in move.select('td')]
        tms.append({
            "tm": tm,
            "name": name,
            "type": ty,
            "category": cat,
            "power": power,
            "accuracy": acc,
        })

    data['moves'] = {
        'learned': learned,
        'tm': tms
    }

    return data


def main():
    page = store.get(init_page)
    pokemons = page.select('.infocard-list a.ent-name')

    os.makedirs("data/pokemon", exist_ok=True)

    pokemon_pages = (
        (base + pokemon['href'], store.get(base + pokemon['href']))
        for pokemon in pokemons
    )

    for (url, page) in pokemon_pages:
        print(url)
        data_sheet = find_stats(url, page)

        with open(f"data/pokemon/{data_sheet['name']}.json", 'w') as fp:
            json.dump(data_sheet, fp)


if __name__ == "__main__":
    main()
