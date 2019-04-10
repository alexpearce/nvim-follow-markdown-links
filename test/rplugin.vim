call remote#host#RegisterPlugin('python3', 'INSERT_PATH_HERE', [
      \ {'sync': v:true, 'name': 'FollowMarkdownLink', 'type': 'function', 'opts': {}},
      \ {'sync': v:true, 'name': 'PreviousMarkdownBuffer', 'type': 'function', 'opts': {}},
     \ ])
