from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules=[
        Extension("Origin_API_v2",
                sources=["Origin_API_v2.pyx"],
                extra_compile_args=['-fopenmp'],
                extra_link_args=['-fopenmp'])]
setup(
    name="Origin_API_v2",
    cmdclass = {'build_ext' : build_ext},
    ext_modules=ext_modules
    )