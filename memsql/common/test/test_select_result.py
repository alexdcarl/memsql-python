# -*- coding: utf-8 -*-
from memsql.common import database
import random
import pytest
import simplejson as json
from collections import OrderedDict

FIELDS = ['l\u203pez', 'ಠ_ಠ', 'cloud', 'moon', 'water', 'computer', 'school', 'network',
          'hammer', 'walking', 'mediocre', 'literature', 'chair', 'two', 'window', 'cords', 'musical',
          'zebra', 'xylophone', 'penguin', 'home', 'dog', 'final', 'ink', 'teacher', 'fun', 'website',
          'banana', 'uncle', 'softly', 'mega', 'ten', 'awesome', 'attatch', 'blue', 'internet', 'bottle',
          'tight', 'zone', 'tomato', 'prison', 'hydro', 'cleaning', 'telivision', 'send', 'frog', 'cup',
          'book', 'zooming', 'falling', 'evily', 'gamer', 'lid', 'juice', 'moniter', 'captain', 'bonding']

def test_result_order():
    raw_data = [[random.randint(1, 2**32) for _ in xrange(len(FIELDS))] for i in xrange(256)]
    res = database.SelectResult(FIELDS, raw_data)

    for i, row in enumerate(res):
        reference = dict(zip(FIELDS, raw_data[i]))
        ordered = OrderedDict(zip(FIELDS, raw_data[i]))
        doppel = database.Row(FIELDS, raw_data[i])

        assert doppel == row
        assert row == reference
        assert row == ordered
        assert row.keys() == FIELDS
        assert row.values() == raw_data[i]
        assert sorted(row) == sorted(FIELDS)
        assert row.items() == zip(FIELDS, raw_data[i])
        assert list(row.itervalues()) == raw_data[i]
        assert list(row.iterkeys()) == FIELDS
        assert list(row.iteritems()) == zip(FIELDS, raw_data[i])

        for f in FIELDS:
            assert f in row
            assert row.has_key(f)
            assert row[f] == reference[f]
            assert row['cloud'] == reference['cloud']
            assert row[f] == ordered[f]
            assert row['cloud'] == ordered['cloud']

        assert dict(row) == reference
        assert dict(row) == dict(ordered)

        with pytest.raises(KeyError):
            row['derp']

        with pytest.raises(AttributeError):
            row.derp

        with pytest.raises(NotImplementedError):
            row.pop()

        with pytest.raises(NotImplementedError):
            reversed(row)

        with pytest.raises(NotImplementedError):
            row.update({'a': 'b'})

        with pytest.raises(NotImplementedError):
            row.setdefault('foo', 'bar')

        with pytest.raises(NotImplementedError):
            row.fromkeys((1,))

        with pytest.raises(NotImplementedError):
            row.clear()

        with pytest.raises(NotImplementedError):
            del row['mega']

        reference['foo'] = 'bar'
        reference['cloud'] = 'blah'
        ordered['foo'] = 'bar'
        ordered['cloud'] = 'blah'
        row['foo'] = 'bar'
        row['cloud'] = 'blah'

        assert row == reference
        assert dict(row) == reference
        assert len(row) == len(reference)
        assert row == ordered
        assert dict(row) == dict(ordered)
        assert len(row) == len(ordered)

        assert json.dumps(row, sort_keys=True) == json.dumps(reference, sort_keys=True)
        assert json.dumps(row, sort_keys=True) == json.dumps(ordered, sort_keys=True)