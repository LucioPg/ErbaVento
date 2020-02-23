class Red_ColorMPBStrategy:
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


class Green_ColorMPBStrategy:
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


class NoteText_MPBStrategy:
    _text = 'Note'

    # def setText(self,text):
    #     self._text = text


class SpeseText_MPBStrategy:
    _text = 'Spese'

    # def setText(self, text):
    #     self._text = text
