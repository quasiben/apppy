'''
Utility functions for marking blocks for code to be translated into:
1) cells for an ipython notebook
2) files exported to /tmp/func1.py

Feature 1) should be the missing piece for a bidirectional transport of
an ipython notebook to a python file and a python file to an ipython notebook
.

Feature 2) is convenient especially when you want to minimize a block of code
in an ipython cell. For example

#to_file _filename.py
def func():
    a
    b
    c

Can now be loaded in an ipython cell like so

%run /tmp/_func1.py

'''

from IPython.nbformat import current as nbf

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
import re
import sys

#cell block marks
p = re.compile('# In\[\d*\]')
line_conds = ['#cell','#to_file']

file_type = 'file'
cell_type = 'cell'

def parse_blocks(py_file,debug=False):
    if debug:
        log.setLevel(logging.DEBUG)

    with open(py_file, 'r') as f:

        in_cell = False
        cell = ''
        count = 0

        #must read in entire file to handle yielding
        data = f.readlines()

        for line in data:
            # log.debug(line)
            #check line for string # In[012...]
            #chekc line for #cell
            #check line for to_file
            try:

                if p.match(line) or line.split()[0] in line_conds:
                    # If #cell start new cell
                    if in_cell==True:
                        log.debug(cell)

                        t,l = line_type
                        yield (cell.strip(),t,l)
                        cell = ''

                    if 'to_file' in line:
                        line_type = (file_type,line)
                    else:
                        line_type = (cell_type,line)

                    in_cell = True

                else:
                    if in_cell:
                        cell += line
            except IndexError as e:
                #skip blank lines
                pass

    #grab last cell
    if cell != '':
        log.debug(cell.strip())
        t,l = line_type
        yield (cell.strip(),t,l)


def convert(py_file, ipynb_file):
    cells = []
    imports = '' #needed for each file

    for cell, line_type, line in parse_blocks(py_file):
        if line_type == file_type:
            #write cell to file
            try:
                fname = line.split()[1]
            except:
                raise Exception("Markdown for file output must be the "
                                +"following format\n#to_file filename.py: "
                                +"{}\n".format(line))
                sys.exit(0)

            with open(fname,'w') as f:
                f.write(cell)
                new_cell = "%run {}".format(fname)
                ipynb_cell = nbf.new_code_cell(new_cell)
                cells.append(ipynb_cell)

        else:
            #convert cell to ipynb cell
            ipynb_cell = nbf.new_code_cell(cell)
            cells.append(ipynb_cell)

    #create new notebook
    nb = nbf.new_notebook()
    nb['worksheets'].append(nbf.new_worksheet(cells=cells))

    with open(ipynb_file, 'w') as f:
        nbf.write(nb, f, 'ipynb')




if __name__ == "__main__":
    # parse_blocks('./test_parse.py', debug=True)
    # convert('test_parse.py', 'parsed_test.ipynb')
    convert('test_parse_file.py', 'parsed_test_file.ipynb')
