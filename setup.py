from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
     requirements = f.readlines()

install_requires = [req.strip() for req in requirements]

setup(
    name='wake_drive',
    version='0.1',
    packages=find_packages(),
    install_requires=install_requires,
    author='Heloísa Fernandes Cano, Matheus Eduardo da Silva, Rafael Santiago da Silva',
    author_email='heloisafcano@gmail.com, matheuseduardosilva13@gmail.com, rafael.santiago.silva.1405@gmail.com',
    description='O objetivo do projeto WakeDrive é acordar motoristas sonolentos, com o intuito de evitar acidentes de trânsito.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/rafaelsantiagosilva/wake_drive',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
