# rdio-sock #
Unofficial Rdio WebSocket Library

**Very early development, Expect major changes without notice or documentation**

## License ##

    rdio-sock - Rdio WebSocket Library
    Copyright (C) 2013  fzza- <fzzzzzzzza@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

## Todo ##

#### Core ####
*rdiosock.metadata* - Access Rdio music metadata (searching, lookup, etc...)    
*rdiosock.player* - Local Rdio music player    
*rdiosock.remote* - Remotely control an Rdio music player **(Media controls working, No PubSub events handled yet)**     
*rdiosock.user* - User information (details, collection, playlists, friends/following, notifications)

#### PubSub Services ####
*rdiosock.services.collaborators*    
*rdiosock.services.chat*    
*rdiosock.services.fields*    
*rdiosock.services.player*   
*rdiosock.services.playlists*    
*rdiosock.services.presence*    
*rdiosock.services.private* **(`publish_command` implemented)**    
*rdiosock.services.subscribers*    

## News ##
**2013/03/04** - *rdiosock.remote* implemented with most media controls    
**2013/03/02** - Started work on actual library    
**2013/03/02** - Working Prototype    

## Example ##

Simple example showing current functionality as of **2013/03/04**

	>>> rdio = RdioSock()
	>>> rdio.user.login("<username>", "<password>")
	[...snip...]

	>>> rdio.pubsub.connect()
    [RdioPubSubClient] using server : 8.18.203.81:8080
    [RdioPubSubClient] opened
    [RdioPubSubClient] send_message CONNECT [...snip...]
    [RdioPubSub] received_message: CONNECTED [...snip...]

    >>> rdio.remote.volume = 0.7
    [RdioPubSubClient] send_message PUB s*******/private|{"command": {"type": "set", "key": "volume", "value": 0.7}, "event": "remote"}

    >>> rdio.remote.pause()
    [RdioPubSubClient] send_message PUB s*******/private|{"command": {"type": "pause"}, "event": "remote"}
	
	>>> rdio.remote.play()
	[RdioPubSubClient] send_message PUB s*******/private|{"command": {"type": "play"}, "event": "remote"}

	>>> rdio.remote.shuffle = True
	[RdioPubSubClient] send_message PUB s*******/private|{"command": {"type": "set", "key": "shuffle", "value": true}, "event": "remote"}

	>>> rdio.remote.repeat = rdio.remote.REPEAT_ALL
	[RdioPubSubClient] send_message PUB s*******/private|{"command": {"type": "set", "key": "repeat", "value": 2}, "event": "remote"}