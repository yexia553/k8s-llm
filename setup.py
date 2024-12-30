"""
Setup configuration for k8sllm package.

This module contains the package configuration for installing k8sllm
using pip or other Python package managers.
"""

from setuptools import setup, find_packages

setup(
    name="k8sllm",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'click>=8.0.0',
        'pyyaml>=6.0.1',
        'openai>=1.3.0',
        'kubernetes>=28.1.0',
        'python-dotenv>=1.0.0',
    ],
    entry_points={
        'console_scripts': [
            'k8sllm=k8sllm.cli:cli',
        ],
    },
    author="yexia553",
    author_email="your.email@example.com",
    description="A natural language interface for Kubernetes operations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yexia553/k8sllm",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
