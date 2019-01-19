# combination-template
Simple combination template engine.  
Embed the Cartesian product of combination data into the template text.  
This software is released under the MIT License, see LICENSE file.

# How to use

1. Install dependent libraries.  
```sh
$ pip install -r requirements.txt
```

2. Prepare json data and template file.  
I prepared the following sample.  
* Template format: python Template strings  
  - settings.json ... combination data sample
  - template/sample-template.S ... template text sample
* Template format: Jinja2  
  - settings.j2.json ... combination data sample
  - template/sample-template.j2.S ... template text sample

3. Run combination-template.  
```sh
$ python combination-template.py settings.json
generate OK > gen\sample-template00_func_name-combination_op1-add_op2-add_op3-add.S
generate OK > gen\sample-template01_func_name-combination_op1-add_op2-add_op3-sub.S
generate OK > gen\sample-template02_func_name-combination_op1-add_op2-add_op3-mul.S
...
# For the jinja 2 sample, it is below.
# python combination-template.py settings.j2.json
```

The result file is output to the gen directory.

# About the format of json
The required data is as follows.  
- template ... Template file path  
- output ... Output directory path  
- data ... Combination data  
- auto_id ... Include autoincrement ID in file name(option)  
- format ... For jinja 2 format, please specify jinja2, j2.  

# About the format of template
The substitutions method follows python Template strings and Jinja2.  

- [python Template strings](https://docs.python.org/3/library/string.html#template-strings)
- [Jinja2](http://jinja.pocoo.org/)

