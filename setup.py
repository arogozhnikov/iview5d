from setuptools import setup

setup(
    name="iview5d",
    version='0.1.0',
    description="Simplistic viewer for multidimensional data right in the jupyter notebook",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Alex Rogozhnikov',
    packages=['iview5d'],
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3 ',
    ],
    keywords='variability analysis, variability decomposition, contributing factors',
    install_requires=[
        'numpy',
        'einops',
        'pillow',
        'matpotlib',
    ],
)