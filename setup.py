import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='easylog',
    version='0.1.9999',
    description='Logging simplified',
    url='https://github.com/christopherLang/easylog',
    author='Christopher Lang',
    author_email='chlang206@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='',
    # packages=setuptools.find_packages(),
    packages=['easylog'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ]
)
