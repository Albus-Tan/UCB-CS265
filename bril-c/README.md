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
python ./core/driver.py core/examples/simple.c

# Use debug mode to print syntax tree
python ./core/driver.py -D core/examples/simple.c

# Check coverted bril program
python ./core/driver.py core/examples/simple.c | bril2txt

# Run coverted bril program
python ./core/driver.py core/examples/simple.c | brili -p
```

# Test

```
chmod +x ./test_c_vs_bril.sh
./test_c_vs_bril.sh ./tests/
```
