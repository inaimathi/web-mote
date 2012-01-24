;;;; package.lisp

(defpackage #:web-mote
  (:use #:cl #:hunchentoot #:cl-who #:cl-fad #:cl-ppcre)
  (:import-from :trivial-shell :shell-command))

(in-package :web-mote)

(defparameter *starting-directory* (make-pathname :directory '(:absolute "home" "inaimathi" "Videos")))

(defvar *web-server* (start (make-instance 'hunchentoot:easy-acceptor :port 4141)))

(defparameter *server-port* 4141)
(defparameter *target-directory* (make-pathname :directory '(:absolute "home" "inaimathi" ".mplayer")))
(defparameter *cmd-in* (merge-pathnames *target-directory* "in"))
(defparameter *cmd-out* (merge-pathnames *target-directory* "out"))

(defun install ()
  (progn (ensure-directories-exist *target-directory*)
	 (shell-command (format nil "mkfifo ~a" *cmd-in*))
	 (shell-command (format nil "mkfifo ~a" *cmd-out*))
	 (shell-command (format nil "chmod 777 ~a" *cmd-in*))))

(defun serve-mplayer ()
  (shell-command (format nil "tail -f ~a | mplayer -slave -idle -fs -vc ffh264vdpau,ffmpeg12vdpau,ffvc1vdpau,ffwmv3vdpau, -ao alsa:device=hw=0.3 -display :0.0 |  cat > ~a" *cmd-in* *cmd-out*)))

(defvar *web-server* (start (make-instance 'hunchentoot:easy-acceptor :port *server-port*)))
;; (serve-mplayer)