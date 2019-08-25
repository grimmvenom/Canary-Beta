
# Resource: https://blog.easyaspy.org/post/16/2019-05-15-compiling-python-code-with-cython
# Create Recursive Cleanup of .pyc, .c, .pyd files
# To Compile: python3 compile.py build_ext --inplace
# To Cleanup on Linux: find . -maxdepth 3 -type f -name "*.c" -delete 

from setuptools import find_packages, setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

cy_ext_modules = (
    cythonize('app/core/base.py', compiler_directives={'embedsignature': True}),
    cythonize('app/core/get_arguments.py', compiler_directives={'embedsignature': True}),
    cythonize('app/modules/db_query.py', compiler_directives={'embedsignature': True}),
    cythonize('app/modules/status.py', compiler_directives={'embedsignature': True}),
    cythonize('app/modules/scraper.py', compiler_directives={'embedsignature': True}),
    cythonize('app/modules/verifier.py', compiler_directives={'embedsignature': True}),
    cythonize('app/modules/executor.py', compiler_directives={'embedsignature': True}),
    cythonize('app/modules/parse_results.py', compiler_directives={'embedsignature': True}),
    cythonize('canary.py', compiler_directives={'embedsignature': True}),
    cythonize('canary_gui.py', compiler_directives={'embedsignature': True}),
    cythonize('compile.py', compiler_directives={'embedsignature': True}),
)

packages = [
    # 'src',
    'app',
    'app.core',
    'app.modules',
    'resources',
    'resources.web_template',
    'resources.web_template.css',
    'resources.web_template.fonts',
    'resources.web_template.img',
    'resources.web_template.img.art',
]

ext_modules = [
    Extension('app.core.base', ['app/core/base.py']),
    Extension('app.core.get_arguments', ['app/core/get_arguments.py']),
    Extension('app.modules.db_query', ['app/modules/db_query.py']),
    Extension('app.modules.status', ['app/modules/status.py']),
    Extension('app.modules.scraper', ['app/modules/scraper.py']),
    Extension('app.modules.verifier', ['app/modules/verifier.py']),
    Extension('app.modules.executor', ['app/modules/executor.py']),
    Extension('app.modules.parse_results', ['app/modules/parse_results.py']),
    Extension('compile', ['compile.py']),
    Extension('canary', ['canary.py']),
    Extension('canary_gui', ['canary_gui.py']),
    Extension('compile', ['compile.py']),
]

requires = [
    'Eel',
    'pandas',
    'numpy',
    'argparse',
    'urllib3',
    'requests',
    'beautifulsoup4',
    'lxml',
    'xlsxwriter',
    'pathlib',
    'configparser',
    'sqlite3',
    'json',
    'multiprocessing',
    'Cython',
]

setup(
    name='Canary',
    version='2.0',
    install_requires=requires,
    requires=requires,
    package_dir={'': 'app'},
    packages=packages,
    author='grimmvenom',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules,
    # ext_modules=cy_ext_modules,
    language_level='3',
)
