"""
    start.py
    ~~~~~~
    Starter File
    Created By : Pankaj Suthar
"""
from src.server import app

"""
host = localhost or 0.0.0.0
port  Default 5000
"""
if __name__ == "__main__":
    app.run(host="localhost", port=5000)
