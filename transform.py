#!/usr/bin/env python3

import csv
from functools import reduce

from amo.builders import *
from amo.utilities import timer_decorator, read_json, \
    comprehend_lead_custom_fields


# The problem is that when now we have a lot of custom fields
# which will cause stack overflow, so it's better to write them
# down to a csv file row by row.


@timer_decorator
def transform_entity(entity, amo):
    entity_file = open(
        f'temp_data/{amo}_{entity}_tmp.json', 'r',
        encoding='utf-8'
    )

    read_file = read_json(entity_file)

    build_entity = 'build_' + entity + '_tuple'

    with open(f'temp_data/{amo}_{entity}.csv', 'w', newline='') as f:
        # Create a CSV DictWriter

        builder = globals()[build_entity]

        fields = builder(read_file[0])._fields # Initial fields we put

        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader() # write the initial fields

        for entry in read_file:

            # First build the named tuple:
            built = builder(entry)

            # Now extract the custom fields:
            comprehended = comprehend_lead_custom_fields(built)

            # Check if the fields in new tuple are different
            # from original tuple:
            if fields != comprehended._fields:
                fields = comprehended._fields
                writer.fieldnames = fields
                # Write the data row
            writer.writerow(comprehended._asdict())
