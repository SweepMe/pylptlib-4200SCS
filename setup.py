from setuptools import find_packages, setup

setup(
    name='pylptlib',
    version='1.0',
    packages=find_packages("src"),
    package_dir={'': 'src'},
    # py_modules=['pylptlib'],
    license='MIT',
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ])
