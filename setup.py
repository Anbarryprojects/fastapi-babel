from setuptools import find_packages, setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name="fastapi-babel",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "fastapi",
        "uvicorn",
        "babel",
    ],
)
