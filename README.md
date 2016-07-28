# loadtweets
A simple python3 script that allows the user to load all tweets of an account.  
If rerun, the program will detect if newer tweets have been created and update the data.  
The result is stored as a list of IDs and tweet texts using the JSON format.

## Requirements
To run the script, you need python-twitter.  
Installation with pip:
````
pip install twitter
````

## Configuration
Use the included file to edit your configuration.
Valid access tokens are required to connect to the Twitter API.
[Here's how to get them](https://python-twitter.readthedocs.io/en/latest/getting_started.html)

## Execution
Simply run the following line:
```
python3 load_tweets.py
```
