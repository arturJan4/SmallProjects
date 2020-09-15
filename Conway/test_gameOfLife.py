from unittest import TestCase
from gameOfLife import *


class Test(TestCase):
    def test_next_board_state_empty(self):
        initial = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        expected = initial
        actual = next_board_state(initial)
        self.assertEqual(expected, actual)

    def test_next_board_state_test1(self):
        initial = [
            [0, 0, 1],
            [0, 1, 1],
            [0, 0, 0]
        ]
        expected = [
            [0, 1, 1],
            [0, 1, 1],
            [0, 0, 0]
        ]
        actual = next_board_state(initial)
        self.assertEqual(expected, actual)
        actual2 = next_board_state(actual)
        expected2 = expected
        self.assertEqual(expected2, actual2)

    def test_next_board_state_shoot(self):
        initial = [
            [0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0]
        ]
        state1 = [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 1, 0, 0]
        ]
        state2 = [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 1, 1, 0, 0]
        ]
        state3 = [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0]
        ]
        state4 = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0]
        ]
        state5 = dead_board(5,4)

        actual = next_board_state(initial)
        self.assertEqual(state1, actual)
        actual = next_board_state(actual)
        self.assertEqual(state2, actual)
        actual = next_board_state(actual)
        self.assertEqual(state3, actual)
        actual = next_board_state(actual)
        self.assertEqual(state4, actual)
        actual = next_board_state(actual)
        self.assertEqual(state5, actual)
