import pytest
from Parse import Parser

p = Parser("test.asm")

def test_comp():
    """
    Tests that comp method returns the correct string
    """
    p.current_command = "D=M"
    assert p.comp() == "M"

    p.current_command = "M=-1"
    assert p.comp() == "-1"

    p.current_command = "0;JMP"
    assert p.comp() == "0"

    p.current_command = "D;JLE"
    assert p.comp() == "D"


def test_dest():
    """
    Tests that the dest method returns the correct string
    """
    p.current_command = "D=D+A"
    assert p.dest() == "D"

    p.current_command = "MD=M-1"
    assert p.dest() == "MD"

    p.current_command = "D;JLE"
    assert p.dest() == ""


def test_jump():
    """
    Tests that the jump method returns the correct string
    """
    p.current_command = "D;JLE"
    assert p.jump() == "JLE"

    p.current_command = "M=M+1"
    assert p.jump() == ""

    p.current_command = "0;JMP"
    assert p.jump() == "JMP"

    p.current_command = "D;JGT"
    assert p.jump() == "JGT"
