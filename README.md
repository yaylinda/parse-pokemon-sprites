# parse-pokemon-sprites
Scrape https://projectpokemon.org/ for Pokemon Sprites 

My plan is to get all the sprites for Generations 1-8 and export the data in the associated `results/json` and `results/csv` directory.

The parsed data will be exported to store the urls of each pokmeon sprite, including shiny, variation, regional stuff, etc.

You can make some tweaks to my Python code and run it locally, produce your own JSON/CSV files. 

Or you may simply take the results directory as is, and start using them in your app! I would love to see what you come up with :)

## Local Development
### Python Envrionment
```
MacOS (latest)
python 3.7.7
```

# Running Locally
```
>> pip install requirements.txt

>> python scraper.py
```

That's it! You should not have all your JSON/CSV files in the `results` directory now.  

