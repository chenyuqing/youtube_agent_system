from setuptools import setup, find_packages

setup(
    name="youtube_agent_system",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.103.1",
        "uvicorn==0.23.2",
        "python-multipart==0.0.6",
        "python-dotenv==1.0.0",
        "openai==1.3.7",
        "requests==2.31.0",
        "google-api-python-client==2.108.0",
        "google-auth-oauthlib==1.1.0",
        "google-auth-httplib2==0.1.1",
        "numpy==1.24.3",
        "pandas==1.5.3",
        "python-jose==3.3.0",
        "passlib==1.7.4",
        "bcrypt==4.0.1",
        "pydantic>=1.10.0,<2.0.0",
    ],
    python_requires=">=3.8,<3.11",
)
