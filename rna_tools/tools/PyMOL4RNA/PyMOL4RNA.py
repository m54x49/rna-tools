#!/usr/bin/env python
"""
Quick reference:

- clarna: show contacts classification of the selected fragment based on ClaRNA
- ss: show secondary structure of the selection based on py3dna.py (3DNA (Lu, Olson 2003))
- ss_all: the same as ss() but for all objects
- pdbsrc: show PDB content (source) of selection.
- seq: show sequence of the selection
- ino: represent ions as sphare and yellow inorganic, such us Mg
- p: shortcut for putting a seq at the bottom. Pretty cool for screenshots with names of objects
- spli: color snRNA of the spliceosome and bases according to identity U(blue), A(orange), G(red), C(forest)
- rp: @todo
- rs: @todo
- rib: @todo
- clr:
-
If you want more, read for interesting functions https://daslab.stanford.edu/site_data/docs_pymol_rhiju.pdf
"""
import tempfile
import math
import subprocess
import os
from itertools import izip
import sys

try:
    from pymol import cmd
except ImportError:
    print("PyMOL Python lib is missing")
    # sys.exit(0)

from rna_tools.rna_tools_lib import RNAStructure

try:
    RNA_TOOLS_PATH
    EXECUTABLE
except NameError:
    RNA_TOOLS_PATH = os.environ.get('RNA_TOOLS_PATH')
    EXECUTABLE="/bin/zsh"
    SOURCE=""

def exe(cmd, verbose=False):
    """Helper function to run cmd. Using in this Python module."""
    if verbose: print('cmd:' + cmd)
    o = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         executable=EXECUTABLE)
    out = o.stdout.read().strip().decode()
    err = o.stderr.read().strip().decode()
    return out, err


def save_transformed(object, file):
    """Saves the molecule with coordinates from the current orientation.

     Args:
        object (string): PyMOL name
        file (string): a file name to output file

    Example::

         PyMOL>save_transformed 6bk8_RNA_only_Oriented, 6bk8_RNA_only_Oriented.pdb

    Source: <https://pymolwiki.org/index.php/Modeling_and_Editing_Structures>
    """
    m = cmd.get_view(0)
    ttt = [m[0], m[1], m[2], 0.0,
           m[3], m[4], m[5], 0.0,
           m[6], m[7], m[8], 0.0,
           0.0,   0.0,  0.0, 1.0]
    cmd.transform_object(object,ttt,transpose=1)
    cmd.save(file,object)


def color_by_text(txt):
    """Helper function used for color-coding based on residue indexes ranges."""
    for t in txt.strip().split('\n'):
        color, resi = t.replace('color ', '').split(',')
        print((color, resi))
        cmd.color(color.strip(), resi.strip())


def rp():
    """Represent your RNA."""
    cmd.hide("sticks", "all")
    cmd.hide("lines", "all")
    cmd.show("cartoon", "all")
    cmd.set("cartoon_ring_mode", 3)
    cmd.set("cartoon_ring_finder", 2)
    cmd.set("cartoon_ladder_mode", 1)

def show_all_at_once():
    cmd.set('states', 'on')


def rp06():
  txt = """color black, all
  color pink, resi 2-10+163-170
  color grey, resi 12-33
  color green, resi 40-41
  color green, resi 161-162
  color orange, resi 45-61
  color green, resi 64-73
  color blue, resi 74-155
  color cyan, resn B1Z"""
  for t in txt.split('\n'):
    color, resi = t.replace('color ', '').split(',')
    print(color, resi)
    cmd.color(color.strip(), resi.strip())


def grid_on():
    cmd.set('grid_mode', 1)


def grid_off():
    cmd.set('grid_mode', 0)


def rp14():
  """color black; # everything
 color blue, resi 1-5+55-59; # p1
 color green, resi 7-11+16-20; # p2
 color magenta, resi 23+60; # pk
 color yellow, resi 29-34+45-50; # p3
 color grey, resi 24-28+51-54; # e-loop
 color red, resi 6+21+22+24+25+28+52+54; # higly conserved"""
 #color blue, resi 5+55


  txt ="""color black, all
 color red, resi 1-5+55-59
 color blue, resi 1-5+55-59; # p1
 color green, resi 7-11+16-20
 color magenta, resi 23+60
 color yellow, resi 29-34+45-50
 color grey, resi 24-28+51-54
 color red, resi 6+21+22"""
  for t in txt.split('\n'):
    color, resi = t.replace('color ', '').split(',')
    print(color, resi)
    cmd.color(color.strip(), resi.strip())

def rp14s():
  """color with Baker's SHAPE data for rp14!"""
  txt = """
   color yellow, resi 12-15+25-29+35-44
   color red, resi 21-24+53+54+60
  """
  color_by_text(txt)

def rs():
    """    The function creates super-cool cartoon-like RNA and colors each structure as a rainbow.
    Good to view aligned structures in a grid.

    .. image:: ../../rna_tools/utils/PyMOL4RNA/doc/rs.png
    """
    cmd.hide("sticks", "all")
    cmd.hide("lines", "all")
    cmd.show("cartoon", "all")
    cmd.set("cartoon_ring_mode", 3)
    cmd.set("cartoon_ring_finder", 2)
    cmd.set("cartoon_ladder_mode", 2)
    cmd.set("cartoon_ring_transparency", 0.30)
    cmd.spectrum()

    obj_list = cmd.get_names('objects')

    colours = ['rainbow']
    ncolours = len(colours)
    # Loop over objects
    i = 0
    for obj in obj_list:
        print("  ", obj, colours[i])
        cmd.spectrum('count', colours[i], obj)
        i = i+1
        if(i == ncolours):
           i = 0


def rcomp():
    """RNA like in papers ;-)

    Similar to rc() but this time it colors each (and every) structure in different colour.
    Great on viewing-comparing superimposed structures.

    """
    cmd.hide("sticks", "all")
    cmd.hide("lines", "all")
    cmd.show("cartoon", "all")
    cmd.set("cartoon_ring_mode", 3)
    cmd.set("cartoon_ring_finder", 2)
    cmd.set("cartoon_ladder_mode", 2)
    cmd.set("cartoon_ring_transparency", 0.30)

    obj_list = cmd.get_names('objects')

    colours = ['red', 'green', 'blue', 'yellow', 'violet', 'cyan',    \
           'salmon', 'lime', 'pink', 'slate', 'magenta', 'orange', 'marine', \
           'olive', 'purple', 'teal', 'forest', 'firebrick', 'chocolate',    \
           'wheat', 'white', 'grey' ]
    ncolours = len(colours)

           # Loop over objects
    i = 0
    for obj in obj_list:
        print("  ", obj, colours[i])
        cmd.color(colours[i], obj)
        i = i+1
        if(i == ncolours):
           i = 0


def align_all( subset = [] ):
  """
  Superimpose all open models onto the first one.
  This may not work well with selections.

  This function is probably taken from https://daslab.stanford.edu/site_data/docs_pymol_rhiju.pdf
  """
  print("""This returns a list with 7 items:

    RMSD after refinement
    Number of aligned atoms after refinement
    Number of refinement cycles
    RMSD before refinement
    Number of aligned atoms before refinement
    Raw alignment score
    Number of residues aligned """)

  AllObj=cmd.get_names("all")
  for x in AllObj[1:]:
    #print(AllObj[0],x)
    subset_tag = ''
    if isinstance( subset, int ):
      subset_tag = ' and resi %d' % subset
    elif isinstance( subset, list ) and len( subset ) > 0:
      subset_tag = ' and resi %d' % (subset[0])
      for m in range( 1,len(subset)): subset_tag += '+%d' % subset[m]
    elif isinstance( subset, str ) and len( subset ) > 0:
      subset_tag = ' and %s' % subset
    values = cmd.align(x+subset_tag,AllObj[0]+subset_tag)
    print(AllObj[0], x, ' '.join([str(v) for v in values]), '-- RMSD', values[3], ' of ', values[6], 'residues')
    cmd.zoom()


def pdb():
    """Get PDB content of selection.

    .. image:: ../../rna_tools/utils/PyMOL4RNA/doc/pdb.png"""
    tmpfn = '/tmp/pymol_get_pdb.pdb'
    cmd.save(tmpfn, '(sele)')
    s = RNAStructure(tmpfn)
    for l in s.lines:
        print(l)


def clarna():
    """Get contacts classification of the selected fragment based on ClaRNA.

    .. image:: ../../rna_tools/tools/PyMOL4RNA/doc/clarna.png
    """
    f = tempfile.NamedTemporaryFile(delete=False) # True)
    cmd.save(f.name + '.pdb', '(sele)')
    out, err = exe(SOURCE + " && " + CLARNA_RUN + " -ipdb " + f.name + '.pdb -bp+stack')
    print('\n'.join(out.split('\n')[1:]))  # to remove first line of py3dna /tmp/xxx
    if err:
        print(err)
    f.close()


def seq():
    """Get sequence of the selected fragment using ``rna_pdb_toolsx.py --get_seq ``.

    .. image:: ../../rna_tools/utils/PyMOL4RNA/doc/ss.png
    """
    f = tempfile.NamedTemporaryFile(delete=False) # True)
    cmd.save(f.name, '(sele)')
    out, err = exe('source ~/.zshrc && ' + RNA_TOOLS_PATH + '/bin/rna_pdb_toolsx.py --get_seq ' + f.name)
    print(out)
    if err:
        print(err)
    f.close()

def ss():
    """Get Secondary Structure of (sele) based on py3dna.py.

    .. image:: ../../rna_tools/utils/PyMOL4RNA/doc/ss.png
    """
    f = tempfile.NamedTemporaryFile(delete=False) # True)
    cmd.save(f.name, '(sele)')
    out, err = exe(RNA_TOOLS_PATH + '/bin/rna_x3dna.py ' + f.name)
    print('\n'.join(out.split('\n')[2:]))  # to remove first line of py3dna /tmp/xxx
    if err:
        print(err)
    f.close()


def ss_all():
    """The same as ss() but for all objects."""
    subset = "*"
    AllObj = cmd.get_names("all")
    # print AllObj
    for name in AllObj[:]:
        if not name.startswith('_align'):
            print('> ' + name)
            f = tempfile.NamedTemporaryFile(delete=False) # True)
            cmd.save(f.name, name)
            out, err = exe(RNA_TOOLS_PATH + '/bin/rna_x3dna.py ' + f.name)
            print('\n'.join(out.split('\n')[2:]))  # to remove first line of py3dna /tmp/xxx
            # hide this line: is >tmpGCszi7 nts=4 [tmpGCszi7] -- secondary structure derived by DSSR
            if err:
                print(err)
            f.close()
    print('-- secondary structure derived by DSSR')


def p():
    """A shortcut for putting a seq at the bottom. Pretty cool for screenshots with names of objects.

    .. image:: ../../rna_tools/utils/PyMOL4RNA/doc/p.png
    """
    cmd.set("seq_view_format", 4)
    cmd.set("seq_view", 1)
    cmd.set("seq_view_location", 1)
    cmd.set("seq_view_overlay", 1)


def rna_cartoon():
    """http://www-cryst.bioc.cam.ac.uk/members/zbyszek/figures_pymol

    .. image:: ../pngs/rna_cartoon.png
    """
    cmd.set("cartoon_ring_mode", 3)
    cmd.set("cartoon_ring_finder", 1)
    cmd.set("cartoon_ladder_mode", 1)
    cmd.set("cartoon_nucleic_acid_mode", 4)
    cmd.set("cartoon_ring_transparency", 0.5)


def rp17():
    """Color-coding for secondary structure elements for the RNA Puzzle 17.

    For the variant::

         CGUGGUUAGGGCCACGUUAAAUAGUUGCUUAAGCCCUAAGCGUUGAUAAAUAUCAGGUGCAA
         ((((.[[[[[[.))))........((((.....]]]]]]...(((((....)))))..))))
         # len 62-nt

    .. image:: ../../rna_tools/tools/PyMOL4RNA/doc/rna.png
    """
    txt = """color forest, resi 1-5+12-16; # p1
 color magenta, resi 6-11+34-39;
 color grey, resi 17-24;
 color marine, resi 25-28+59-62;
 color deepblue, resi 29-33+40-42;
 color orange, resi 44-47+48-56;
 color yellow, resi 57-58;
 color red, resi 19+20+21;
"""
    color_by_text(txt)

def rp17csrv():
    """Color-coding for secondary structure elements for the RNA Puzzle 17.

    For the variant::

         CGUGGUUAGGGCCACGUUAAAUAGUUGCUUAAGCCCUAAGCGUUGAUAAAUAUCAGGUGCAA
         ((((.[[[[[[.))))........((((.....]]]]]]...(((((....)))))..))))
         # len 62-nt

    .. image:: ../../rna_tools/utils/PyMOL4RNA/doc/rna.png
    """
    txt = """color forest, resi 1-5+12-16; # p1
 color magenta, resi 6-11+34-39;
 color grey, resi 17-24;
 color marine, resi 25-28+59-62;
 color deepblue, resi 29-33+40-42;
 color orange, resi 44-47+48-56;
 color yellow, resi 57-58;
 color red, resi 5+19+20+21+31+32+33+40+41+42
"""
    color_by_text(txt)



def rp172():
    """Color-coding for secondary structure elements for the RNA Puzzle 17.

    For the variant::

         CGUGGUUAGGGCCACGUUAAAUAGUUGCUUAAGCCCUAAGCGUUGAUAUCAGGUGCAA
         ((((.[[[[[[.))))........((((.....]]]]]]...((((()))))..))))
         # len 58-nt

    See rp17()
    """

    txt = """color forest, resi 1-5+12-16; # p1
 color magenta, resi 6-11+34-39
 color grey, resi 17-24
 color marine, resi 25-28+55-58
 color deepblue, resi 29-33+40-42;
 color orange, resi 43-47+48-52;
 color yellow, resi 53-54;
 color red, resi 19+20+21;
"""
    color_by_text(txt)

def color_aa_types():
    """Color aminoacides types like in Cider (http://pappulab.wustl.edu/CIDER/)"""
    txt = """
color gray70, resn Ala+Ile+Leu+Met+Phe+Trp+Val #hydrophobic
color yellow, resn Tyr+Trp #aromatic
color blue, resn Arg+Lys+His # positive
color forest, resn GLN+SER+GLY+thr
color pink, resn PRO # pro
color red, resn GLU+asp # """
    print("""color (according to) amino-acids types)
hydrohobic (gray)  Ala+Ile+Leu+Met+Phe+Trp+Val
aromatic (yellow) Tyr+Trp
positive (blue)  Arg+Lys+His
polar (forest) Gln+Ser+Glu+Thr
negative (red) Glu+Asp
prolina ;) (pink) Pro""")
    color_by_text(txt)


def color_obj(rainbow=0):

        """
        stolen from :)
AUTHOR
        Gareth Stockwell

USAGE
        color_obj(rainbow=0)

        This function colours each object currently in the PyMOL heirarchy
        with a different colour.  Colours used are either the 22 named
        colours used by PyMOL (in which case the 23rd object, if it exists,
        gets the same colour as the first), or are the colours of the rainbow

        """

        # Process arguments
        rainbow = int(rainbow)

        # Get names of all PyMOL objects
        obj_list = cmd.get_names('objects')

        if rainbow:

           print("\nColouring objects as rainbow\n")

           nobj = len(obj_list)

           # Create colours starting at blue(240) to red(0), using intervals
           # of 240/(nobj-1)
           for j in range(nobj):
              hsv = (240-j*240/(nobj-1), 1, 1)
              # Convert to RGB
              rgb = hsv_to_rgb(hsv)
              # Define the new colour
              cmd.set_color("col" + str(j), rgb)
              print(obj_list[j], rgb)
              # Colour the object
              cmd.color("col" + str(j), obj_list[j])

        else:
           # List of available colours
           colours = ['red', 'green', 'blue', 'yellow', 'violet', 'cyan',    \
           'salmon', 'lime', 'pink', 'slate', 'magenta', 'orange', 'marine', \
           'olive', 'purple', 'teal', 'forest', 'firebrick', 'chocolate',    \
           'wheat', 'white', 'grey' ]
           ncolours = len(colours)

           # Loop over objects
           i = 0
           for obj in obj_list:
              print("  ", obj, colours[i])
              cmd.color(colours[i], obj)
              i = i+1
              if(i == ncolours):
                 i = 0


def names():
    # Get names of all PyMOL objects
    obj_list = cmd.get_names('objects')
    for o in obj_list:
        print(o)


def color_rbw(rainbow=0):
        """
        similar to color_obj() but this time colors every obect as rainbow
        """
        rainbow = int(rainbow)

        # Get names of all PyMOL objects
        obj_list = cmd.get_names('objects')

        if rainbow:

           print("\nColouring objects as rainbow\n")

           nobj = len(obj_list)

           # Create colours starting at blue(240) to red(0), using intervals
           # of 240/(nobj-1)
           for j in range(nobj):
              hsv = (240-j*240/(nobj-1), 1, 1)
              # Convert to RGB
              rgb = hsv_to_rgb(hsv)
              # Define the new colour
              cmd.set_color("col" + str(j), rgb)
              print(obj_list[j], rgb)
              # Colour the object
              cmd.color("col" + str(j), obj_list[j])
        else:
           colours = ['rainbow']
           ncolours = len(colours)

           # Loop over objects
           i = 0
           for obj in obj_list:
              print("  ", obj, colours[i])
              cmd.spectrum('count', colours[i], obj)
#              cmd.color(colours[i], obj)
              i = i+1
              if(i == ncolours):
                 i = 0

def ino():
    """Sphare and yellow inorganic, such us Mg.

    .. image:: ../../rna_tools/utils/PyMOL4RNA/doc/ion.png"""
    cmd.show("spheres", "inorganic")
    cmd.set('sphere_scale', '0.25', '(all)')
    cmd.color("yellow", "inorganic")

def spl():
    """Color spl RNAs (for only color spl RNA and use 4-color code for residues see `spl2`)
    """
    AllObj = cmd.get_names("all")
    for name in AllObj:
        if 'Exon' in name or 'exon' in name:
            cmd.color('yellow', name)
        if 'Intron' in name or 'intron' in name or '5splicing-site' in name:
            cmd.color('gray40', name)
        if '3exon-intron' in name.lower():
            cmd.color('gray20', name)
        if name.startswith("U2_snRNA"):
            cmd.color('forest', name)
        if name.startswith("U5_snRNA"):
            cmd.color('blue', name)
        if name.startswith("U4_snRNA"):
            cmd.color('orange', name)
        if name.startswith("U6_snRNA"):
            cmd.color('red', name)

    cmd.do('color gray')

    # trisnrp
    cmd.do('color orange, chain V') # conflict
    cmd.do('color red, chain W')
    cmd.do('color blue, chain U')
    #
    cmd.do('color blue, chain 5')
    cmd.do('color forest, chain 2')
    cmd.do('color red, chain 6')
    cmd.do('color orange, chain 4')
    cmd.do('color yellow, chain Y')
    # shi
    cmd.do('color blue, chain D') # u5
    cmd.do('color forest, chain L') # u2
    cmd.do('color red, chain E') # u6
    cmd.do('color yellow, chain M')
    cmd.do('color yellow, chain N')
    # afte branch
    cmd.do('color blue, chain U') # u5
    cmd.do('color forest, chain Z') # u2
    cmd.do('color red, chain V') # u6
    cmd.do('color yellow, chain E')
    cmd.do('color black, chain I')
    # 5WSG
    # Cryo-EM structure of the Catalytic Step II spliceosome (C* complex) at 4.0 angstrom resolution
    cmd.do('color blue, chain D') # u5
    #cmd.do('color forest, chain L') # u2
    cmd.do('color yellow, chain B')
    cmd.do('color yellow, chain b')
    cmd.do('color black, chain N')
    cmd.do('color black, chain M')

    cmd.do('color black, chain 3') # orange
    cmd.do('color black, chain E') # yellow
    cmd.do('color black, chain i')
    cmd.do('color black, chain e')

    cmd.do('bg gray')
    cmd.do('remove (polymer.protein)')

    cmd.set("cartoon_tube_radius", 1.0)
    ino()

def spl2():
    """Color spl RNAs and use 4-color code for residues (for only color spl RNA see `spl`)
    """

    AllObj = cmd.get_names("all")
    for name in AllObj:
        if 'Exon' in name or 'exon' in name:
            cmd.color('yellow', name)
        if 'Intron' in name or 'intron' in name or '5splicing-site' in name:
            cmd.color('gray40', name)
        if '3exon-intron' in name.lower():
            cmd.color('gray20', name)
        if name.startswith("U2_snRNA"):
            cmd.color('forest', name)
        if name.startswith("U5_snRNA"):
            cmd.color('blue', name)
        if name.startswith("U4_snRNA"):
            cmd.color('orange', name)
        if name.startswith("U6_snRNA"):
            cmd.color('red', name)

    cmd.do('color gray')

    # trisnrp
    cmd.do('color orange, chain V') # conflict
    cmd.do('color red, chain W')
    cmd.do('color blue, chain U')
    #
    cmd.do('color blue, chain 5')
    cmd.do('color forest, chain 2')
    cmd.do('color red, chain 6')
    cmd.do('color orange, chain 4')
    cmd.do('color yellow, chain Y')
    # shi
    cmd.do('color blue, chain D') # u5
    cmd.do('color forest, chain L') # u2
    cmd.do('color red, chain E') # u6
    cmd.do('color yellow, chain M')
    cmd.do('color yellow, chain N')
    # afte branch
    cmd.do('color blue, chain U') # u5
    cmd.do('color forest, chain Z') # u2
    cmd.do('color red, chain V') # u6
    cmd.do('color yellow, chain E')
    cmd.do('color black, chain I')
    # 5WSG
    # Cryo-EM structure of the Catalytic Step II spliceosome (C* complex) at 4.0 angstrom resolution
    cmd.do('color blue, chain D') # u5
    #cmd.do('color forest, chain L') # u2
    cmd.do('color yellow, chain B')
    cmd.do('color yellow, chain b')
    cmd.do('color black, chain N')
    cmd.do('color black, chain M')

    cmd.do('color black, chain 3') # orange
    cmd.do('color black, chain E') # yellow
    cmd.do('color black, chain i')
    cmd.do('color black, chain e')

    cmd.do('bg gray')
    cmd.do('remove (polymer.protein)')

    cmd.color("red",'resn rG+G and name n1+c6+o6+c5+c4+n7+c8+n9+n3+c2+n1+n2')
    cmd.color("forest",'resn rC+C and name n1+c2+o2+n3+c4+n4+c5+c6')
    cmd.color("orange",'resn rA+A and name n1+c6+n6+c5+n7+c8+n9+c4+n3+c2')
    cmd.color("blue",'resn rU+U and name n3+c4+o4+c5+c6+n1+c2+o2')
    cmd.set("cartoon_tube_radius", 1.0)
    ino()


def _spli():
    """
    # this trick is taken from Rhiju's Das code
    color red,resn rG+G and name n1+c6+o6+c5+c4+n7+c8+n9+n3+c2+n1+n2
    color forest,resn rC+C and name n1+c2+o2+n3+c4+n4+c5+c6
    color orange, resn rA+A and name n1+c6+n6+c5+n7+c8+n9+c4+n3+c2
    color blue, resn rU+U and name n3+c4+o4+c5+c6+n1+c2+o2

    #
    #cmd.color("yellow", "*intron*")
    #cmd.color("yellow", "*exon*")

    #cmd.show("spheres", "inorganic")
    #cmd.color("yellow", "inorganic")
    """
    cmd.color("orange", "U4_snRNA*")
    cmd.color("red", "U6_snRNA*")
    cmd.color("blue", "U5_snRNA*")
    cmd.color("green", "U2_snRNA*")
    cmd.color("red",'resn rG+G and name n1+c6+o6+c5+c4+n7+c8+n9+n3+c2+n1+n2')
    cmd.color("forest",'resn rC+C and name n1+c2+o2+n3+c4+n4+c5+c6')
    cmd.color("orange",'resn rA+A and name n1+c6+n6+c5+n7+c8+n9+c4+n3+c2')
    cmd.color("blue",'resn rU+U and name n3+c4+o4+c5+c6+n1+c2+o2')


def rgyration(selection='(all)', quiet=1):
    '''

[PyMOL] RES: radius of gyration
From: Tsjerk Wassenaar <tsjerkw@gm...> - 2011-03-31 14:07:03
https://sourceforge.net/p/pymol/mailman/message/27288491/
DESCRIPTION

    Calculate radius of gyration

USAGE

    rgyrate [ selection ]
 :::warning:::
 if nothing is selected  function is calculating radius of gyration for all pdbs in current Pymol session
    '''
    quiet = int(quiet)
    model = cmd.get_model(selection).atom
    x = [i.coord for i in model]
    mass = [i.get_mass() for i in model]
    xm = [(m*i,m*j,m*k) for (i,j,k),m in izip(x,mass)]
    tmass = sum(mass)
    rr = sum(mi*i+mj*j+mk*k for (i,j,k),(mi,mj,mk) in izip(x,xm))
    mm = sum((sum(i)/tmass)**2 for i in izip(*xm))
    rg = math.sqrt(rr/tmass - mm)
    if not quiet:
        print("Radius of gyration: %.2f" % (rg))
    return rg


def qrnass():
    cmd.save('sele.pdb', '(sele)')
    mini('sele.pdb')


def qrnas():
    subset = "*"
    AllObj=cmd.get_names("all")
    #print AllObj
    for x in AllObj[:]:
      print(x, 'qrnas...')
      #print(AllObj[0],x)
      f = tempfile.NamedTemporaryFile(delete=True)
      #print f.name
      #f.write(XX)
      cmd.save(f.name, x)
      #p = Process(target=mini)
      #p.start()
      mini()
      #cmd.load('out.pdb', 'ref')
      #p.join()
      #print x
      #print '\n'.join(out.split('\n')[1:]) # to remove first line of py3dna /tmp/xxx
      f.close()
      break
    align_all()
    rr()
    cmd.set('grid_mode', 1)


def mini(f):
    #os.system('/home/magnus/opt/qrnas/QRNA02/QRNA -i ' + f + ' -c /home/magnus/opt/qrnas/QRNA02/configfile.txt -o out.pdb')
    os.system('~/opt/qrnas/QRNA02/QRNA -i ' + f + ' -c ~/opt/qrnas/QRNA02/configfile.txt -o out.pdb')
    cmd.delete('mini')
    cmd.load('out.pdb', 'mini')
    print('end')


def reload():
    """Reload PyMOL4RNA.py"""
    cmd.run(RNA_TOOLS_PATH + "/rna_tools/tools/PyMOL4RNA/PyMOL4RNA.py")

def clr():
  """clr - make white bg and structure black"""
  cmd.bg_color( "white" )
  color_by_text('color black, all')


def rlabel():
    cmd = "n. C1'", '"%s %s" % (resn, resi)'
    print('label ' + cmd)
    cmd.label(cmd)


def sav(name):
    cmd.bg_color( "white" )
    cmd.save('/home/magnus/Desktop/' + name + '.png')
    cmd.save('/home/magnus/Desktop/' + name + '.pse')

def hide_rna():
    cmd.hide('(polymer.nucleic)')
cmd.extend('rna-hide', hide_rna)

def show_rna():
    cmd.show('(polymer.nucleic)')
cmd.extend('rna-show', show_rna)

def select_rna():
    cmd.select('polymer.nucleic')
cmd.extend('select-rna', select_rna)

def hide_protein():
    cmd.hide('(polymer.protein)')
cmd.extend('protein-hide', hide_protein)

def select_protein():
    cmd.select('polymer.protein')
cmd.extend('protein-select', select_protein)

import getpass
user = getpass.getuser()

def tmp():
    cmd.save('/home/' + user + '/Desktop/' + tmp + '.png')
    cmd.save('/home/' + user + '/Desktop/' + tmp + '.pse')


################################################################################
def sav_tmp():
    from shutil import copyfile
    import datetime
    try:
        TMP_FOLDER + ' '
    except:
        print("Error: Set up TMP_FOLDER in your ~/.pymolrc, e.g. TMP_FOLDER = '/home/magnus/Desktop/PyMOL/'")
        return

    try:
        os.mkdir(TMP_FOLDER)
    except:
        pass

    date = datetime.datetime.today().strftime('%Y-%m-%d.%S')
    try:
        fn = TMP_FOLDER +  os.sep + id + '_' + date + '.pse'
    except TypeError:
        fn = TMP_FOLDER +  os.sep + '_' + date + '.pse'
    cmd.save(fn)
    print('Save...' + fn)
    cmd.save(fn.replace('.pse', '.png'))
    copyfile(fn, TMP_FOLDER + '/last.pse')

def load_tmp():
    print('Load...')
    cmd.load(TMP_FOLDER + '/last.pse')

try:
    from pymol import cmd
except ImportError:
    print("PyMOL Python lib is missing")
else:
    print('   PyMOL4RNA (rna-pdb-tools)  ')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('Quickref: ')
    print('  alter (sele), chain="B" ')
    print('  alter (sele), resv -= 4')
    print('  alter (chain B), resv -= 44 ')
    print('set dash_color, red; set dash_width, 4')
    print('p - prepare seq for printing')
    print('rp - rna present, object names only click to get compact legend')
    print('rp17')
    print('get_pdb')
    print('rna_cartoon')
    print('rs')
    print('rcomp')
    print('color_obj')
    print('color_rbw')
    print('aa')
    print('savt - save_transformed <object>, <file>')
    print("""spl - color snRNAs of the spliceosome:
    green: U2,  blue: U5, red:U6, orange:U2""")
    print('RNA_TOOLS_PATH env variable used: ' + RNA_TOOLS_PATH)

    #cmd.set_key('CTRL-S', cmd.save, ['/home/magnus/Desktop/tmp.pse'])
    cmd.set_key('CTRL-S', sav_tmp)
    cmd.set_key('CTRL-Z', load_tmp)  # ostatni wrzucam tutaj
    #cmd.load, ['/home/magnus/Desktop/tmp.pse'])
    # main code #

    cmd.extend('rp17', rp17)
    cmd.extend('rp17csrv', rp17csrv)

    cmd.extend('rp', rp)
    cmd.extend('p', p)
    cmd.extend('pdb', pdb)
    cmd.extend('seq', seq)
    cmd.extend('rna_cartoon', rna_cartoon)
    cmd.extend('rs', rs)
    cmd.extend('ino', ino)
    cmd.extend('rcomp', rcomp)
    cmd.extend('color_obj', color_obj)
    cmd.extend('color_rbw', color_rbw)
    cmd.extend('aa', align_all)
    cmd.extend('ss', ss)
    cmd.extend('ss_all', ss_all)
    cmd.extend('clarna', clarna)
    cmd.extend("rgyration", rgyration)
    cmd.extend("spl", spl)
    cmd.extend("spl2", spl2)
    cmd.extend('rlabel', 'rlabel')

    cmd.extend('grid_on', grid_on)
    cmd.extend('grid_off', grid_off)
    cmd.extend('reload', reload)

    cmd.extend('color_aa_types', color_aa_types)

    cmd.extend('names', names)

    # set dash lines
    cmd.set('dash_color', 'red')
    cmd.set('dash_width', 4)

    cmd.extend('sav', sav)
    cmd.extend('save_transformed', save_transformed)
    cmd.extend('savt', save_transformed)
    cmd.extend('show_all_at_once', show_all_at_once)

    print('###########################')
    print('PYMOL4RNA loading .... [ok]')
    print('###########################')
