import pytest
import json

@pytest.fixture
def cli():
    from src.lib.brainxio import BrainXioCLI
    return BrainXioCLI()

def test_help(cli, capsys):
    rc = cli.run('help', [], False)
    assert rc == 0
    captured = capsys.readouterr()
    assert 'Usage: brainxio [options] <command> [args]' in captured.out
    assert '  help' in captured.out
    assert '  echo' in captured.out

def test_json_help(cli, capsys):
    rc = cli.run('help', [], True)
    assert rc == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data['name'] == 'BrainXio CLI'
    assert data['usage'] == 'brainxio [options] <command> [args]'
    assert any(opt['name'] == '--json' for opt in data['options'])
    assert any(cmd['name'] == 'help' for cmd in data['commands'])
    assert any(cmd['name'] == 'echo' and cmd['description'] == 'Echo the provided text' for cmd in data['commands'])
    assert '[info]' not in captured.out

def test_echo(cli, capsys):
    rc = cli.run('echo', ['Hello, BrainXio!'], False)
    assert rc == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == 'Hello, BrainXio!'

def test_echo_json(cli, capsys):
    rc = cli.run('echo', ['Hello, BrainXio!'], True)
    assert rc == 0
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data['success'] is True
    assert data['output'] == 'Hello, BrainXio!'

def test_echo_empty(cli, capsys):
    rc = cli.run('echo', [], False)
    assert rc != 0
    captured = capsys.readouterr()
    assert '[error] No text provided for echo' in captured.err
