# Follow Markdown links in Neovim

WIP.

Inspired by [vimwiki][vimwiki] and
[prashanthellina/follow-markdown-links][followlinks].

## Installing

Using [vim-plug][vim-plug], add this to your Neovim `init.vim`:

```
Plug 'alexpearce/nvim-follow-markdown-links', { 'do': ':UpdateRemotePlugins' }
```

No bindings are created. Useful behaviour is to follow links when hitting
Enter, and to go back to the previous file with Backspace:

```
command! FollowMarkdownLink call FollowMarkdownLink()
command! PreviousMarkdownBuffer call PreviousMarkdownBuffer()
autocmd FileType markdown nnoremap <script> <CR> :FollowMarkdownLink<CR>
autocmd FileType markdown nnoremap <script> <BS> :PreviousMarkdownBuffer<CR>
```

The plugin can search for matching files using a user-defined list of
extensions:

```
let g:follow_markdown_links#extensions = ['.md', '.markdown']
```

When the plugin is now activated over a link, e.g. `[Some link](the_file)`, it will
try first to open `the_file.md` and then `the_file.markdown`.

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
