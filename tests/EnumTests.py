## In PyCharm, run this as: right-click + select 'Run py.test in EnumTests'
import sys
sys.path.append("..")
import pytest
from SearchDistribute.Enums import StrictEnum

class Animals(StrictEnum):
    Platypus = "Platypus"
    Armadillo = "Armadillo"

def test_enum_get_value():
    assert Animals.Armadillo == "Armadillo"

def test_enum_set_value():
    Animals.Horse = "Horse"
    assert Animals.Platypus == "Platypus"
    assert Animals.Horse == "Horse"

def test_enum_set_value_exception():
    with pytest.raises(AttributeError):
        Animals.Cat = "Csat"

def test_enum_insitantising_exception():
    with pytest.raises(TypeError):  ## http://doc.pytest.org/en/latest/assert.html#assertions-about-expected-exceptions
        x = Animals()

def test_enum_listing():
    Animals.Horse = "Horse"
    assert Animals.list() == ['Armadillo', 'Horse', 'Platypus']

def test_enum_deletion():
    Animals.Horse = "Horse"
    del(Animals.Horse)
    assert Animals.list() == ['Armadillo', 'Platypus']

def test_contains():
    assert ("Armadillo" in Animals) == True
    assert ("LinusTorvlads" in Animals) == False    ## debatable