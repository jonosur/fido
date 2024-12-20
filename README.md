[![Language](https://img.shields.io/badge/language-Python-green.svg?style=for-the-badge)](http://www.python.org)
[![MIT](https://shields.io/badge/license-MIT-green?style=for-the-badge)](https://choosealicense.com/licenses/mit/)
[![Issues](https://img.shields.io/github/issues/jonosur/fido?style=for-the-badge)](https://github.com/jonosur/fido/issues)

### FIDO

fido.py fetches LUSERS, MAP, MOTD, LIST for servers in the list and stores the results. 

Make sure you have pendulum installed.

Edit the fido.py's following hardset variables.
```
server_list = ['irc.server1.com:6667', 'irc.server2.com:6667']
server_index = 0
channel = "#services"
nickname = "fido"
realname = "i fetch MOTD, LUSERS, MAP, and LIST."
data_dir = "./data"
#change this to 0 or bot will not load.
die = 1
```

Tested using Python3.
```
=================================================================
             .       ..
   oec :    @88>   dF
  @88888    %8P   '88bu.             u.
  8"*88%     .    '*88888bu    ...ue888b
  8b.      .@88u    ^"*8888N   888R Y888r
 u888888> ''888E`  beWE "888L  888R I888>
  8888R     888E   888E  888E  888R I888>
  8888P     888E   888E  888E  888R I888>
  *888>     888E   888E   888F u8888cJ888
  4888      888&  .888N..888   "*888*P"
  '888      R888"  `"888*""      'Y"
   88R       ""       ""
   88>
   48       v1
   '8

=================================================================
usage: fido.py [-h] [--time TIME]

i fetch MOTD, LUSERS, MAP, and LIST.

optional arguments:
  -h, --help   show this help message and exit
  --time TIME  Duration to stay connected in seconds.
=================================================================
```

