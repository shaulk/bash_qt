#!/bin/bash

source bash_qt.sh

qt_init

shell_clicked() {
	echo "Line=`qt $lineedit.text`"
	qts sig_end
}

msgbox_clicked() {
	qts QtGui.QMessageBox.information null "Textbox Contents" "`qt $lineedit.text`"
	qts sig_end
}

window=`qt QtGui.QWidget`
vbox=`qt QtGui.QVBoxLayout`
hbox=`qt QtGui.QHBoxLayout`
button1=`qt QtGui.QPushButton 'Print in shell'`
button2=`qt QtGui.QPushButton 'Display in MessageBox'`
lineedit=`qt QtGui.QLineEdit`
qt_signal $button1 "clicked()" shell_clicked
qt_signal $button2 "clicked()" msgbox_clicked
qts ${hbox}.addWidget $button1
qts ${hbox}.addWidget $button2
qts ${vbox}.addWidget $lineedit
qts ${vbox}.addLayout $hbox
qts ${window}.setLayout $vbox
qts ${window}.setWindowTitle "Simple bash-Qt Test Program"

qts ${window}.show
qt_exec
