# 2 варианта FlatIterator - с преобразованием list_of_list в плоский список внутри FlatIterator 
# и без преобразования

# class FlatIterator:

#     def __init__(self, list_of_list):
#         self.flat_list = sum(list_of_list, start=[])
#         self.n = len(self.flat_list)

#     def __iter__(self):
#         self.cursor = -1
#         return self

#     def __next__(self):
#         self.cursor += 1
#         if self.cursor >= self.n:
#             raise StopIteration
#         return self.flat_list[self.cursor]

class FlatIterator:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list
        self.n = len(self.list_of_list)

    def __iter__(self):
        self.cursor_outer = 0
        self.cursor_inner = -1
        return self

    def __next__(self):
        self.cursor_inner += 1
        if self.cursor_inner >= len(self.list_of_list[self.cursor_outer]):
            self.cursor_outer += 1
            self.cursor_inner = 0
        if self.cursor_outer >= self.n:  
            raise StopIteration
        return self.list_of_list[self.cursor_outer][self.cursor_inner]


def test_1():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


if __name__ == '__main__':
    test_1()