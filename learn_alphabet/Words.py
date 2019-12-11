from PyQt5.QtCore import Qt

WORD_A = [
            (1, 0), (2, 0),
    (0, 1),                 (3, 1),
    (0, 2),                 (3, 2),
    (0, 3),                 (3, 3),
    (0, 4), (1, 4), (2, 4), (3, 4),
    (0, 5),                 (3, 5),
    (0, 6),                 (3, 6),
]

WORD_B = [
    (0, 0), (1, 0), (2, 0),
    (0, 1),                 (3, 1),
    (0, 2),                 (3, 2),
    (0, 3), (1, 3), (2, 3),
    (0, 4),                 (3, 4),
    (0, 5),                 (3, 5),
    (0, 6), (1, 6), (2, 6),
]

WORD_C = [
    (0, 0), (1, 0), (2, 0), (3, 0),
    (0, 1),                 (3, 1),
    (0, 2),
    (0, 3),
    (0, 4),
    (0, 5),                 (3, 5),
    (0, 6), (1, 6), (2, 6), (3, 6),
]


class Words:
    words = {
        'A': WORD_A,
        'B': WORD_B,
        'C': WORD_C,
    }

    keys = {
        Qt.Key_A: 'A',
        Qt.Key_B: 'B',
        Qt.Key_C: 'C',
    }

    def get_by_key(self, key: Qt.Key):
        return self.keys[key] if key in self.keys.keys() else None

    def get_by_str(self, word: str):
        return self.words[word].copy() if word in self.words.keys() else None


