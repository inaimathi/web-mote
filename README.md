## Web-Mote

This is a Common Lisp, web-based interface for MPlayer I put together because I felt like controlling my media center with an iPod touch that serves no other purpose.

#### Don't try to use it yet, there are still some bugs in the interface.

Ok, if you want to use it anyway, 

1. change config variables in `package.lisp` to reflect your setup
2. load `:web-mote`
3. start an `mplayer` service by evaluating `(serve-mplayer)`
4. navigate to `http://[machine ip]:[*server-port*]` to use the remote menu

Like I said, it's meant to be used through my iPod touch, so the stylesheet is specifically crafted to fit the width of the screen and be readable at that size. If you're using another device, you may need to play with the .css file. There are also a few outstanding issues that I want to deal with before I can endorse the use of this system by anyone other than me.

#### Licensing

This program is released under the GNU AGPL (check the `LICENSE` file for details).

The media player icon artwork is taken from [lucamennoia's media player icons piece](http://lucamennoia.deviantart.com/art/CustomMediaPlayer-icon-buttons-174712679) (released under [CC-NC-SA](http://creativecommons.org/licenses/by-nc-sa/3.0/), so I don't even need to attribute them, but I'm cool that way).

The folder/video/audio/image icons are from the [Crystal Clear set](http://commons.wikimedia.org/wiki/Crystal_Clear) (released under [LGPL](http://www.gnu.org/licenses/lgpl.html)).

A copy of [jQuery](http://jquery.com/) is included for ease of use. jQuery is [dual-licensed under GPL and MIT-style licenses](http://jquery.org/license/).
