from beets.plugins import BeetsPlugin


class PateticoPlugin(BeetsPlugin):
    album_tags = {
        'album',
        'artist',
        'label',
        'artist_sort',
        'albumdisambig',
        'releasegroupdisambig',
        'artist_credit'}

    track_tags = {
        'title',
        'artist',
        'artist_sort',
        'disctitle',
        'artist_credit',
        'lyricist',
        'composer',
        'composer_sort',
        'arranger'}

    def __init__(self):
        super(PateticoPlugin, self).__init__('patetico')

        self.config.add({
            'apostrophe': True,
            'zero_padding': True
        })

        if self.config['apostrophe']:
            self.register_listener('trackinfo_received', self.on_trackinfo_received)
            self.register_listener('albuminfo_received', self.on_albuminfo_received)

        if self.config['zero_padding']:
            self.register_listener('write', self.on_write)

    def _replace_apostrophe(self, item, tag):
        if not hasattr(item, tag):
            self._log.error("Item processed doesn't have tag {!r}", tag)
            return

        tag_value = getattr(item, tag)
        if isinstance(tag_value, str):
            setattr(item, tag, tag_value.replace('’', "'"))
        elif tag_value is not None:
            self._log.debug("Tried to process tag {!r} with value type {!r}", tag, type(tag_value))

    def on_albuminfo_received(self, info):
        info.decode()

        for tag in self.album_tags:
            self._replace_apostrophe(info, tag)

        if info.tracks:
            for track in info.tracks:
                for tag in self.track_tags:
                    self._replace_apostrophe(track, tag)

    def on_trackinfo_received(self, info):
        info.decode()
        for tag in self.track_tags:
            self._replace_apostrophe(info, tag)

    def on_write(self, item, path, tags):
        width = max(2, len(str(tags['tracktotal'])))
        tags['track'] = str(tags['track']).zfill(width)
