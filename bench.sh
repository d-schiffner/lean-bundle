#!/bin/bash

for i in 10 20 40 100 200 250 500 628
do
    python3 lean_bundle/from-xapi.py --dump --limit ${i}000 --out data/bench-$1-${i}k.lean data/vigor.json
done