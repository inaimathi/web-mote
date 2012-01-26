;;;; web-mote.lisp

;; This file is part of :web-mote.

;; :web-mote is free software: you can redistribute it and/or modify
;; it under the terms of the GNU Affero General Public License as published by
;; the Free Software Foundation, either version 3 of the License, or
;; (at your option) any later version.

;; :web-mote is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;; GNU Affero General Public License for more details.

;; You should have received a copy of the GNU Affero General Public License
;; along with :web-mote.  If not, see <http://www.gnu.org/licenses/>.

(in-package #:web-mote)

(defparameter *commands*
  (list :rewind "seek -40"
	:pause "pause"
	:forward "seek +40"
	:stop "stop"
	:play (lambda (f) (format nil "loadfile '~a'" f))
	
	;; :mute "mute 0"
	
	:quiet "volume -1"
	:loud "volume +1"))

(defparameter *ui-bar* (list :rewind :pause :forward :stop))
(defparameter *volume-bar* (list :quiet :loud))

(defmethod run-cmd ((cmd string) &optional arg)
  (declare (ignore arg))
  (shell-command (format nil "echo \"~a\" > ~a" cmd *cmd-in*)))

(defmethod run-cmd ((cmd function) &optional arg)
  (shell-command (format nil "echo \"~a\" > ~a" (funcall cmd arg) *cmd-in*)))

(defun ajax-command (cmd &optional file-name) 
  (format nil "$.post(\"/command\", {\"cmd-name\": \"~a\"~@[, \"file-name\": \"~a\"~]})"
	  cmd file-name))

(defun prev-dir (dir) (make-pathname :directory (pathname-directory (pathname-as-file dir))))

(defun to-string (obj) (format nil "~a" obj))

(defun directory? (file) (directory-exists-p file))
(defun video? (file) (scan "(mpg|mpeg|m4v|mov|wmv|mp4|flv|avi|ogv)$" (to-string file)))
(defun audio? (file) (scan "(mp3|ogg|wav)$" (to-string file)))
(defun image? (file) (scan "(png|gif|jpg|jpeg|tiff)$" (to-string file)))

(defun video-length (video-file) 
  (scan-to-strings "duration: (\\d+?)" 
		   (shell-command (format nil "mplayer -vo null -ao null -frames 0 -identify '~a'" video-file))))

(defun entry-list (entries)
  (with-html-output (*standard-output* nil :indent t)
    (loop for e in entries
	  do (single-entry e))))

(defun single-entry (entry)
  (with-html-output (*standard-output* nil :indent t)
    (:a :href (if (directory? entry) (format nil "/?dir=~a" entry) "javascript:void(0);")
	:onclick (when (or (video? entry) (audio? entry)) (ajax-command :play (to-string entry)))
	(:li (:img :src (entry-icon entry) (:span (str (file-namestring (pathname-as-file entry)))))))))

(defun entry-icon (entry)
  (cond ((directory? entry) "/icons/folder.png")
	((video? entry) "/icons/video.png")
	((audio? entry) "/icons/audio.png")))

(defun dir-list (directory)
  (let* ((raw-list (list-directory directory))
	 (dirs (remove-if-not #'directory-exists-p raw-list))
	 (files (remove-if #'directory-exists-p raw-list)))
    (with-html-output (*standard-output* nil :indent t)
      (:ul :class "file-list"
	   (when (not (string= (to-string directory) (to-string *starting-directory*))) 
	     (htm (:a :href (format nil "/?dir=~a" (prev-dir directory)) 
		      (:li (:img :src "/icons/folder.png") ".."))))
	   (entry-list dirs)
	   (entry-list files)))))


(defmacro page-template ((&key title) &body body)
  `(with-html-output-to-string (*standard-output* nil :prologue t :indent t)
     (:html :xmlns "http://www.w3.org/1999/xhtml" :xml\:lang "en" :lang "en"
	    (:head (:meta :http-equiv "Content-Type" :content "text/html;charset=utf-8")
		   (:link :href "/web-mote.css" :rel "stylesheet" :type "text/css" :media "screen")
		   (:script :type "text/javascript" :src "/jquery.js")
		   (:title ,title))
	    (:body ,@body))))

(define-easy-handler (control-panel :uri "/") (dir)
  (page-template (:title "Web Mote - Control Panel")
    (loop for c in *ui-bar*
	  do (htm (:a :class "cmd-button" :href "javascript:void(0);"
		      :onclick (ajax-command c)
		      (:img :src (format nil "/icons/~(~a~)-normal.png" c)))))
    (:br :class "clear")
    (dir-list (or dir *starting-directory*))))

(define-easy-handler (handle-command :uri "/command") (cmd-name file-name)
  (format nil "command: ~a" (run-cmd (getf *commands* (intern (string-upcase cmd-name) :keyword)) file-name)))