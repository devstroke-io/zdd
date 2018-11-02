from os.path import dirname, join

from setuptools import find_packages, setup

KEYWORDS = []
CLASSIFIERS = [
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python',
    'Topic :: Software Development',
    'Topic :: Utilities',
]
INSTALL_REQUIRES = [
    'click==7.*',
    'colorama==0.4.*',
    'docker==3.*',
    'pyinstaller==3.*',
]

PROJECT_DIR = dirname(__file__)
README_FILE = join(PROJECT_DIR, 'README.md')
ABOUT_FILE = join(PROJECT_DIR, 'src', 'zdd', '__about__.py')


def get_readme():
    with open(README_FILE) as fileobj:
        return fileobj.read()


def get_about():
    about = {}
    with open(ABOUT_FILE) as fileobj:
        exec(fileobj.read(), about)
    return about


ABOUT = get_about()

setup(
    name=ABOUT['__title__'],
    version=ABOUT['__version__'],
    description=ABOUT['__summary__'],
    long_description=get_readme(),
    author=ABOUT['__author__'],
    author_email=ABOUT['__email__'],
    url=ABOUT['__uri__'],
    keywords=KEYWORDS,
    license=ABOUT['__license__'],
    classifiers=CLASSIFIERS,
    package_dir={'': 'src'},
    packages=find_packages('src'),
    entry_points={
        'console_scripts': [
            'zdd=zdd.__main__:main',
        ],
    },
    install_requires=INSTALL_REQUIRES,
    python_requires='>=3.7',
    zip_safe=False
)
