from os.path import join, dirname
from setuptools import setup


VERSION = (0, 0, 1)
__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))

f = open(join(dirname(__file__), 'README.rst'))
long_description = f.read().strip()
f.close()

install_requires = [
    'Django',
]
test_requires = [
    'nose',
    'coverage',
]

setup(
    name = 'ella-quizzes',
    description = "ella-quizzes",
    url = "https://github.com/ella/ella-quizzes/",
    long_description = long_description,
    version = __versionstr__,
    author = "ella",
    author_email = "ella.project@gmail.com",
    packages = ['ella_quizzes'],
    zip_safe = False,
    include_package_data = True,
    classifiers = [
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires,

    test_suite='test_ella_quizzes.run_tests.run_all',
    test_requires=test_requires,
)
