import json
import sys
import os
import re

directories = ('blazeandcave', 'minecraft')  # directories > tabs > advancements
technical = ('technical', 'bacap')  # tabs that should not be shown

"""
Copy your advancements .json file into a folder with this script and rename it as "advs.json".
It is located in advancements folder in your world. The path most likely looks like this:
"C:/Users/USERNAME/AppData/Roaming/.minecraft/saves/WORLD_NAME/advancements"
Then copy your advancements pack into the same folder.
"""
with open('a61e9722-5113-353f-9a47-19fb9a6aa9b0.json') as advs:

    try:
        advs = json.load(advs)
    except json.decoder.JSONDecodeError:
        sys.exit('Wrong file.')

    undone = []  # advancements with only one requirement
    incomplete = []  # advancements with multiple requirements, you can check what is left to do

    for directory in directories:
        for tab in os.listdir('data/' + directory + '/advancements'):
            if tab not in technical:
                for adv_file in os.listdir('data/' + directory + '/advancements/' + tab):
                    adv = directory + ':' + tab + '/' + adv_file[:-5]
                    if adv not in advs:
                        undone.append(adv)
                    elif adv != 'DataVersion'\
                            and 'recipes' not in adv\
                            and not advs[adv]['done']\
                            and tab not in technical:
                        incomplete.append(adv)

    print('Undone:')
    for u in sorted(undone):
        print(u)

    print('\nIncomplete:')
    for i in sorted(incomplete):
        print(i)

    while 'my guitar gently weeps':
        selected = input('\nChoose incomplete advancement from the list above to see requirements: ')
        try:
            directory, tab, adv_name = re.split('[:/]', selected)
            with open('data/' + directory + '/advancements/' + tab + '/' + adv_name + '.json') as advancement:
                advancement = json.load(advancement)
                requirements = set(advancement['criteria'])
            print(*sorted([criteria for criteria in requirements - set(advs[selected]['criteria'])]), sep='\n')
        except KeyError:
            print('\nWrong input. You should just copy and paste name of the advancement '
                  'e.g. blazeandcave:bacap/advancement_legend')
