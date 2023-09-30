from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("index_cython.pyx")
)