import json
import os
import sys

import pytest
import pynvim

THIS_FILE_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(THIS_FILE_DIR)
RPYTHON_DIR = os.path.join(BASE_DIR, 'rplugin/python3')
PLUGIN_DIR = os.path.join(RPYTHON_DIR, 'nvim_follow_markdown_links')
NVIMRC = os.path.join(BASE_DIR, 'test/nvimrc',)
sys.path.insert(0, RPYTHON_DIR)


@pytest.fixture
def vim():
    # Provide our own manifest as an equivalent to running :UpdateRemotePlugins
    manifest_orig = os.path.join(THIS_FILE_DIR, 'rplugin.vim')
    assert os.path.exists(manifest_orig)
    manifest_mod = manifest_orig.replace('.vim', '_with_path.vim')

    # Need to open the manifest to modify the file path
    with open(manifest_orig) as f:
        s = f.read()
    with open(manifest_mod, 'w') as f:
        f.write(s.replace('INSERT_PATH_HERE', PLUGIN_DIR))
    os.environ['NVIM_RPLUGIN_MANIFEST'] = manifest_mod

    child_argv = os.environ.get('NVIM_CHILD_ARGV')
    listen_address = os.environ.get('NVIM_LISTEN_ADDRESS')
    if child_argv is None and listen_address is None:
        child_argv = '["nvim", "-u", "{}", "--embed", "--headless"]'.format(NVIMRC)

    if child_argv is not None:
        editor = pynvim.attach('child', argv=json.loads(child_argv))
    else:
        editor = pynvim.attach('socket', path=listen_address)

    return editor
