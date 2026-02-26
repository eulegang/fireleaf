from store import Store

base = 'https://pokemondb.net/pokedex/game/firered-leafgreen'

def main():
    store = Store()
    store.get(base)
    # print(store.get(base))


if __name__ == "__main__":
    main()
