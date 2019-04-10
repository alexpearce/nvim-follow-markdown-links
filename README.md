# Follow Markdown links in Neovim

WIP.

Inspired by [vimwiki][vimwiki] and
[prashanthellina/follow-markdown-links][followlinks].

## Installing

Using [vim-plug][vim-plug], add this to your Neovim `init.vim`:

```
Plug 'alexpearce/nvim-follow-markdown-links', { 'do': ':UpdateRemotePlugins' }
```

## Developing

```
$ git clone https://github.com/alexpearce/nvim-follow-markdown-links.git
$ cd nvim-follow-markdown-links
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install -r requirements.txt -r requirements-test.txt
$ pytest
```

[vim-plug]: https://github.com/junegunn/vim-plug
[vimwiki]: https://github.com/vimwiki/vimwiki
[followlinks]: https://github.com/prashanthellina/follow-markdown-links
