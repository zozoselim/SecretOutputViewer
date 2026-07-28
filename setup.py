import setuptools


setuptools.setup(
    name="novavision-secret-output-viewer",
    version="0.3.0",
    author="DigiNova",
    author_email="info@diginova.com.tr",
    description=(
        "Decrypts and consumes trusted Environment Secrets Store payloads."
    ),
    license="MIT",
    install_requires=[
        "cryptography>=41,<47",
    ],
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
