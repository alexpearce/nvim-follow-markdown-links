"""
## TODO

* Test that modifications to the buffer are saved when jumping
forwards/backwards
* Add a test to check that our rplugin.vim is in sync with the plugin's API
"""
import pathlib


def create_files(tmp_path):
    fpath1 = tmp_path / 'file1.md'
    fpath2 = tmp_path / 'file2.md'

    text1 = 'Follow this [Markdown link](file2.md) now.'
    text2 = 'Follow another [Markdown link](file1.md) again.'
    fpath1.write_text(text1)
    fpath2.write_text(text2)

    return (fpath1, fpath2)


def test_follow(vim, tmp_path):
    fpath1, fpath2 = create_files(tmp_path)

    opener1 = fpath1.read_text().find('[')
    closer1 = fpath1.read_text().find(')')

    # Open the first file
    vim.command('edit {}'.format(fpath1))
    assert pathlib.Path(vim.eval('expand("%:p")')) == fpath1

    # Iterate through every position in the buffer, verifying that we only
    # follow the link when we're 'inside' the link
    for pos, character in enumerate(vim.current.line):
        inside_link = opener1 <= pos <= closer1

        # Place the cursor on the opening bracket
        vim.current.window.cursor = [1, pos]
        # Trigger the plugin
        vim.call('FollowMarkdownLink')

        # Check we've opened the linked file
        expected_path = fpath2 if inside_link else fpath1
        assert pathlib.Path(vim.eval('expand("%:p")')) == expected_path, (pos, character)

        # Go back to the first file
        vim.command('edit {}'.format(fpath1))


def test_history(vim, tmp_path):
    fpath1, fpath2 = create_files(tmp_path)

    opener1 = fpath1.read_text().find('[')
    opener2 = fpath2.read_text().find('[')

    # Open the first file
    vim.command('edit {}'.format(fpath1))
    # Place the cursor on the opening bracket of the first file
    vim.current.window.cursor = cursor1 = [1, opener1]
    # Trigger the plugin
    vim.call('FollowMarkdownLink')
    assert vim.current.window.cursor == [1, 0]

    # Place the cursor on the opening bracket of the second file
    vim.current.window.cursor = cursor2 = [1, opener2]
    # Trigger the plugin
    vim.call('FollowMarkdownLink')
    assert vim.current.window.cursor == [1, 0]

    # We should be back to the first file
    assert  pathlib.Path(vim.eval('expand("%:p")')) == fpath1

    # Revisit the previous file, which should be the second file
    vim.call('PreviousMarkdownBuffer')
    assert  pathlib.Path(vim.eval('expand("%:p")')) == fpath2
    assert vim.current.window.cursor == cursor2

    # Revisit the previous file again, which should be the first file
    vim.call('PreviousMarkdownBuffer')
    assert  pathlib.Path(vim.eval('expand("%:p")')) == fpath1
    assert vim.current.window.cursor == cursor1

    # History stack should now be empty, function should be a no-op
    vim.call('PreviousMarkdownBuffer')
    assert  pathlib.Path(vim.eval('expand("%:p")')) == fpath1
    assert vim.current.window.cursor == cursor1
