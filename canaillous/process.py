import os
import pandas as pd
import re
from os.path import join, splitext
import logging
import sys
import traceback


def process_salary_line(line):
    l = line.strip()
    sa = l[:2]
    dt = l[2:10]
    compte = l[30:38]
    name = l[41:71].strip()
    rem = l[71:79].strip()
    t = l[79]
    return [sa, dt, compte, name, rem, t]


def process_salary(folder, file_name):
    logging.info('process salary for {}'.format(file_name))
    with open(join(folder, file_name)) as f:
        data = [process_salary_line(s) for s in f.readlines()]
        df = pd.DataFrame(data)
    df.to_csv(join(folder, splitext(file_name)[0] + '.csv'), sep=';', index=False, 
              header=None)
    

def process_ventes_line(line, code):
    l = line.replace('\n', '')
    dt = l[7: 15]
    c = l[35: 46].strip()
    if c.startswith('411'):
        compte = [u'41110000', c]
    else:
        compte = [c, u'']
    rib = l[46:57]
    name = l[58: 71].strip()
    rem = l[71:84].strip()
    t = l[84]
    return [code, dt] + compte + [rib, name, rem, t]


def get_code(file_name):
    if 'armagnac' in file_name.lower():
        return 'VEA'
    elif 'brascassat' in file_name.lower():
        return 'VEB'
    elif 'lafitteau' in file_name.lower():
        return 'VEL'
    

def process_ventes(folder, file_name, code):
    logging.info('process ventes for {} with code {}'.format(file_name, code))
    with open(join(folder, file_name)) as f:
        data = [process_ventes_line(s, code) for s in f.readlines()]
        df = pd.DataFrame(data)
    df.to_csv(join(folder, splitext(file_name)[0] + '.csv'), sep=';', index=False, 
             header=['JAL', 'DATE', 'COMPTE', 'TIERS', '', '', '', ''])
    return code


def process_folder(folder=None):
    if folder is None:
        folder = os.path.dirname(os.path.realpath(__file__))
    for f in os.listdir(folder):
        _, file_ext = splitext(f)
        if file_ext.lower() == '.txt':
            try:
                code = get_code(f)
                if code is None:
                    process_salary(folder, f)
                else:
                    process_ventes(folder, f, code)
            except:
                logging.error('Something went wrong wiht: {}'.format(f))
                traceback.print_exc()

def main():
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) < 2:
        logging.error('You should pass the folder where the processing should be done')
        sys.exit(1)
    folder = sys.argv[1]
    process_folder(folder)
