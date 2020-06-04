import csv
import json
import os
import requests

###############################################################################
# Global Constants Definitions
###############################################################################

# key   -> pokemon generation number
# value -> projectpokemon sprite page for that gen
SPRITE_PAGES = {
    '1': 'https://projectpokemon.org/docs/spriteindex_148/3d-models-generation-1-pok%C3%A9mon-r90/',
    '2': 'https://projectpokemon.org/docs/spriteindex_148/3d-models-generation-2-pok%C3%A9mon-r91/',
    '3': 'https://projectpokemon.org/docs/spriteindex_148/3d-models-generation-3-pok%C3%A9mon-r92/',
    '4': 'https://projectpokemon.org/docs/spriteindex_148/3d-models-generation-4-pok%C3%A9mon-r93/',
    '5': 'https://projectpokemon.org/docs/spriteindex_148/3d-models-generation-5-pok%C3%A9mon-r94/',
    '6': 'https://projectpokemon.org/docs/spriteindex_148/3d-models-generation-6-pok%C3%A9mon-r95/',
    '7': 'https://projectpokemon.org/docs/spriteindex_148/3d-models-generation-7-pok%C3%A9mon-r96/',
    '8': 'https://projectpokemon.org/docs/spriteindex_148/3d-models-generation-8-pok%C3%A9mon-r123/',
}

# For results directories
RESULTS_DIR = 'results'
RESULT_FILE_TYPES = ['csv', 'json']


###############################################################################
# Functions
###############################################################################


def get_html(url):
    print('\tGetting HTML from %s' % url)
    r = requests.get(url)
    return r.text


def parse_html(generation, html):
    data = []

    lines = html.splitlines()
    print('\tParsing %d lines of HTML...' % len(lines))

    for line in lines:
        line = line.strip()

        # Only interested in lines of these format:
        #   <img alt="bulbasaur.gif" src="https://projectpokemon.org/images/normal-sprite/bulbasaur.gif">
        #   <img align="middle" alt=" " src="https://projectpokemon.org/images/sprites-models/swsh-normal-sprites/grookey.gif">

        if line.startswith('<img') and 'src="https://projectpokemon.org/images/' in line and line.endswith('.gif">'):
            datum = {}

            datum['generation'] = generation

            if '/images/sprites-models/swsh-' in line:
                pokemon_name = line.split('-sprites/')[1].split('.gif')[0]
            elif '/images/sprites-models/' in line:
                pokemon_name = line.split('<img alt="')[1].split('.gif')[0]
            else:
                pokemon_name = line.split('-sprite/')[1].split('.gif')[0]

            pokemon_name_split = pokemon_name.split('-')

            if len(pokemon_name_split) > 1:
                datum['pokemon_variant'] = ' '.join([x.capitalize() for x in pokemon_name_split[1:]])
            else:
                datum['pokemon_variant'] = 'None'

            datum['pokemon_name'] = pokemon_name_split[0].capitalize()

            if 'swsh-' in line:
                sprite_type = line.split('https://projectpokemon.org/images/sprites-models/swsh-')[1].split('-sprites/')[0]
                datum['sprite_type'] = sprite_type.capitalize()
            elif 'sprites-models' in line:
                datum['sprite_type'] = line.split('/sprites-models/')[1].split('-back')[0].capitalize()
            else:
                sprite_type = line.split('https://projectpokemon.org/images/')[1].split('-sprite/')[0]
                datum['sprite_type'] = sprite_type.capitalize()

            datum['sprite_url'] = line.split('src="')[1].split('">')[0]

            data.append(datum)

    print('\tParsed %d sprites' % len(data))

    return data


def export_to_csv(filename_template, generation, data):
    filename = filename_template % ('csv', generation, 'csv')

    print('\tWriting data to CSV file %s' % filename)

    with open(filename, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=['generation','pokemon_variant','pokemon_name','sprite_type','sprite_url'])                                               
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def export_to_json(filename_template, generation, data):
    filename = filename_template % ('json', generation, 'json')

    print('\tWriting data to JSON file %s' % filename)

    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)


###############################################################################
# Main
###############################################################################


def main():

    # Create result directories if they don't already exist

    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)

    for extension in RESULT_FILE_TYPES:
        if not os.path.exists(RESULTS_DIR + '/' + extension):
            os.makedirs(RESULTS_DIR + '/' + extension)

    # Parse sprites for each generation defined in SPRITE_PAGES

    for generation in SPRITE_PAGES:

        sprite_page_url = SPRITE_PAGES[generation]
        print('\nProcessing sprites for Pokemon Generation %s...' % generation)

        html = get_html(sprite_page_url)
        data = parse_html(generation, html)
        
        filename_template = RESULTS_DIR + '/%s/generation_%s.%s'
        export_to_csv(filename_template, generation, data)
        export_to_json(filename_template, generation, data)
    
    print('\nDone!')


if __name__ == "__main__":
    main()