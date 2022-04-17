from PyQt5.QtWidgets import *
import json

# creating window
app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Items')
main_win.resize(700, 500)

# creating text
lab_film = QLabel('List items')
lab_tag = QLabel('List tags')

# creating input fields
field_text = QTextEdit()
list_film = QListWidget()
list_tag = QListWidget()
searce_tag = QLineEdit()
searce_tag.setPlaceholderText('Enter tag...')

# creating buttons
btn_ap_fl = QPushButton('Append item')
btn_del_fl = QPushButton('Delete item')
btn_sv_fl = QPushButton('Save item')
btn_ap_tg = QPushButton('Append tag')
btn_del_tg = QPushButton('Delete tag')
btn_sr_tg = QPushButton('Searce tag')

# creating guide lines
lay_main = QHBoxLayout()
col = QVBoxLayout()
row1 = QHBoxLayout()
row2 = QHBoxLayout()

# adding widgets on layouts
row1.addWidget(btn_ap_fl)
row1.addWidget(btn_del_fl)
row2.addWidget(btn_ap_tg)
row2.addWidget(btn_del_tg)

col.addWidget(lab_film)
col.addWidget(list_film)
col.addLayout(row1)
col.addWidget(btn_sv_fl)

col.addWidget(lab_tag)
col.addWidget(list_tag)
col.addWidget(searce_tag)
col.addLayout(row2)
col.addWidget(btn_sr_tg)


def show_item(): # showing item data from json file
    key = list_film.selectedItems()[0].text()
    field_text.setText(notes[key]['text'])
    list_tag.clear()
    list_tag.addItems(notes[key]['tags'])


def add_item(): # adding item in json file
    fl_name, ok = QInputDialog.getText(main_win, 'Append item', 'Name item')
    if ok and fl_name != '':
        notes[fl_name] = {'text': '', 'tags': []}
        list_film.addItem(fl_name)
        list_tag.addItems(notes[fl_name]['tags'])


def save_item(): # saving item data in json file
    if list_film.selectedItems():
        key = list_film.selectedItems()[0].text()
        notes[key]['text'] = field_text.toPlainText()
        with open('notes.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)


def del_win(): # creating a confirmation window
    msb = QMessageBox()
    msb.setWindowTitle('Exactly')
    msb.setText('You definitely want to delete the item')
    msb.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msbinf = msb.exec()
    if msbinf == QMessageBox.Ok:
        del_item()


def del_item(): # deleting an item from a file
    if list_film.selectedItems():
        key = list_film.selectedItems()[0].text()
        del notes[key]
        list_film.clear()
        list_tag.clear()
        field_text.clear()
        list_film.addItems(notes)
        with open('notes.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)


def add_tag(): # adding a tag to an item
    if list_film.selectedItems():
        key = list_film.selectedItems()[0].text()
        tag = searce_tag.text()
        if not tag in notes[key]['tags']:
            notes[key]['tags'].append(tag)
            list_tag.addItem(tag)
            searce_tag.clear()
        with open('notes.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)


def del_tag(): # deleting tag
    if list_film.selectedItems():
        key = list_film.selectedItems()[0].text()
        tag = list_tag.selectedItems()[0].text()
        notes[key]['tags'].remove(tag)
        list_tag.clear()
        list_tag.addItems(notes[key]['tags'])
        with open('notes.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)


def searc_tag(): # search for an item by tags
    tag = searce_tag.text()
    if btn_sr_tg.text() == 'Searce tag' and tag:
        notes_filt = {}
        for note in notes:
            if tag in notes[note]['tags']:
                notes_filt[note] = notes[note]
        btn_sr_tg.setText('Reset search')
        list_film.clear()
        list_tag.clear()
        field_text.clear()
        list_film.addItems(notes_filt)
    elif btn_sr_tg.text() == 'Reset search':
        searce_tag.clear()
        list_film.clear()
        list_tag.clear()
        field_text.clear()
        list_film.addItems(notes)
        btn_sr_tg.setText('Searce tag')
    else:
        pass


# button click processing
list_film.itemClicked.connect(show_item)
btn_ap_fl.clicked.connect(add_item)
btn_sv_fl.clicked.connect(save_item)
btn_del_fl.clicked.connect(del_win)
btn_ap_tg.clicked.connect(add_tag)
btn_del_tg.clicked.connect(del_tag)
btn_sr_tg.clicked.connect(searc_tag)

# also adding widgets on layouts
lay_main.addWidget(field_text)
lay_main.addLayout(col)
main_win.setLayout(lay_main)

# read file and transferring values to a variable
with open('notes.json', 'r') as f:
    notes = json.load(f)

list_film.addItems(notes)

# set style for beauty
style = """
QPushButton{
    font-size:15px;
}
QLineEdit{
    font-size:15px;
}
QLabel{
    font-size:15px;
}
QTextEdit{
    font-size:15px;
}
QListWidget{
    font-size:15px;
}
"""
app.setStyleSheet(style)
main_win.show()
app.exec_()