from setuptools import setup, find_packages
import setuptools

setup(
    name="schrodinger",
    version="1.0.0",
    description="A command-line tool that clones and organizes directory structures for multi-language projects.",
    author="Kayur Amour Harry",
    packages=find_packages(),
    install_requires=[
        "rich>=13.0.0",
        "structlog>=23.1.0",
    ],
    entry_points={
        "console_scripts": [
            "schrodinger=schrodinger.cli:main",
        ],
    },
    include_package_data=True,
)

if __name__ == "__main__":
    setuptools.setup()


# KEEP TOML, KILL THIS except discord thing