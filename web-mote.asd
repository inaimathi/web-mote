;;;; web-mote.asd

(asdf:defsystem #:web-mote
  :serial t
  :depends-on (#:cl-fad
               #:cl-who
               #:hunchentoot
               #:cl-ppcre
               #:trivial-shell)
  :components ((:file "package")
               (:file "web-mote")))

