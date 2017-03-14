from byte.statements.where.parser import WHERE

from hamcrest import *


def test_and():
    assert_that(WHERE.parseString('id < 35 AND username == "alpha"').asList(), equal_to([
        ['id', '<', '35'],
        'and',
        ['username', '==', '"alpha"']
    ]))


def test_brackets():
    assert_that(WHERE.parseString('id < 35 AND (username == "alpha" OR username == "beta")').asList(), equal_to([
        ['id', '<', '35'],
        'and',
        [
            '(',
            ['username', '==', '"alpha"'],
            'or',
            ['username', '==', '"beta"'],
            ')'
        ]
    ]))


def test_or():
    assert_that(WHERE.parseString('id < 35 OR username == "alpha"').asList(), equal_to([
        ['id', '<', '35'],
        'or',
        ['username', '==', '"alpha"']
    ]))


def test_parameters():
    assert_that(WHERE.parseString('id < ? AND username == ?').asList(), equal_to([
        ['id', '<', '?'],
        'and',
        ['username', '==', '?']
    ]))


def test_simple():
    assert_that(WHERE.parseString('id < 35').asList(), equal_to([
        ['id', '<', '35']
    ]))
