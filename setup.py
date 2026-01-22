from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="api-log-viewer",
    version="1.0.0",
    author="Yuth Set",
    author_email="set.yuth@gmail.com",
    description="A feature-rich terminal-based tool for viewing and editing API logs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/setyuth/api-log-viewer",
    py_modules=["api_log_viewer"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Debuggers",
        "Topic :: System :: Logging",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "rich>=13.7.0",
    ],
    entry_points={
        "console_scripts": [
            "logviewer=api_log_viewer:main",
        ],
    },
)