import setuptools


setuptools.setup(
    name="novavision-secret-output-viewer",
    version="0.4.2",
    author="DigiNova",
    author_email="info@diginova.com.tr",
    description=(
        "Resolves Environment Secrets Store references through the "
        "NovaVision runtime without exposing their values."
    ),
    license="MIT",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=8,<9",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=[
        "novavision.package",
        "novavision.package.executors",
        "novavision.package.models",
        "novavision.package.utils",
    ],
    package_dir={
        "novavision.package": "src",
    },
    python_requires=">=3.8",
    include_package_data=True,
    zip_safe=False,
)
