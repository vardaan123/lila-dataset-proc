import pandas as pd
import numpy as np
import json
from tqdm import tqdm
import argparse
import os
from collections import Counter

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--taxonomy-file', type=str, default='lila-taxonomy-mapping_release.csv')
    
    args = parser.parse_args()

    taxonomy = pd.read_csv(args.taxonomy_file)
    # print(taxonomy.columns)
    taxonomy.columns = ['dataset_name', 'original_label', 'taxonomy_level', 'scientific_name', \
       'common_name', 'taxonomy_string', 'kingdom', 'phylum', 'subphylum', \
       'superclass', 'class', 'subclass', 'infraclass', 'superorder', 'order', \
       'suborder', 'infraorder', 'superfamily', 'family', 'subfamily', 'tribe', \
       'genus', 'species', 'subspecies', 'variety']

    # TODO: change taxonomy query to original_label

    all_categories = list(set(taxonomy.scientific_name))

    print('len(all_categories) = {}'.format(len(all_categories)))

    '''
    taxonomy_level = list(taxonomy.taxonomy_level)
    taxonomy_level_freq_labellevel = Counter(taxonomy_level)
    print(taxonomy_level_freq_labellevel.most_common())
    '''

    species_categories = dict()
    genus_categories = dict()

    print(taxonomy.columns)
    i=0
    print({'species': taxonomy.columns[22], 'genus': taxonomy.columns[21], 'family': taxonomy.columns[18], 'order': taxonomy.columns[14], 'class': taxonomy.columns[10], 'phylum': taxonomy.columns[7], 'kingdom': taxonomy.columns[6]})

    for i in range(len(taxonomy)):
        scientific_name = taxonomy.iloc[i, 3]
        # print(taxonomy.iloc[i, 2])

        if taxonomy.iloc[i, 2] == 'species':
            if scientific_name in species_categories:
                if taxonomy.iloc[i, 1] not in species_categories[scientific_name]['original_label']:
                    species_categories[scientific_name]['original_label'].append(taxonomy.iloc[i, 1])
            else:
                species_categories[scientific_name] = {'original_label': [taxonomy.iloc[i, 1]], 'species': taxonomy.iloc[i, 22], 'genus': taxonomy.iloc[i, 21], 'family': taxonomy.iloc[i, 18], 'order': taxonomy.iloc[i, 14], 'class': taxonomy.iloc[i, 10], 'phylum': taxonomy.iloc[i, 7], 'kingdom': taxonomy.iloc[i, 6]}

        elif taxonomy.iloc[i, 2] == 'genus':
            if scientific_name in genus_categories:
                if taxonomy.iloc[i, 1] not in genus_categories[scientific_name]['original_label']:
                    genus_categories[scientific_name]['original_label'].append(taxonomy.iloc[i, 1])
            else:
                genus_categories[scientific_name] = {'original_label': [taxonomy.iloc[i, 1]], 'genus': taxonomy.iloc[i, 21], 'family': taxonomy.iloc[i, 18], 'order': taxonomy.iloc[i, 14], 'class': taxonomy.iloc[i, 10], 'phylum': taxonomy.iloc[i, 7], 'kingdom': taxonomy.iloc[i, 6]}

    print('len(species_categories) before = {}'.format(len(species_categories)))
    print('len(genus_categories) = {}'.format(len(genus_categories)))

    species_categories_orig = species_categories.copy()

    species_categories_remove = set()

    # goal: create a mapping from query/original_label to scientific name of species/genus
    for genus_category in genus_categories.keys():
        for species_category in species_categories.keys():
            if species_categories[species_category]['genus'] == genus_categories[genus_category]['genus']:
                # merge the species category into genus_category
                species_categories_remove.add(species_category)
                # print('merging species {} with genus {}'.format(species_category, genus_category))

    for species_category in species_categories_remove:
        species_categories.pop(species_category)

    print('len(species_categories) after = {}'.format(len(species_categories)))

    category_to_label_map = {}

    # TODO: add the species common names that are mapped to genuses.
    for species_category in species_categories_remove:
        for orig_label in species_categories_orig[species_category]['original_label']:
            category_to_label_map[orig_label] = species_categories_orig[species_category]['genus']

    for species_category in species_categories:
        for orig_label in species_categories[species_category]['original_label']:
            category_to_label_map[orig_label] = species_categories[species_category]['species']

    for genus_category in genus_categories:
        for orig_label in genus_categories[genus_category]['original_label']:
            category_to_label_map[orig_label] = genus_categories[genus_category]['genus']

    # categories are original (common) names
    # labels are scientific names

    json.dump(category_to_label_map, open('category_to_label_map.json', 'w'), indent=1)

    all_categories_valid = list(set(category_to_label_map.values()))

    label_to_id_map = {label:i for i,label in enumerate(all_categories_valid)}
    json.dump(label_to_id_map, open('label_to_id_map.json', 'w'), indent=1)

   
