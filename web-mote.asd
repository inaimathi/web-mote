;;;; web-mote.asd

(asdf:defsystem #:web-mote
  :serial t
  :depends-on (#:cl-fad
               #:cl-who
	       #:parenscript
               #:hunchentoot
               #:cl-ppcre
               #:trivial-shell
	       #:bordeaux-threads)
  :components ((:file "package")
               (:file "web-mote")))

