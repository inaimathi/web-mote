## Web-Mote

This is a currently Python, web-based interface for MPlayer I put together because I felt like controlling my RasPi-based media center with an iPod touch that serves no other purpose.

The latest re-write of the system was done for the purposes of exploring some UI construction techniques. Writeups available in

[Part 1](http://langnostic.blogspot.ca/2012/10/webmote-right-way.html) and [Part 2](http://langnostic.blogspot.ca/2012/10/webmote-right-way-part-2-or-controlling.html)

#### Usage

1. install Python 2.7 (if you're on Debian, you already have it)
2. run `python web-mote.py` (if you want it running in the background, use `screen`)
3. navigate to `http://[machine ip]:8080` to use the remote menu

Like I said, it's meant to be used through my iPod touch, so the stylesheet is specifically crafted to fit the width of the screen and be readable at that size. If you're using another device, you may need to play with the .css file. There are also a few outstanding issues that I want to deal with before I can endorse the use of this system by anyone other than me.

#### Licensing/Components
*(Why is this always the longest section?)*

This program is released under the GNU AGPL (check the `LICENSE` file for details).

The front-end uses [Twitter Bootstrap](https://github.com/twitter/bootstrap) for styling and icons, which is released under the [Apache License](https://github.com/twitter/bootstrap/blob/master/LICENSE)

A previous version used artwork from the [famfamfam SILK Icon set](http://www.famfamfam.com/lab/icons/silk/), which are released under [CC-BY 2.5](http://creativecommons.org/licenses/by/2.5/)

A previous version used artwork from [lucamennoia's media player icons piece](http://lucamennoia.deviantart.com/art/CustomMediaPlayer-icon-buttons-174712679) (released under [CC-NC-SA](http://creativecommons.org/licenses/by-nc-sa/3.0/), so I didn't even need to attribute them, but I'm cool that way).

The folder/video/audio/image icons are from the [Crystal Clear set](http://commons.wikimedia.org/wiki/Crystal_Clear) (released under [LGPL](http://www.gnu.org/licenses/lgpl.html)).

A copy of [jQuery](http://jquery.com/) and [jQueryUI](http://jqueryui.com/) are included for ease of use. Both are [dual-licensed under GPL and MIT-style licenses](http://jquery.org/license/).

The system uses [backbone.js](http://backbonejs.org/) (and therefore also [underscore.js](http://underscorejs.org/)) for the purposes of internal routing. Both are released under the [MIT-style Expat license](https://github.com/documentcloud/backbone/blob/master/LICENSE)

[handlebars.js](http://handlebarsjs.com/) is used for HTML templating. It is released under an [MIT-style Expat license](https://github.com/wycats/handlebars.js/blob/master/LICENSE).
