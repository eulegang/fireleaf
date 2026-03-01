
# fireleaf

a project to scrape game data from pokemondb.net and load into postgres for personal usage

## How to use

> [!NOTE]
> TLDR;
> Run `docker compose up -d && uv run main.py && uv run load.py`

### main.py

Scrapes pokemondb.net in respect to fire red and leaf green pokemon data
and loads the individual entries into data/pokemon/{pokemon}.json

### load.py

takes the flat files in data/pokemon/*.json and load the entries
(with moves, locations, other such things) into the postgres database
