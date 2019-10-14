import abc


class Color_MPBStrategyAbstract(object):
    """You do not need to know about metaclasses.
    Just know that this is how you define abstract
    classes in Python."""
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def show_color(self):
        """Required Method"""

    @abc.abstractmethod
    def nome(self):
        """Required Method"""




class Red_ColorMPBStrategy(Color_MPBStrategyAbstract):
    DEFAULTSTYLE = """
            QProgressBar::chunk {background-color:qlineargradient(spread:reflect, x1:1, y1:0, x2:0.500455, y2:0, stop:0.414773 rgba(255, 255, 255, 20), stop:1 rgba(255, 20, 20, 46))}
            QProgressBar{border: 0px solid red;background-color: rgba(255, 255, 255,0);};
            font: 175 16pt \"MS Shell Dlg 2\";
            """
    NOME = "RED progress button"

    def show_color(self):
        # print("quack!")
        return self.DEFAULTSTYLE

    def nome(self):
        # print(self.NOME)
        return self.NOME
        # return self.nome


class Green_ColorMPBStrategy(Color_MPBStrategyAbstract):
    DEFAULTSTYLE = """
        QProgressBar::chunk {background-color:qlineargradient(spread:reflect, x1:1, y1:0, x2:0.500455, y2:0, stop:0.414773 rgba(255, 255, 255, 20), stop:1 rgba(0, 255, 61, 255))}
        QProgressBar{border: 0px solid red;background-color: rgba(255, 255, 255,0);};
        font: 175 16pt \"MS Shell Dlg 2\";
        """
    NOME = "GREEN progress button"
    def show_color(self):
        # print("quack!")
        return self.DEFAULTSTYLE

    def nome(self):
        return self.NOME


class Text_MPBStrategyAbstract(object):
    """You do not need to know about metaclasses.
    Just know that this is how you define abstract
    classes in Python."""
    __metaclass__ = abc.ABCMeta

    # @abc.abstractmethod
    # def setText(self,text):
    #     """Required Method"""
    # @abc.abstractmethod
    # def setText(self,text):
    #


class NoteText_MPBStrategy(Text_MPBStrategyAbstract):
    _text = 'Note'

    # def setText(self,text):
    #     self._text = text


class SpeseText_MPBStrategy(Text_MPBStrategyAbstract):
    _text = 'Spese'

    # def setText(self, text):
    #     self._text = text
