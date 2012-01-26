;;;; web-mote.asd

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

(asdf:defsystem #:web-mote
  :serial t
  :depends-on (#:cl-fad
               #:cl-who
               #:hunchentoot
               #:cl-ppcre
               #:trivial-shell
	       #:bordeaux-threads)
  :components ((:file "package")
               (:file "web-mote")))

