#!/bin/echo To use bash-qt, put in your source file source

_qt_sig() {
	read cmd <&4
	if echo "$cmd" | egrep -q "^sig:"
	then
		eval "${cmd:4:${#cmd}-4}"
	fi
}

qt_init() {
	trap _qt_exit EXIT

	QT_IN_PIPE="$(mktemp)"
	QT_OUT_PIPE="$(mktemp)"
	rm -f "$QT_IN_PIPE" "$QT_OUT_PIPE"
	mknod --mode=600 "$QT_IN_PIPE" p
	mknod --mode=600 "$QT_OUT_PIPE" p
	./bash_qt_support.py $$ <"$QT_IN_PIPE" >"$QT_OUT_PIPE" &
	_QT_SUPPORT_PID="$!"
	exec 3>"$QT_IN_PIPE"
	exec 4<"$QT_OUT_PIPE"
	rm "$QT_IN_PIPE" "$QT_OUT_PIPE"
	QT_APP="$(qt QtGui.QApplication [])"
}

_qt_exit() {
	kill $_QT_SUPPORT_PID
}

qt() {
	line=""
	for arg in "$@"
	do
		line="$line\"$arg\" "
	done
	echo "$line" >&3
	head -1 <&4
}

qts() {
	qt "$@" >/dev/null
}

qt_signal() {
	qts signal "$@"
}

qt_sig_end() {
	qts sig_end
}

qt_exec() {
	qts exec "$QT_APP"
	while true
	do
		_qt_sig
	done
}
