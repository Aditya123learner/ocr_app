from setuptools import setup, find_packages

setup(
    name='ocr_app',  # Name of the app
    version='0.0.1',        # Your app version
    description='OCR App for Frappe',  # A short description
    author='lmc',     # Replace with your name
    author_email='sanketshelar2002@gmail.com',  # Replace with your email
    packages=find_packages(),  # Automatically find all packages in your app
    include_package_data=True,  # Include non-Python files (e.g., images, templates, static)
    zip_safe=False,            # Set to False if your app is not safe to be zipped
    install_requires=[  
        'frappe'       # List of dependencies
      'pytesseract',          # If using Tesseract OCR, for example
        'requests',             # Example of another common dependency
        'Pillow',
        'opencv-python-headless',
    ],
)