from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='daba',
    version='0.0.9',
    description='daba by Klivolks.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Vishnu Prakash',
    author_email='vishnu@klivolks.com',
    url='https://github.com/klivolks/Database',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.11'
    ],
)