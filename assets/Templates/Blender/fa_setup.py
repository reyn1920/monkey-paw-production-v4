from setuptools import setup, find_packages

# Load the README for the long description
with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="traeai",
    version="1.0.0-alpha",
    author="The TRAE.AI Open Source Team",
    description="The complete, autonomous, and free AI teammate for software development.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/trae-ai/trae-ai",  # Placeholder URL
    packages=find_packages(),
    # This is the crucial part: it gathers all dependencies we've discussed
    install_requires=[
        "fastapi[all]",
        "psutil",
        "chromadb",
        "sentence-transformers",
        "ollama",
        "pandas",
        "evidently",
        "great-expectations",
        "shap",
        "lime",
        "captum",
        "torch",
        "streamlit",
        "gradio",
        "typer[all]",
    ],
    # This creates the powerful `traeai` command in your terminal
    entry_points={
        "console_scripts": [
            "traeai = trae_ai.cli.main:app",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
