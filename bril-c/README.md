# Install and Build

```
pip install -r requirements.txt
chmod +x build.sh
./build.sh
```

See [Python runtime targets](https://github.com/antlr/antlr4/blob/master/doc/python-target.md) for more information.

# Simple Example

Try parsing an example:

```
python ./c/driver.py c/examples/simple.c

# Use debug mode to print syntax tree
python ./c/driver.py -D c/examples/simple.c

# Check coverted bril program
python ./c/driver.py c/examples/simple.c | bril2txt

# Run coverted bril program
python ./c/driver.py c/examples/simple.c | brili -p
```

# Test

```
chmod +x ./test_c_vs_bril.sh
./test_c_vs_bril.sh ./tests/
```
