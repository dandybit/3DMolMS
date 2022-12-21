'''
Date: 2022-12-09 17:38:44
LastEditors: yuhhong
LastEditTime: 2022-12-09 18:14:24
'''
import argparse
import pandas as pd
from pprint import pprint

from rdkit import Chem
# ignore the warning
from rdkit import RDLogger 
RDLogger.DisableLog('rdApp.*')



def get_atom_symbols(smiles):
    mol = Chem.MolFromSmiles(smiles)
    atom_syb = set()

    for i in range(mol.GetNumAtoms()):
        atom_syb.add(mol.GetAtomWithIdx(i).GetSymbol())
    return list(atom_syb)

def remove_for_rare_atom(smiles, keep_atoms):
    mol = Chem.MolFromSmiles(smiles)
    if mol == None:
        return False
        
    for i in range(mol.GetNumAtoms()):
        a = mol.GetAtomWithIdx(i).GetSymbol()
        if a not in keep_atoms:
            return False
    return True


KEEP_INST = ['QTOF']
KEEP_ATOM = ['C', 'O', 'N', 'H', 'P', 'S', 'F', 'Cl', 'B', 'Br', 'I']
KEEP_PRE_TYPE = ['M+H', 'M-H', 'M+H-H2O', 'M+Na', 'M+2H']

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Preprocess the Data')
    parser.add_argument('--input', type=str, default = '',
                        help='path to input data')
    parser.add_argument('--output', type=str, default = '',
                        help='path to output data')
    args = parser.parse_args()

    # load the data
    df = pd.read_csv(args.input)
    print('Load {} data from {}'.format(len(df), args.input))

    # check columns
    col_names = [col for col in df.columns]
    assert 'ID' in col_names and \
            'SMILES' in col_names and \
            'Precursor_Type' in col_names and \
            'Source_Instrument'in col_names and \
            'Collision_Energy' in col_names
    
    # filter the data frame
    print("\nPlease check the conditions!")
    conditions = {'Keep Instruments': KEEP_INST, 
                    'Atom Types': KEEP_ATOM,
                    'Adduct Types': KEEP_PRE_TYPE}
    pprint(conditions, compact=True)

    df = df[df['Precursor_Type'].isin(KEEP_PRE_TYPE) & \
            df['Source_Instrument'].isin(KEEP_INST)]
    # df['atom_types'] = df.apply(lambda row: get_atom_symbols(row['SMILES']), axis=1)
    df = df[df.apply(lambda row: remove_for_rare_atom(row['SMILES'], KEEP_ATOM), axis=1)]
    df.to_csv(args.output, index=False)
    print('\nOutput {} data into {}'.format(len(df), args.output))