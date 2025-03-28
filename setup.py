# type: ignore
"""
Setup file for progressivis.
"""
import sys
import os
import os.path
from setuptools import setup
from setuptools.extension import Extension

PACKAGES = [
    "progressivis_cpp",
    "progressivis_cpp.examples",
]

def _is_linux():
    return sys.platform == "linux"


def _np_get_include():
    import numpy as np

    return np.get_include()


EXTENSIONS = [
    Extension(
        "progressivis_cpp.examples.cxx_max",
        ["progressivis_cpp/examples/cxx_max.cpp"],
        include_dirs=[
            "include",
            _np_get_include(),
            "pybind11/include",
            "xtensor/include",
            "xtensor-python/include",
            "xtl/include",
            "CRoaringUnityBuild",
            os.path.join(sys.prefix, "include"),
            os.path.join(sys.prefix, "Library", "include"),
        ],
        extra_compile_args=["-std=c++17", "-Wall", "-O0", "-g"] if _is_linux() else ["-std=c++17",],
        language="c++",
    ),
]


def read(fname):
    "Read the content of fname as string"
    with open(os.path.join(os.path.dirname(__file__), fname)) as infile:
        return infile.read()


setup(
    url="https://github.com/progressivis/progressivis_cpp",
    packages=PACKAGES,
    platforms="any",
    ext_modules=EXTENSIONS,
    package_data={
        # If any package contains *.md, *.txt or *.rst files, include them:
        "doc": ["*.md", "*.rst"],
    },
)
