py_expand_urls
---

Expand shortened URLs present in a text file.

```
usage: expand_urls [-h] [-o OUTPUT] [-e ENCODING] [-v] input

positional arguments:
  input                 input file name

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output file name
  -e ENCODING, --encoding ENCODING
                        file encoding (default: utf-8)
  -v, --verbose         print expanded URLs
```

Tested with python3-requests library version 2.23.0.