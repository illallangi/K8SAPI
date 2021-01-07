import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="illallangi-k8sapi",
    version="0.0.1",
    author="Andrew Cole",
    author_email="andrew.cole@illallangi.com",
    description="TODO: SET DESCRIPTION",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/illallangi/K8SAPI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": ["k8s-tool=illallangi.k8s:__main__.cli"],
    },
    install_requires=[
        "cached_property",
        "click",
        "loguru",
        "notifiers",
        "yarl",
    ],
)
