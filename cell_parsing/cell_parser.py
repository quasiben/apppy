from IPython.nbformat import current as nbf

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
import re

p = re.compile('# In\[\d*\]')

def parse_into_cells(py_file,debug=True):
    if debug:
        log.setLevel(logging.DEBUG)

    with open(py_file, 'r') as f:

        in_cell = False
        cell = ''
        count = 0

        #must read in entire file to handle yielding
        data = f.readlines()

        for line in data:
            #check line for string # In[012...]
            if  p.match(line):

                # If #cell start new cell
                if in_cell==True:
                    log.debug(cell)
                    yield cell.strip()
                    cell = ''

                in_cell = True

            else:
                if in_cell:
                    cell += line

    if cell != '':
        log.debug(cell.strip())
        yield cell.strip()


def convert(py_file, ipynb_file):

    #create new notebook
    nb = nbf.new_notebook()
    cells = list(map(nbf.new_code_cell,parse_into_cells(py_file)))
    nb['worksheets'].append(nbf.new_worksheet(cells=cells))

    with open(ipynb_file, 'w') as f:
        nbf.write(nb, f, 'ipynb')




if __name__ == "__main__":
    parse_into_cells('./test_parse.py', debug=True)
    convert('test_parse.py', 'test_parse.ipynb')
