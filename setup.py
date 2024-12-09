from setuptools import setup, find_packages

setup(
    name='ocr_app',  # Name of the app
    version='0.0.1',        # Your app version
    description='OCR App for Frappe',  # A short description
    author='Your Name',     # Replace with your name
    author_email='your_email@example.com',  # Replace with your email
    packages=find_packages(),  # Automatically find all packages in your app
    include_package_data=True,  # Include non-Python files (e.g., images, templates, static)
    zip_safe=False,            # Set to False if your app is not safe to be zipped
    install_requires=[         # List of dependencies
        'frappe',               # Frappe is mandatory
        'pytesseract',          # If using Tesseract OCR, for example
        'requests',             # Example of another common dependency
        'Pillow',
        'opencv-python-headless',
    ],
)