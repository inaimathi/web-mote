;;;; package.lisp

(defpackage #:web-mote
  (:use #:cl #:hunchentoot #:cl-who #:cl-fad #:cl-ppcre)
  (:import-from :trivial-shell :shell-command))

(in-package :web-mote)

(defparameter *starting-directory* "/home/inaimathi/Videos/")

(defvar *web-server* (start (make-instance 'hunchentoot:easy-acceptor :port 4141)))