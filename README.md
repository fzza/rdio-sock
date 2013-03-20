# Rdio-Sock #
Unofficial Rdio WebSocket Library

**Very early development, Expect major changes without notice**

Documentation available at http://rdio-sock.readthedocs.org

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

## Current State ##

**This library *does not* directly support playing tracks**,
You will require an RTMPe client / library to stream tracks yourself.
We do plan to implement the needed methods to receive track playback info *soon*.

**This library *does* support remotely controlling an Rdio client and will expose all the
internal methods used by the Rdio client (playlists, metadata, etc..)**,
The currently implemented functions are listed below, check out the *To Do / Finish* list
below for features / services that are currently being implemented or are planned to be implemented.

### Implemented Functions ###
 - **Media controls** - Play, pause and skip tracks
 - **Currently playing** - View the currently playing track *(PubSub updates)*
 - **Queue** - View the current play queue *(PubSub updates)*

## To Do / Finish ##

**[S]** *rdiosock.metadata* - **Implemented Methods :** `search`    
**[--]** *rdiosock.user*    

**[--]** *rdiosock.services.collaborators*    
**[--]** *rdiosock.services.chat*     
**[--]** *rdiosock.services.playlists*    
**[--]** *rdiosock.services.presence*      
**[--]** *rdiosock.services.subscribers*    

---------

**[--] = Not Started**   
**[S] = Started, needs to be finished**

## News ##
**2013/03/20** - Documentation now available at http://rdio-sock.readthedocs.org    
**2013/03/12** - `RdioAlbum, RdioArtist, RdioList` objects added, Rdio `objects` hierarchy + parsing has been optimized, `metadata.search()` now returns results via `RdioList` object      
**2013/03/11** - Added `metadata.search()`, faster song change events, asynchronous web requests (currently only used for `getPlayerState` requests)  
**2013/03/04** - *rdiosock.remote* (now merged with *rdio.player*) implemented with most media controls    
**2013/03/02** - Started work on actual library    
**2013/03/02** - Working Prototype    
