#!/usr/bin/env python
"""
Author Marcin Magnus mmagnus@stanford.edu // magnus@genesilico.pl
"""
AMINOACID_CODES = ["ALA", "ARG", "ASN", "ASP", "CYS", "GLU", "GLN", "GLY",
            "HIS", "ILE", "LEU", "LYS", "MET", "PHE", "PRO", "SER", "THR",
            "TRP", "TYR", "VAL"]
RES = ['DA', 'DG', 'DT', 'DC']
RES += ['A', 'G', 'U', 'C']

RESS = ['A', 'C', 'G', 'U', 'ADE', 'CYT', 'GUA', 'URY', 'URI', 'U34', 'U31', 'C31', '4SU', 'H2U', 'QUO', 'G7M', '5MU', '5MC', 'PSU', '2MG', '1MG', '1MA', 'M2G', '5BU', 'FHU', 'FMU', 'IU', 'OMG', 'OMC', 'OMU', 'A2M', 'A23', 'CCC', 'I'] + ['RC', 'RU', 'RA', 'RG', 'RT']
#DNA = ['DA', 'DG', 'DT', 'DC']
#RNA = ['A', 'G', 'U', 'C']
IONS = ['NA', 'MG']
HYDROGEN_NAMES = ["H", "H5'", "H5''", "H4'", "H3'", "H2'", "HO2'", "H1'", "H3", "H5", "H6", "H5T", "H41", "1H5'", 
                          "2H5'", "HO2'", "1H4", "2H4", "1H2", "2H2", "H1", "H8", "H2", "1H6", "2H6",
                          "HO5'", "H21", "H22", "H61", "H62", "H42", "HO3'", "1H2'", "2HO'", "HO'2", "H2'1" , "HO'2", "HO'2",
                          "H2", "H2'1", "H1", "H2", "1H5*","2H5*", "H4*", "H3*", "H1*", "1H2*", "2HO*", "1H2", "2H2", "1H4", "2H4", "1H6", "2H6", "H1", "H2", "H3", "H5", "H6", "H8", "H5'1", "H5'2"]

class StrucFile:
    def __init__(self, fn):
        self.fn = fn
    
        self.report = []
        self.report.append('The RNAStrucFile report: %s ' % fn) 

        self.mol2_format = False

        self.lines = []
        lines = open(fn).read().strip().split('\n')
        for l in lines:
            if l.startswith('MODEL'):
                raise Exception('Please select only one model before using this program!')
            if l.startswith('ATOM') or l.startswith('HETATM') or l.startswith('TER') or l.startswith('END'):
                self.lines.append(l.strip())
            if l.startswith("@<TRIPOS>"):
                self.mol2_format = True
                self.report.append('This is mol2 format')

        self.res = self.get_resn_uniq()

    def is_it_pdb(self):
        if len(self.lines):
            return True
        else:
            return False

    def is_mol2(self):
        """Return true if is_mol2 (based on the presence of "@<TRIPOS>" during __init__.
        """
        return self.mol2_format

    def is_amber_like(self):
        """Use self.lines and check if there is XX line
        """
        for l in self.lines:
            if l.startswith('ATOM') or l.startswith('HETATM') :
                rn = l[17:20]
                if rn in ['RU5', 'RC5', 'RA5', 'RT5', 'RG5']:
                    self.report.append('This is amber-like format')
                    return True
        return False

    def mol2toPDB(self, outfn=""):
        try:
            import pybel
        except ImportError:
            print 'pybel is needed for mol2 to pdb convertion'
            sys.exit(1)

        if not outfn:
            outfn = self.fn.replace('.mol2', '.pdb')
            
        for mol in pybel.readfile("mol2", self.fn):
            mol.write("pdb", outfn, overwrite=True)

        print 'outfn: ', outfn
        self.report.append('  Converted from mol2 to PDB')
        return outfn

    def get_no_lines(self):
        return len(self.lines)

    def get_text(self):
        txt = ''
        for l in self.lines:
            txt += l.strip() + '\n'
        return txt

    def get_chain(self, chain_id='A'):
        txt = ''
        for l in self.lines:
            if l.startswith('ATOM') or l.startswith('HETATM') :
                if l[21] == chain_id:
                    txt += l.strip() + '\n'
        txt += 'TER'
        return txt

    def get_resn_uniq(self):
        res = set()
        for l in self.lines:
            r = l[17:20].strip().upper()
            res.add(r)
        return res

    def check_res_if_std_na(self):
        wrong = []
        
        for r in self.res:
            if r not in RES:
                wrong.append(r)
        return wrong

    def get_seq(self):
        seq = ''
        curri = int(self.lines[0][22:26])
        seq = self.lines[0][19]
        for l in self.lines:
            if l.startswith('ATOM') or l.startswith('HETATM') :
                resi = int(l[22:26])
                if curri != resi:
                    seq += l[19]
                    curri = resi
        return seq

    def detect_file_format(self):
        pass
    
    def detect_molecule_type(self):
        aa = []
        na = []
        for r in self.res:
            if r in AMINOACID_CODES:
                aa.append(r)
            if r in RESS:
                na.append(r)            

        aa = float(len(aa)) / len(self.res)
        na = float(len(na)) / len(self.res)

        if aa == 0 and na == 0:
            return 'error'
        if aa > na:
            return '>protein< vs na', aa, na
        else:
            return 'protein vs >na<', aa, na

    def get_head(self):
        return '\n'.join(self.lines[:5])

    def get_tail(self):
        return '\n'.join(self.lines[-5:])

    def get_preview(self):
        t = '\n'.join(self.lines[:5])
        t += '\n-------------------------------------------------------------------\n'
        t += '\n'.join(self.lines[-5:])
        return t

    def remove_hydrogen(self):
        lines = []
        for l in self.lines:
            if l[77:79].strip() == 'H':
                continue
            if l[12:16].strip() in HYDROGEN_NAMES:
            #if l[12:16].strip().startswith('H'):
                continue
            else:
                #print l[12:16]
                lines.append(l)
        self.lines = lines

    def remove_water(self):
        """Remove HOH and TIP3"""
        lines  = []
        for l in self.lines:
            if l[17:21].strip() in ['HOH', 'TIP3', 'WAT']:
                continue
            else:
                lines.append(l)
        self.lines = lines

    def remove_ion(self):
        """
    TER    1025        U A  47                                                      
    HETATM 1026 MG    MG A 101      42.664  34.395  50.249  1.00 70.99          MG  
    HETATM 1027 MG    MG A 201      47.865  33.919  48.090  1.00 67.09          MG 
        """
        lines = []
        for l in self.lines:
            element = l[76:78].strip().upper()
            element2 = l[17:20].strip().upper()
            if element in IONS:
                continue
            if element2 in IONS:
                continue
            else:
                lines.append(l)
        self.lines = lines

    def fixU__to__U(self):
        lines = []
        for l in self.lines:
            if l.startswith('ATOM') or l.startswith('HETATM') :
                rn = l[17:20]
                rn = rn.replace('G  ', '  G')
                rn = rn.replace('U  ', '  U')
                rn = rn.replace('C  ', '  C')
                rn = rn.replace('A  ', '  A')
                l = l[:16] + ' ' + rn + ' ' + l[21:]
            #print l.strip()
            #print l2
            #l = l.replace(' U   ', '   U ')
            #l = l.replace(' G   ', '   G ')
            #l = l.replace(' A   ', '   A ')
            #l = l.replace(' C   ', '   C ')
            lines.append(l)
        print 'fixU__to__U OK'
        self.report.append('  Fix: U__ -> __U')
        self.lines = lines

    def resn_as_dna(self):
        lines = []
        for l in self.lines:
            if l.startswith('ATOM') or l.startswith('HETATM') :
                #print l
                nl = l.replace( 'DA5', ' DA') # RA should be the last!!!!
                nl = nl.replace('DA3', ' DA')
                nl = nl.replace(' DA', ' DA')
                nl = nl.replace(' rA', ' DA')

                nl = nl.replace('DC5', ' DC')
                nl = nl.replace('DC3', ' DC')
                nl = nl.replace(' DC', ' DC')
                nl = nl.replace(' rC', ' DC')

                nl = nl.replace('DG5', ' DG')
                nl = nl.replace('DG3', ' DG')
                nl = nl.replace(' DG', ' DG')
                nl = nl.replace(' rG', ' DG')

                nl = nl.replace('DU5', ' DU')
                nl = nl.replace('DU3', ' DU')
                nl = nl.replace(' DU', ' DU')
                nl = nl.replace(' rU', ' DU')

                nl = nl.replace('DT5', ' DT')
                nl = nl.replace('DT3', ' DT')
                nl = nl.replace(' DT', ' DT')
                nl = nl.replace(' rT', ' DT')

                nl = nl.replace('C5M', 'C7 ')

                if l[17:20].strip() == 'G':
                    nl = nl[:17] + ' DG' + nl[20:]

                if l[17:20].strip() == 'C':
                    nl = nl[:17] + ' DC' + nl[20:]

                if l[17:20].strip() == 'T':
                    nl = nl[:17] + ' DT' + nl[20:]

                if l[17:20].strip() == 'U':
                    nl = nl[:17] + ' DU' + nl[20:]

                if l[17:20].strip() == 'A':
                    nl = nl[:17] + ' DA' + nl[20:]

                lines.append(nl)
            if l.startswith("END") or l.startswith("TER"):
                lines.append(l)

        print 'resn_as_dna'
        self.report.append('  resn_as_dna')
        self.lines = lines

    def fix_O_in_UC(self):
        """.. warning: remove RU names before using this function"""
        lines = []
        for l in self.lines:
            #if l[12:16].strip() in 
            #if l[12:16].strip().startswith('H'):
            nl = l.replace('O     U',
                           'O2    U')
            nl =nl.replace('O     C',
                           'O2    C')
            lines.append(nl)
        self.lines = lines


    def fix_op_atoms(self):
        lines = []
        for l in self.lines:
            nl = l.replace('*', '\'')
            nl = nl.replace('O1P', 'OP1')
            nl = nl.replace('O2P', 'OP2')
            nl = nl.replace('O3P', 'OP3')
            lines.append(nl)
        self.lines = lines

    def get_report(self):
        return '\n'.join(self.report)


    def is_rna(self):
        wrong = []
        for r in self.res:
            if r.upper().strip() in ['RC', 'RU', 'RA', 'RG', 'RT']:
                if r not in wrong_res:
                    wrong_res.append(r)
        return wrong_res

    def check_res_if_std_dna(self):
        wrong_res = []
        for r in self.res:
            if r.upper().strip() in ['A', 'T', 'C', 'G']:
                if r not in wrong_res:
                    wrong_res.append(r)
        return wrong_res

    def check_res_if_supid_rna(self):
        wrong_res = []
        for r in self.res:
            if r.upper().strip() in ['RC', 'RU', 'RA', 'RG', 'RT']:
                if r not in wrong_res:
                    wrong_res.append(r)
        return wrong_res

    def is_rna(self):
        for r in self.res:
            if r.upper().strip() in ['RC', 'RU', 'RA', 'RG', 'RT']:
                if r not in wrong_res:
                    wrong_res.append(r)
        return wrong_res

    def renum_atoms(self):
        """Renum atoms, from 1 to X for line; ATOM/HETATM"""
        lines = []
        c = 1
        for l in self.lines:
            nl = l[:6] + str(c).rjust(5) + l[11:]
            c += 1
            lines.append(l)
        self.lines = lines

    def fix_resn(self):
        lines = []
        for l in self.lines:
            nl = l.replace( 'RA5', '  A') # RA should be the last!!!!
            nl = nl.replace('RA3', '  A')
            nl = nl.replace('ADE', '  A')
            nl = nl.replace(' RA', '  A')
            nl = nl.replace(' rA', '  A')

            nl = nl.replace('RC5', '  C')
            nl = nl.replace('RC3', '  C')
            nl = nl.replace('CYT', '  C')
            nl = nl.replace(' RC', '  C')
            nl = nl.replace(' rC', '  C')

            nl = nl.replace('RG5', '  G')
            nl = nl.replace('RG3', '  G')
            nl = nl.replace('GUA', '  G')
            nl = nl.replace(' RG', '  G')
            nl = nl.replace(' rG', '  G')

            nl = nl.replace('RU5', '  U')
            nl = nl.replace('RU3', '  U')
            nl = nl.replace('URA', '  U')  
            nl = nl.replace(' RU', '  U')
            nl = nl.replace(' rU', '  U')

            nl = nl.replace('RT5', '  T')
            nl = nl.replace('RT3', '  T')
            nl = nl.replace('THY', '  T')  
            nl = nl.replace(' RT', '  T')
            nl = nl.replace(' rT', '  T')
            
            lines.append(nl)
            
        self.lines = lines

    def check_res_if_std_prot(self):
        wrong = []
        for r in self.res:
            if r not in AMINOACID_CODES:
                wrong.append(r)
        return wrong


    def write(self, outfn):
        """Write (and END file")"""
        f = open(outfn, 'w')
        for l in self.lines:
            f.write(l + '\n')
        if not l.startswith('END'):
            f.write('END')
        f.close()
        print 'Write %s' % outfn

def start(): pass

if '__main__' == __name__:
    fn = 'input/image'
    print 'fn:', fn
    struc = StrucFile(fn)
    print ' pdb?:', struc.is_it_pdb()
    print ' # atoms:', struc.get_no_lines()

    fn = 'input/na.pdb'
    s = StrucFile(fn)
    print s.detect_molecule_type()
    #res = get_all_res(na)
    #print 'what is?', what_is(res)
    #print res
    print 'non standard:', s.check_res_if_std_na()
    print 'is protein:', s.detect_molecule_type()

    fn = 'input/prot.pdb'
    s = StrucFile(fn)
    print 'non standard:', s.check_res_if_std_prot()
    print 'is protein:',  s.detect_molecule_type()


    fn = 'input/rna-ru.pdb'
    s = StrucFile(fn)
    print 'non standard:', s.check_res_if_supid_rna()
    print 'is protein:', s.detect_molecule_type()

    fn = 'input/na_highAtomNum.pdb'
    print fn
    s = StrucFile(fn)
    s.renum_atoms()
    s.write('output/na_highAtomNum.pdb')

    fn = 'input/na_solvet_old_format.pdb'
    print fn
    s = StrucFile(fn)
    s.fix_op_atoms()
    s.remove_hydrogen()
    s.remove_ion()
    s.remove_water()
    s.write('output/na_solvet_old_format.pdb')

    fn = 'input/na_solvet_old_format.pdb'
    print fn
    s = StrucFile(fn)
    s.fix_resn()
    s.remove_hydrogen()
    s.remove_ion()
    s.remove_water()
    s.write('output/na_solvet_old_format.pdb')

    #fn = 'input/na_solvet_old_format__.pdb'
    #s = StrucFile(fn)
    #s.fix_resn()
    #s.remove_hydrogen()
    #s.remove_ion()
    #s.remove_water()
    #s.renum_atoms()
    #s.fix_op_atoms()
    #s.write('output/na_solvet_old_format__.pdb')


    fn = 'input/1xjr.pdb'
    s.fix_resn()
    s.remove_hydrogen()
    s.remove_ion()
    s.remove_water()
    s.renum_atoms()
    s.fix_op_atoms()
    s.write('output/1xjr.pdb')

    fn = 'input/decoy0165_amb.pdb'
    print fn
    s = StrucFile(fn)
    s.fix_resn()
    s.remove_hydrogen()
    s.remove_ion()
    s.remove_water()
    s.renum_atoms()
    s.fix_O_in_UC()
    s.fix_op_atoms()
    s.write('output/decoy0165_amb_clx.pdb')

    fn = 'input/farna.pdb'
    print fn
    s = StrucFile(fn)
    s.fix_resn()
    s.remove_hydrogen()
    s.remove_ion()
    s.remove_water()
    s.fix_op_atoms()
    s.renum_atoms()
    s.write('output/farna.pdb')

    fn = 'input/farna.pdb'
    print fn

    r = StrucFile(fn)
    print r.is_mol2()

    if True:
        print '================================================'
        print "input/1xjr_clx_fChimera_noIncludeNumbers.mol2"
        r = StrucFile("input/1xjr_clx_fChimera_noIncludeNumbers.mol2")
        print r.is_mol2()
        r.mol2toPDB('/tmp/x.pdb')

        r = StrucFile('/tmp/x.pdb')
        print r.get_report()
        r.fix_resn()
        r.remove_hydrogen()
        r.remove_ion()
        r.remove_water()
        r.fix_op_atoms()
        r.renum_atoms()
        r.fixU__to__U()
        r.write("output/1xjr_clx_fChimera_noIncludeNumbers.mol2")

    if True:
        r = StrucFile("input/2du3_prot_bound.mol2")
        print r.is_mol2()
        outfn = r.mol2toPDB()
        print r.get_report()

    print '================================================'
    fn = "input/3e5fA-nogtp_processed_zephyr.pdb"
    r = StrucFile(fn)
    print r.is_mol2()
    #outfn = r.mol2toPDB()
    print r.is_amber_like()
    print r.get_report()

    print r.get_preview()

    r.fix_resn()

    print r.get_preview()

    r.remove_hydrogen()
    r.remove_ion()
    r.remove_water()
    #renum_atoms(t, t)
    #fix_O_in_UC(t, t)
    #fix_op_atoms(t, t)
    r.write('output/3e5fA-nogtp_processed_zephyr.pdb')

    print
    fn = "input/1xjr_clx_charmm.pdb"
    print fn
    s = StrucFile(fn)
    s.fix_resn()
    s.remove_hydrogen()
    s.remove_ion()
    s.remove_water()
    s.write('output/1xjr_clx_charmm.pdb')

    #renum_atoms(t, t)
    #fix_O_in_UC(t, t)
    #fix_op_atoms(t, t)

    print
    fn = "input/dna_fconvpdb_charmm22.pdb"
    print fn
    r = StrucFile(fn)
    r.get_preview()
    r.resn_as_dna()
    r.remove_hydrogen()
    r.remove_ion()
    r.remove_water()
    r.fix_resn()
    print r.get_head()
    print r.get_tail()
    print r.get_preview()
    r.write("output/dna_fconvpdb_charmm22.pdb")
