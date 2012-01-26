;;;; package.lisp

(defpackage #:web-mote
  (:use #:cl #:hunchentoot #:cl-who #:parenscript #:cl-fad #:cl-ppcre #:bordeaux-threads)
  (:import-from :trivial-shell :shell-command))

(in-package :web-mote)

;;;;;;;;;;;;;;; config variables ;;;;;;;;;;;;;;;
    ;;the directory that contains your media library
(defparameter *starting-directory* (make-pathname :directory '(:absolute "home" "inaimathi" "Videos")))
    ;;the directory that application-related files will be kept in
(defparameter *target-directory* (make-pathname :directory '(:absolute "home" "inaimathi" ".mplayer")))
(defparameter *server-port* 4141)
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defparameter *cmd-in* (merge-pathnames *target-directory* "in"))
(defparameter *cmd-out* (merge-pathnames *target-directory* "out"))

(defparameter *mplayer-thread* nil)

(defun mkfifo (pathname &optional (mode #o777))
  #+sbcl (sb-posix:mkfifo pathname mode)
  #+clozure (ccl::with-filename-cstrs ((p pathname))(#.(read-from-string "#_mkfifo") p mode))
  #+clisp (LINUX:mkfifo pathname mode) ;;(error "Problem with (LINUX:mkfifo ~S ~S)" pathname mode)
  #-(or sbcl clozure clisp) (error "mkfifo not implemented for your Lisp"))

(defun install ()
  (progn (ensure-directories-exist *target-directory*)
	 (mkfifo *cmd-in* #o777)
	 (mkfifo *cmd-out*)))

(defun serve-mplayer () (setf *mplayer-thread* (make-thread (shell-command (format nil "tail -f ~a | mplayer -slave -idle -fs -display :0.0" *cmd-in*)))))
(defun kill-mplayer () (destroy-thread *mplayer-thread*))

(defvar *web-server* (start (make-instance 'hunchentoot:easy-acceptor :port *server-port*)))
(push (create-folder-dispatcher-and-handler "/icons/" "icons/") *dispatch-table*)
(push (create-static-file-dispatcher-and-handler "/web-mote.css" "web-mote.css") *dispatch-table*)
(push (create-static-file-dispatcher-and-handler "/jquery.js" "js/jquery-1.7.1.min.js") *dispatch-table*)
;; (serve-mplayer)