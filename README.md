# pyhidentity
[![Build Status](https://travis-ci.org/bierschi/pyhidentity.svg?branch=master)](https://travis-ci.org/bierschi/pyhidentity) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/bierschi/pyhidentity/blob/master/LICENSE) <br>

pyhidentity is a **py**thon based library to **hide** your **identity**

included features within this library:

 - make requests over the tor network 
 - make requests from a selectable pool of proxies
 - easily renew your public ip address
 
 
## installation
install from source with: 

<pre><code>
sudo python3 setup.py install
</code></pre>

## usage



## tor dependency and settings
install tor with apt
<pre><code>
sudo apt install tor
</code></pre>

edit the torrc file in `/etc/tor`
<pre><code>

</code></pre>


## privoxy

<pre><code>
sudo apt install privoxy
</code></pre>

## add user 

<pre><code>
sudo usermod -a -G debian-tor "username"
</code></pre>


## Changelog
All changes and versioning information can be found in the [CHANGELOG](https://github.com/bierschi/pyhidentity/blob/master/CHANGELOG.rst)

## License
Copyright (c) 2019 Bierschneider Christian. See [LICENSE](https://github.com/bierschi/pyhidentity/blob/master/LICENSE)
for details