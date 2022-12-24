#INI FILE HANYA KETIKA DI HOSTING AJA UNTUK MANGGIL WSGI APP NYA
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from eperpu.wsgi import application
