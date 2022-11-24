# this test is for the ot module

import pytest
import ot

# test it with pytest
# $ python3 -m pytest tests/

def is_num_128_bit():
    a = ot.num
    assert a.bit_length() == 128
def test_length_num_to_bin():
    a = 1
    assert len(ot.num_to_bin(a)) == 128

def test_length_string_to_bin():
    a = 'abc'
    assert len(ot.string_to_bin(a)) == 128

def test_length_bin_to_string():
    a = '00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000011000010110001001100011' # 'abc'
    assert len(ot.bin_to_string(a)) == 3
def test_length_xor_int():
    a = 1
    b = 2
    assert len(ot.xor(a, b)) == 128

def test_length_xor_string():
    a = 'abc'
    b = 'def'
    assert len(ot.xor(a, b)) == 128

def test_length_xor_int_and_string():
    a = 1
    b = 'abc'
    assert len(ot.xor(a, b)) == 128

def test_length_xor_string_and_int():
    a = 'abc'
    b = 1
    assert len(ot.xor(a, b)) == 128

def this_test_will_fail():
    a = 1
    b = 2
    assert len(ot.xor(a, b)) == 127
