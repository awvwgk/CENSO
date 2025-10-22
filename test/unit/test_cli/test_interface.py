from pathlib import Path

from censo.cli.cml_parser import parse
from censo.cli.interface import startup, entry_point
from censo.params import Returncode


def test_blank_startup(capsys):
    ret = entry_point([])
    captured = capsys.readouterr()
    assert ret == Returncode.OK
    assert "No tasks enabled" in captured.out


def test_help_startup():
    argv = ["-h"]
    entry_point(argv)


def test_general_startup(example_ensemble_file):
    argv = str(
        f"-i {example_ensemble_file} --prescreening --solvent water -c 0 -u 0"
    ).split()
    ensemble, config = startup(parse(argv), {"check": ["prescreening"]})


def test_writeconfig():
    argv = "--new-config".split()
    entry_point(argv)

    assert Path("censo2rc_NEW").is_file()


def test_writereadconfig(example_ensemble_file):
    argv = "--new-config".split()
    entry_point(argv)

    argv = str(
        f"-i {example_ensemble_file} --prescreening --solvent water -c 0 -u 0 --inprc censo2rc_NEW"
    ).split()
    ensemble, config = startup(parse(argv), {"check": ["prescreening"]})


def test_rc_override(example_ensemble_file):
    argv = "--new-config".split()
    entry_point(argv)

    argv = str(
        f"--inprc censo2rc_NEW -i {example_ensemble_file} --prescreening --solvent water -c 1 -u 1 --gas-phase"
    ).split()
    args = parse(argv)
    ensemble, config = startup(args, {"check": ["prescreening"]})

    assert config.general.gas_phase is True
    assert config.general.solvent == "water"
    assert ensemble.conformers[0].charge == 1
    assert ensemble.conformers[0].unpaired == 1
