import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="i3-workspace-swap",
    description='A python utility swap the content of two workplaces in i3wm',
    long_description=long_description,
    long_description_content_type="text/markdown",

    version="1.1.0",
    url='https://github.com/einzigartigername/i3-workspace-swap',
    license='MIT',

    author='Nelson Gillo',
    author_email='nelson.gillo@gmx.de',

    packages=setuptools.find_packages(),

    scripts=['i3-workspace-swap'],
    install_requires=['i3ipc'],
    classifiers=[
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        'Programming Language :: Python :: 3'
    ],
    python_requires='>=3.6',
)
