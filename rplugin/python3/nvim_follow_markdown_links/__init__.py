"""
## TODO

* Support non-inline links.
* Support links over multiple lines
   * Probably need a MAX_LINES_TO_SEARCH to stop us looking at lots of lines
"""
import pathlib
import re
import urllib

import pynvim

# Match text and URL from an inline Markdown link
# https://stackoverflow.com/a/40178293
LINK_RE = re.compile(r'\[([^]]*)\]\(([^\s^\)]*)[\s\)]')


@pynvim.plugin
class FollowMarkdownLinksPlugin:
    def __init__(self, nvim):
        self.nvim = nvim
        self.config = {
            'open_remote': False,
            'debug': True
        }
        # List of (Path, cursor position) tuples
        self.buffer_stack = []

    @pynvim.function('FollowMarkdownLink', sync=True)
    def follow_markdown_link(self, _):
        # Cursor position
        crow, ccol = self.nvim.current.window.cursor
        # Current line buffer
        line = self. nvim.current.line
        # Index in string containing the start of the link
        # ccol + 1 so that we match when the cursor is *on* the opener
        start_pos = line.rfind('[', 0, ccol + 1)
        if start_pos == -1:
            self.debug('No link opener found before cursor: {}'.format(line[:ccol + 1]))
            return
        end_pos = line.find(')', start_pos)
        if end_pos < ccol:
            self.debug('No link closer found after cursor: {}'.format(line[start_pos:]))
            return

        # endpos + 2 so that we match when the cursor is *on* the closer
        haystack = line[start_pos:end_pos + 1]
        matches = LINK_RE.match(haystack)
        if matches is None:
            self.debug('No matches found: {}'.format(haystack))
            return
        _, href = matches.groups()

        # We only handle foillowing local paths
        url = urllib.parse.urlparse(href)
        if url.scheme:
            if self.config['open_remote']:
                # TODO
                pass
            self.debug('Path is not local: {}'.format(url))
            return

        # Get the path to the open buffer
        # https://unix.stackexchange.com/a/320129
        buffer_path = pathlib.Path(self.nvim.eval('expand("%:p")'))
        target_path = (buffer_path.parent / url.path).resolve()
        if not target_path.exists():
            # TODO: print an error/warning?
            self.debug('Path does not exist: {}'.format(target_path))
            return

        self.buffer_stack.append((buffer_path, (crow, ccol)))

        # TODO: escape quotation marks in path?
        self.debug('Opening path: {}'.format(target_path))
        self.nvim.command('w')
        self.nvim.command('edit {}'.format(target_path))

    @pynvim.function('PreviousMarkdownBuffer', sync=True)
    def previous_buffer(self, _):
        if not self.buffer_stack:
            self.debug('Empty history stack.')
            return

        target_path, cursor = self.buffer_stack.pop()

        self.debug('Opening path: {}'.format(target_path))
        self.nvim.command('w')
        self.nvim.command('edit {}'.format(target_path))

        # Restore the cursor position
        self.nvim.current.window.cursor = cursor

    def debug(self, msg):
        if self.config['debug']:
            # TODO show this as a list message when logging multiple times? log file?
            self.nvim.out_write(msg + '\n')
