# TSE Group 15: Facebook Sentimental Analysis

When running the program for the first time please follow the instructions below:

1. Make sure you are running python 3.7.9 use the windows x86 executable installer in vs code. 
https://www.python.org/downloads/release/python-379/
In the bottom corner of vs code it should say the python version of your interpreter. if it's incorrect select a different interpreter using ctrl + shift + p -> select interpreter.

create a venv using ctrl + shift + p then create environment and select the interpreter

2. Run the following commands in the integrated terminal at the bottom of vs code:
* python -m pip install --upgrade pip
* python -m pip install -r requirements.txt

test streamlit by running in terminal:
* streamlit hello
press Enter. After it should open a web page.


To run the Streamlit app, enter into your terminal
* streamlit run app.py
The first time it may take a while downloading all the NLTK packages.

To run unit tests:
Ensure you're in the project directory, enter into terminal 'pytest'

The app is hosted using the release branch. Please see the url below:

https://joeldavidson1-tseprojectgroup15-app-release-4gxs7r.streamlit.app

## Unit testing:

Ensure you have pytest intalled, follow instructions above (already included in requirements.txt) or enter into terminal:

pip install -U pytest

To run pytest, ensure you're in the project directory and enter into terminal 'pytest'
