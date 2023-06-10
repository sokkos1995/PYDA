# Задание выполнил, но "обходным путем" - через выпрямление списка в ините
# понимаю, что нужно реализовать задание через рекурсию, но не получается выполнить
# В первой реализации развил логику из задания 1, но из-за return возвращается 
# только первый элемент вложенного списка
# Вторая реализация - облегченный, с упором на рекурсию, класс, но не получается выполнить 
# по той же причине
# подскажите, как обойти return в этих функциях? чтобы цикл не прекращался на этом первом 
# return


class FlatIterator:

    def __init__(self, list_of_list):
        self.list_of_list = self.zart_flatten(list_of_list)
        self.n = len(self.list_of_list)

    def zart_flatten(self, a):
        """
        Non recursive algorithm
        Based on pop from old and append elements to new list
        """
        queue, out = [a], []
        while queue:
            elem = queue.pop(-1)
            if isinstance(elem, list):
                queue.extend(elem)
            else:
                out.append(elem)
        return out[::-1]

    def __iter__(self):
        self.cursor = -1
        return self

    def __next__(self):
        self.cursor += 1
        if self.cursor >= self.n:  
            raise StopIteration        
        if isinstance(self.list_of_list[self.cursor], list):
            с = FlatIterator(self.list_of_list[self.cursor])
            for el in с:
                return el
        else:
            return self.list_of_list[self.cursor]


# class FlatIterator:

#     def __init__(self, list_of_list):
#         self.list_of_list = list_of_list
#         self.n = len(self.list_of_list)

#     def __iter__(self):
#         self.cursor_outer = 0
#         self.cursor_inner = -1
#         return self

#     def __next__(self):
#         self.cursor_inner += 1
#         if self.cursor_inner >= len(self.list_of_list[self.cursor_outer]) or self.list_of_list[self.cursor_outer][self.cursor_inner] == []:
#             self.cursor_outer += 1
#             self.cursor_inner = 0
#         if self.cursor_outer >= self.n:  
#             raise StopIteration
#         if isinstance(self.list_of_list[self.cursor_outer][self.cursor_inner], list) and self.list_of_list[self.cursor_outer][self.cursor_inner]:
#             for el in FlatIterator(self.list_of_list[self.cursor_outer][self.cursor_inner]):
#                 return el
#         else:
#             return self.list_of_list[self.cursor_outer][self.cursor_inner]

# class FlatIterator:

#     def __init__(self, list_of_list):
#         self.list_of_list = list_of_list
#         self.n = len(self.list_of_list)

#     def __iter__(self):
#         self.cursor = -1
#         return self

#     def __next__(self):
#         self.cursor += 1
#         if self.cursor >= self.n:  
#             raise StopIteration        
#         if isinstance(self.list_of_list[self.cursor], list):
#             с = FlatIterator(self.list_of_list[self.cursor])
#             for el in с:
#                 return el
#         else:
#             return self.list_of_list[self.cursor]
          
def test_3():

    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']


if __name__ == '__main__':
    test_3()
    # list_of_lists_2 = [
    #     [['a'], ['b', 'c']],
    #     ['d', 'e', [['f'], 'h'], False],
    #     [1, 2, None, [[[[['!']]]]], []]
    # ]
    # for el in FlatIterator(list_of_lists_2):
    #     print(el)