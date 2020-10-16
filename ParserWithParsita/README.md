# Installation
```
pip install parsita
```

# Execution 
```
python3 parser.py <flag> <filename>
```

# Show the result
```
cat <filename>.out
```

# About flags 

* `--prog` -- parse whole prolog program
* `--module` -- parse only one module
* `--relation` -- parser only one relation
* `--atom` -- parse only one atom 

Also you can do not use flags. In this case, program will use `--prog` flag