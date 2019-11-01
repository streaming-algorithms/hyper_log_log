from setuptools import setup, find_packages

setup(
    name='hyper_log_log',
    version='1.0.0',
    author='Mohamed Amine ZGHAL',
    author_email='aminezghal@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    zip_safe=False,
    install_requires=[
        'bitarray>=1.0.1',
        'numpy>=1.17.3'
    ]
)
