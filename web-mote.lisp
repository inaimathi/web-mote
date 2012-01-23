;;;; web-mote.lisp

(in-package #:web-mote)

(defparameter *commands*
  (list :pause "pause"
	:forward "seek +40"
	:rewind "seek -40"
	:stop "stop"
	:osd "osd"
	:play (lambda (f) (format nil "loadfile '~a'" f))))

(defmethod run-cmd ((cmd string) &optional arg)
  (declare (ignore arg))
   (format nil "echo \"~a\" > ~~/.mplayer/in" cmd))

(defmethod run-cmd ((cmd function) &optional arg)
   (format nil "echo \"~a\" > ~~/.mplayer/in" (funcall cmd arg)))

(defun prev-dir (dir)
  (make-pathname :directory (pathname-directory (pathname-as-file dir))))

(defun to-string (obj) (format nil "~a" obj))

(defun directory? (file) (directory-exists-p file))
(defun video? (file) (scan "(mp4|flv|avi|ogv)$" (to-string file)))
(defun audio? (file) (scan "(mp3|ogg|wav)$" (to-string file)))

(defun entry-list (entries)
  (with-html-output (*standard-output* nil :indent t)
    (loop for e in entries
	  do (htm 
	      (:a :href (cond ((directory? e) 
			       (format nil "/?dir=~a" e))
			      ((or (audio? e) (video? e)) 
			       (format nil "/command?cmd-name=play&file-name=~a" e))
			      (t "#"))
		  (:li (:img :src (cond ((directory? e) "/icons/folder.png")
					((video? e) "/icons/video.png")
					((audio? e) "/icons/audio.png")))
		       (str e)))))))

(defun dir-list (directory)
  (let* ((raw-list (list-directory directory))
	 (dirs (remove-if-not #'directory-exists-p raw-list))
	 (files (remove-if #'directory-exists-p raw-list)))
    (with-html-output (*standard-output* nil :indent t)
      (:ul (when (not (string= directory *starting-directory*)) 
	     (htm (:a :href (format nil "/?dir=~a" (prev-dir directory)) 
		      (:li (:img (:src "/icons/folder.png")) ".."))))
	   (entry-list dirs)
	   (entry-list files)))))


(defmacro page-template ((&key title) &body body)
  `(with-html-output-to-string (*standard-output* nil :prologue t :indent t)
     (:html :xmlns "http://www.w3.org/1999/xhtml" :xml\:lang "en" :lang "en"
	    (:head (:meta :http-equiv "Content-Type" :content "text/html;charset=utf-8")
		   (:title ,title))
	    (:body ,@body))))

(define-easy-handler (control-panel :uri "/") (dir)
  (page-template (:title "Web Mote - Control Panel")
    (dir-list (or dir *starting-directory*))))

(define-easy-handler (handle-command :uri "/command") (cmd-name file-name)
  (format nil "command: ~a || file: ~a" cmd-name file-name))

