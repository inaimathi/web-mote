;;;; package.lisp

(defpackage #:web-mote
  (:use #:cl #:hunchentoot #:cl-who #:cl-fad #:cl-ppcre #:bordeaux-threads)
  (:import-from :trivial-shell :shell-command))

(in-package :web-mote)

;;;;;;;;;;;;;;; config variables ;;;;;;;;;;;;;;;
(defparameter *starting-directory* (make-pathname :directory '(:absolute "home" "inaimathi" "Videos")))
(defparameter *server-port* 4141)
(defparameter *target-directory* (make-pathname :directory '(:absolute "home" "inaimathi" ".mplayer")))
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


(defparameter *cmd-in* (merge-pathnames *target-directory* "in"))
(defparameter *cmd-out* (merge-pathnames *target-directory* "out"))

(defun install ()
  (progn (ensure-directories-exist *target-directory*)
	 (shell-command (format nil "mkfifo ~a" *cmd-in*))
	 (shell-command (format nil "mkfifo ~a" *cmd-out*))
	 (shell-command (format nil "chmod 777 ~a" *cmd-in*))))

(defun serve-mplayer ()
  (shell-command (format nil "tail -f ~a | mplayer -slave -idle -fs -display :0.0" *cmd-in*)))

(defvar *web-server* (start (make-instance 'hunchentoot:easy-acceptor :port *server-port*)))
(push (create-folder-dispatcher-and-handler "/icons/" "icons/") *dispatch-table*)
(push (create-static-file-dispatcher-and-handler "/web-mote.css" "web-mote.css") *dispatch-table*)
;; (serve-mplayer)