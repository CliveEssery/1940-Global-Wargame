"""
Code illustration: 4.01

@ Tkinter GUI Application Development Blueprints
"""
from constants import *
import model as mod


class application():

    def __init__(self):
        self.init_model()

    def init_model(self):
        self.model = mod.Model(filename='.json',path='.',move=0)
