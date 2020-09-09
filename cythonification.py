from os import getcwd, remove
from pathlib import Path
from setuptools import setup
from shutil import move, rmtree

from Cython.Build import cythonize

in_path = getcwd()

modules = [py_mod for py_mod in Path(in_path).rglob("*.py") if py_mod.name != "setup.py"]

for py_mod in modules:
    setup(
        ext_modules = cythonize(str(py_mod), language_level = 3, force = True),
        zip_safe = False,
        script_args = ['build_ext'],
        options = {
            'build_ext': {
                'inplace': True
            }
        }
    )

    for so in Path(in_path).glob(py_mod.stem + "*.so"):
        outfile = py_mod.parent / so.name

        if str(so) != str(outfile):
            if outfile.exists():
                remove(outfile)
            move(str(so), str(outfile))

for source in Path(in_path).rglob("*.c"):
    remove(source)

rmtree("build")
