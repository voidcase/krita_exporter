import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="krita_exporter",
    version="1.0.0",
    author="voidcase",
    author_email="isak.e.lindhe@gmail.com",
    description="A script to bulk export krita files to png",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/voidcase/krita_exporter",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['krita-exporter=krita_exporter:run']
        },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
