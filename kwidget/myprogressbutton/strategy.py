import abc


class Color_MPBStrategyAbstract(object):
    """You do not need to know about metaclasses.
    Just know that this is how you define abstract
    classes in Python."""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def show_color(self):
        """Required Method"""


class Red_ColorMPBStrategy(Color_MPBStrategyAbstract):
    def show_color(self):
        print("QUACK! QUACK!!")


class Green_ColorMPBStrategy(Color_MPBStrategyAbstract):
    def show_color(self):
        print("quack!")


class Text_MPBStrategyAbstract(object):
    """You do not need to know about metaclasses.
    Just know that this is how you define abstract
    classes in Python."""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def setText(self):
        """Required Method"""


class NoteText_MPBStrategy(Text_MPBStrategyAbstract):

    def __init__(self):
        self._text = None

    def setText(self):
        self._text = 'Note'


class SpeseText_MPBStrategy(Text_MPBStrategyAbstract):
    _text = None

    def setText(self):
        self._text = 'Spese'
