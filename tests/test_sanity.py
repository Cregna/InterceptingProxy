#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# InterceptingProxy test suite
# Copyright © 2017, Regna Cristian.
# See /LICENSE for licensing information.


import InterceptingProxy
import InterceptingProxy.template


def test_true():
    """Test if True is truthy."""
    assert True


def test_false():
    """Test if False is falsey."""
    assert not False


def test_trueexpr():
    """Test if this evaluates as True."""
    assert 1 == 1


def test_falseexpr():
    """Test if this evaluates as False."""
    assert 1 != 2


def test_math():
    """Test basic arithmetic skills of Python."""
    assert 2 + 2 == 4
    assert 2 - 2 == 0
    assert 2 * 2 == 4
    assert 2 / 2 == 1
    assert 3 % 2 == 1


def test_bitwise():
    """Test bitwise operators."""
    assert 0b11 ^ 0b10 == 0b01
    assert 0b100 | 0b010 == 0b110
    assert 0b101 & 0b011 == 0b001
    assert 0b10 << 2 == 0b1000
    assert 0b1111 >> 2 == 0b11


def test_import():
    """Test imports."""
    InterceptingProxy
    InterceptingProxy.template
