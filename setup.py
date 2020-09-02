from setuptools import setup

setup(
    name="passwordgenerator",
    version='1.0',
    description='passwordgeneratorTool',
    author='Anima8',
    url='https://github.com/Anima8/passwordgenerator',
    license='MIT',
    python_requires='>=3.4',
    py_modules=['passwordgenerator'],
    entry_points={'console_scripts': ['passwordgenerator=passwordgenerator:main',]},
)