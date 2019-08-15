# -*- coding: utf-8 -*-
import os
import pandas as pd
import re
from os.path import join, splitext
import logging
import sys
import traceback


def process_salary_line(line):
    l = line.decode('ISO-8859-1').strip()
    sa = l[:2]
    dt = pd.to_datetime(l[2:10]).date().strftime('%d/%m/%Y')
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
              header=None, encoding='utf-8')
    

def process_ventes_line(line, code):
    l = line.decode('ISO-8859-1').replace('\n', '')
    dt = pd.to_datetime(l[7: 15]).date().strftime('%d/%m/%Y')
    c = l[35: 46].strip()
    axe = ''
    if c.startswith('411'):
        compte = [u'41110000', c]
    else:
        compte = [c, u'']
        axe = get_axe(code)
    rib = l[46:57]
    name = l[58: 71].strip()
    rem = l[71:84].strip()
    t = l[84]
    return [code, dt] + compte + [rib, name, rem, t, axe]


def get_code(file_name):
    if 'armagnac' in file_name.lower():
        return 'VEA'
    elif 'brascassat' in file_name.lower():
        return 'VEB'
    elif 'lafitteau' in file_name.lower():
        return 'VEL'
    elif 'laffiteau' in file_name.lower():
        return 'VEL'
    
def get_axe(code):
    if code == 'VEA':
        return '30 ARMAGNAC'
    elif code =='VEB':
        return '10 BRASCASSAT'
    elif code == 'VEL':
        return '20 LAFFITEAU'


def process_ventes(folder, file_name, code):
    logging.info('process ventes for {} with code {}'.format(file_name, code))
    with open(join(folder, file_name)) as f:
        data = [process_ventes_line(s, code) for s in f.readlines()]
        df = pd.DataFrame(data)
    df.to_csv(join(folder, splitext(file_name)[0] + '.csv'), sep=';', index=False, 
             header=['Journal', 'Date', 'Compte', 'Tiers', 'Réference', 'Libellé', 'Montant', 'Sens', 
             'Axe Etablissement'], 
             encoding='utf-8')
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
