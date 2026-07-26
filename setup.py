import setuptools

setuptools.setup(
    name="novavision-secret-output-viewer",
    version="0.1.0",
    author="DigiNova",
    author_email="info@diginova.com.tr",
    description="Safe Str/List output viewer for Environment Secrets Store demos.",
    license="MIT",
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
    package_dir={"novavision.package": "src"},
    python_requires=">=3.8",
)
