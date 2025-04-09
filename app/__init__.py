# app/__init__.py
from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file

app = Flask(__name__)
