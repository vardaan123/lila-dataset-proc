# lila-dataset-proc

Code to process LILA datasets into a joint label space

## Data download
Download `lila-taxonomy-mapping_release.csv` from https://lila.science/public/lila-taxonomy-mapping_release.csv

## Processing
```
python canonicalize_lila_dataset.py
```
**Output**:

`category_to_label_map`: mapping from original label to canonical taxonomic level scientific name (species, genus, etc.)

`label_to_id_map`: mapping from all category labels to label canonical ID.
