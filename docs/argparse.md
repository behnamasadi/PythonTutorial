# Command Line Arguments

```
import sys
print(sys.argv)
```

example of call: 
```
python command_line_atgv.py -n=3
```

# argparse 
The `argparse` module provides a mechanism to process command line arguments. It should always be preferred over directly processing `sys.argv` manually.

```
parser = argparse.ArgumentParser(
    'provide input and output file, -f for force conversion -o <output-dir> -i <input-dir> -f')
```
This will add a flag without parameters, that means user may or may not provide `-o`

```
parser = argparse.ArgumentParser(
    'provide input and output file, -f for force conversion -o <output-dir> -i <input-dir> -f')

parser.add_argument("-o", type=str, required=False, default="output.xml",
                    help="output file")

parser.add_argument("-i", type=str, required=True,
                    help="input file")

parser.add_argument("-f",'--force' ,required=False,
                    action='store_true', help="force conversion")
```
Now to parse the parameters and use them:
```
args = parser.parse_args()


if args.i:
    print("input file is: ", args.i)
if args.force:
    print("force conversion is:", args.force)
```

In `argparse`, the `action='store_true'` parameter is used to indicate that the corresponding command-line flag/option should store the value `True` if it's provided, and `False` otherwise.

Here's a breakdown of how it works:

1. **When the Flag is Provided**: If the command-line flag associated with `action='store_true'` is specified when the script is run, the corresponding attribute in the `args` object (returned by `parser.parse_args()`) will be set to `True`.

2. **When the Flag is Not Provided**: If the command-line flag is not specified when the script is run, the attribute will be set to `False`.

It's a convenient way to handle boolean flags without needing to provide a value.

You can run the script as:
```
python index.py -f -o out.xml -i input.txt
```


Refs: [1](https://docs.python.org/3/library/argparse.html#module-argparse)
