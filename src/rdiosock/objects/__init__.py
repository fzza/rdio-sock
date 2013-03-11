from rdiosock.objects.album import RdioAlbum
from rdiosock.objects.artist import RdioArtist
from rdiosock.objects.person import RdioPerson
from rdiosock.objects.track import RdioTrack

DATA_TYPE_CLASSES = {
    'a': RdioAlbum,
    'al': RdioAlbum,  # TODO: Investigate why there is 'al' and 'a'
    'r': RdioArtist,
    't': RdioTrack,
    's': RdioPerson
}
