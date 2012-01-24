## Web-Mote

This is a Common Lisp, web-based interface for MPlayer I put together because I felt like controlling my media center with an iPod touch that serves no other purpose.

#### Don't try to use it yet, there are still some bugs in the interface.

Ok, if you want to use it anyway, 

1. change config variables in `package.lisp` to reflect your setup
2. load :web-mote
3. start an `mplayer` service by evaluating `(defparameter *mplayer* (make-thread (shell-command (format nil "tail -f ~a | mplayer -slave -idle -fs -display :0.0" *cmd-in*))))`
4. navigate to `http://[machine ip]:[*server-port*]` to use the remote menu

Like I said, it's meant to be used through my iPod touch, so the stylesheet is specifically crafted to fit the width of the screen and be readable at that size. If you're using another device, you may need to play with the .css file. There are also a few outstanding issues that I want to deal with before I can endorse the use of this system by anyone other than me.
