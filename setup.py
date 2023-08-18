from distutils.core import setup

from setuptools import find_namespace_packages

with open("VERSION", "r") as f:
    version = f.read().strip()

with open("requirements.txt", "r") as f:
    required_packages = f.read().split()

setup(
    name="sat-heuristic-validator",
    version=version,
    description="A tool that tests correctness performance of heuristic algorithms for SAT problem.",
    author="Paweł Wanat",
    author_email="wanatpj+sat@gmail.com",
    packages=find_namespace_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "scikit-learn",
        "torch",
    ],
    setup_requires=["wheel", "bdist_wheel"],
)