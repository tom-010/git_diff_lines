#!/bin/bash

rm dist -r 2> /dev/null
python3 setup.py sdist bdist_wheel
twine upload dist/*