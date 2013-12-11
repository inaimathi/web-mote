## Web-Mote

This is a currently Python, web-based interface for MPlayer I put together because I felt like controlling my RasPi-based media center with an iPod touch that serves no other purpose.

The latest re-write of the system was done for the purposes of exploring some UI construction techniques. Writeups available in

[Part 1](http://langnostic.blogspot.ca/2012/10/webmote-right-way.html) and [Part 2](http://langnostic.blogspot.ca/2012/10/webmote-right-way-part-2-or-controlling.html)

#### Usage

1. install the dependencies
2. run `python main.py`
3. navigate to `http://[machine ip]:8080` to use the remote menu

You can run it in the background using GNU Screen. Assuming you have it installed, you start a background server with `screen -dmS web-mote python main.py`, attach to it using `screen -r web-mote` and detach with `Ctrl+a Ctrl+d`.

Like I said, it's meant to be used through my iPod touch, so the stylesheet is specifically crafted to fit the width of the screen and be readable at that size. If you're using another device, you may need to play with the .css file.

#### Dependencies

- [Python 2.7](http://python.org/download/releases/2.7/)
- [mplayer](http://www.mplayerhq.hu/design7/news.html)
- OPTIONALLY [omxplayer](https://github.com/huceke/omxplayer) *if you're on [Raspbian](http://www.raspbian.org/), you already have this. If you're not, you probably don't need it.*
- OPTIONALLY [GNU Screen](http://www.gnu.org/software/screen/) *you'll need this or similar to run web-mote in the background*
- Python [tornado](http://www.tornadoweb.org/) module

If you're on Debian or Raspbian, you can install everything you need by running the following as `root`:

    apt-get install mplayer screen python-setuptools
    easy_install tornado

#### Licensing/Components
*(Why is this always the longest section?)*

This program is released under the GNU AGPL (check the `LICENSE` file for details).

The favicon is a remote control icon designed by [FatCow - Udderly Fantastic Hosting](http://www.fatcow.com/) and released under [CC-BY 3.0](http://creativecommons.org/licenses/by/3.0/us/)

The folder/video/audio/image icons are from the [Crystal Clear set](http://commons.wikimedia.org/wiki/Crystal_Clear) (released under [LGPL](http://www.gnu.org/licenses/lgpl.html)).

A copy of the [Elm language](http://elm-lang.org/) runtime is included for ease of use. It's released under an [Expat-style license](https://github.com/evancz/Elm/blob/master/LICENSE).
