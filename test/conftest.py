import json
import os
import sys

import pytest
import pynvim

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
NVIMRC = os.path.join(BASE_DIR, 'test/nvimrc',)
sys.path.insert(0, os.path.join(BASE_DIR, 'rplugin/python3'))


@pytest.fixture
def vim():
    # Provide our own manifest as an equivalent to running :UpdateRemotePlugins
    manifest = os.path.join(os.path.dirname(NVIMRC), 'rplugin.vim')
    assert os.path.exists(manifest)
    os.environ['NVIM_RPLUGIN_MANIFEST'] = manifest

    child_argv = os.environ.get('NVIM_CHILD_ARGV')
    listen_address = os.environ.get('NVIM_LISTEN_ADDRESS')
    if child_argv is None and listen_address is None:
        child_argv = '["nvim", "-u", "{}", "--embed", "--headless"]'.format(NVIMRC)

    if child_argv is not None:
        editor = pynvim.attach('child', argv=json.loads(child_argv))
    else:
        editor = pynvim.attach('socket', path=listen_address)

    return editor
