#!/usr/bin/env python3

import psycopg2
from psycopg2.extras import NamedTupleCursor

conn = psycopg2.connect('')

cur = conn.cursor(cursor_factory=NamedTupleCursor)

cur.execute('''
SELECT fktable,
       trim('{}' from fkcols::text) as fkcols,
       pktable,
       trim('{}' from pkcols::text) as pkcols
FROM pg_get_catalog_foreign_keys()
''')
rows = cur.fetchall()

table_columns = {}

for row in rows:
    if not table_columns.get(row.fktable):
        table_columns[row.fktable] = {}
    table_columns[row.fktable][row.fkcols] = 1
    if not table_columns.get(row.pktable):
        table_columns[row.pktable] = {}
    table_columns[row.pktable][row.pkcols] = 1

print("digraph catalog {")
print("\toverlap = scale;")
print("\tsplines = true;")
print("\tnode [shape=plain];")

for table in sorted(table_columns.keys()):
    cols = sorted(table_columns[table].keys())
    print('\t{} [label=< <table> '.format(table), end='')
    print("<tr><td><b>{}</b></td></tr> ".format(table), end='')
    for c in cols:
        print('<tr><td port="{}">{}</td></tr> '.format(c, c), end='')
    print("</table> >];")

for row in rows:
    print('\t{}:"{}" -> {}:"{}";'.format(row.fktable, row.fkcols,
                                         row.pktable, row.pkcols))

print("}")
