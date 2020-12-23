from setuptools import setup

setup(
    name="passwordgenerator",
    version='1.0.3',
    description='passwordgeneratortool',
    author='Anima8',
    url='https://github.com/Anima8/password-generator',
    license='MIT',
    python_requires='>=3.4',
    py_modules=['passwordgenerator'],
    entry_points={
        'console_scripts': [
            'passwordgenerator=passwordgenerator:main',
        ]
    },
)
