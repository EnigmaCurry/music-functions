from ..lsystems import LSystem, PLSystem


def test_plsystem():
    assert list(PLSystem("N", depth=1, loop=False)) == [0]
    assert list(PLSystem("NN", depth=1, loop=False)) == [0] * 2
    assert list(PLSystem("NNNNNNNNNN", depth=1, loop=False)) == [0] * 10

    assert list(PLSystem("NN", depth=2, loop=False)) == [0] * 4
    assert list(PLSystem("NN", depth=3, loop=False)) == [0] * 8
    assert list(PLSystem("NN", depth=4, loop=False)) == [0] * 16

    assert list(PLSystem("NNN", depth=2, loop=False)) == [0] * 9
    assert list(PLSystem("NNN", depth=3, loop=False)) == [0] * 27

    assert list(PLSystem("N+++++N", depth=2, loop=False)) == [
        0,
        5,
        10,
        15,
    ]


def test_lsystem():
    l1 = LSystem("NN", seed="N")
    l1.iterate()
    assert l1.string == "NN"
    l1.iterate()
    assert l1.string == "NNNN"
    l1.iterate()
    assert l1.string == "NNNNNNNN"
    assert len(list(l1)) == 8

    l2 = LSystem("N++_N", seed="N")
    l2.iterate()
    l2.iterate()
    l2.iterate()
    assert l2.string == "N++N++N++N"
