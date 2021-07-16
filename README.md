# Generate schema diagram of PostgreSQL system catalogs using Graphviz

requires PostgreSQL 14+

example invocation

```sh
export PGPORT=65432  # etc.

python3 ./pgcatviz.py | dot -Ksfdp -Tsvg -o catalog.svg
```
