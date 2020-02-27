from PyQt5 import QtWidgets, QtCore, QtGui
from pprint import pprint

tops = ['a', 'b', 'c', 'd']
dic = {ind: [str(ord(ind)), str(ord(ind)+5)] for ind in tops}

class MyListWidget(QtWidgets.QTreeWidget):
    def __init__(self, *args, **kwargs):
        super(MyListWidget, self).__init__(*args, **kwargs)
        self.setMinimumSize(400,400)
        self.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.setAlternatingRowColors(False)
        self.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.setObjectName("treeWidget")
        self.headerItem().setText(0, "1")
        self.header().setVisible(False)
        self.deselected = []
        self.expandAll()
        self.itemClicked.connect(self.root_selections)

    def iterTreeWidgetItems(self, root=None):
        """Iterate through all items in a QTreeWidget
        Args:
            treewidget (QTreeWidget): QTreeWidget to Iterate.
            root (None or QTreeWidgetItem): start point.
        Returns:
            yield each item found.
        """

        if root is None:
            root = self.invisibleRootItem()
        stack = [root]
        while stack:
            parent = stack.pop(0)
            for row in range(parent.childCount()):
                child = parent.child(row)
                yield child
                if child.childCount() > 0:
                    stack.append(child)

    def root_selections(self,current, column):
        """ de/seleziona tutti i figli se si seleziona il root,
        se tutti i figli sono selezionati ma non tramite root (uno alla volta)
        anche il root viene selezionato allo scopo di facilitare la deselezione
        di tutti i figli quando viene deselezionato il root"""
        item = current
        has_dad = item.parent()
        children_num = item.childCount() if not has_dad else 0
        children = [item.child(num) for num in range(children_num) if not has_dad]
        if has_dad:
            siblings = [has_dad.child(num) for num in range(has_dad.childCount())]
            siblings.remove(item)
        else:
            siblings = []
        if not item.isSelected():
            if children:
                for child in children:
                    child.setSelected(False)
            else:
                tutti = True
                for it in siblings:
                    if not it.isSelected():
                        tutti = False
                if tutti:
                    has_dad.setSelected(False)
        else:
            if children:
                for child in children:
                    child.setSelected(True)
            else:
                tutti = True
                for it in siblings:
                    if not it.isSelected():
                        tutti = False
                if tutti:
                    has_dad.setSelected(True)



if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = QtWidgets.QMainWindow()
    ui.setMinimumSize(400,400)
    grid = QtWidgets.QGridLayout(ui)
    my = MyListWidget(ui)
    for top in dic:
        item = QtWidgets.QTreeWidgetItem()
        item.setText(0, top)
        my.insertTopLevelItem(0, item)
        children = [QtWidgets.QTreeWidgetItem() for item in dic[top]]
        for child, campo in zip(children, dic[top]):
            child.setText(0, campo)
        item.addChildren(children)
    my.expandAll()
    grid.addWidget(my)
    ui.setLayout(grid)
    ui.show()
    sys.exit(app.exec_())