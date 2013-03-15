#!/bin/bash

source bash_qt.sh

qt_init

clicked() {
	echo "Button clicked."
	qts sig_end
}

button=`qt QtGui.QPushButton 'Hello, World!'`
qts ${button}.show
qt_signal $button "clicked()" clicked
qt_exec
