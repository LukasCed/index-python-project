class IndexTree:
    def __init__(self, branch_list=[], name='index-tree'):
        self.branchList = branch_list  # its a dict
        self.name = name

    def get_key_branch(self, key):
        return [branch for branch in self.branchList if key in branch][0][key]

    def branch_with_key_exist(self, key):
        return len([branch for branch in self.branchList if key in branch]) > 0

    def get_key_range_from_inclusive(self, key):
        return self.get_key_branch(key)[0][0]

    def get_key_range_to_exclusive(self, key):
        return self.get_key_branch(key)[0][1]

    def get_key_index(self, key):
        return self.get_key_branch(key)[1]

    def does_branch_with_key_exist(self, key):
        return self.get_key_branch(key)


class IndexData:
    def __init__(self, index_tree, index_name, orig_list, sort_to_orig_map):
        self.index_tree = index_tree
        self.index_name = index_name
        self.orig_list = orig_list
        self.sort_to_orig_map = sort_to_orig_map


def get_first_letter(word):
    return '' if word == '' else word[0]


def find_end_point(str_list):
    initial_letter = get_first_letter(str_list[0])
    last_letter_pos = 0
    for elem in str_list:
        if get_first_letter(elem) == initial_letter:
            last_letter_pos = last_letter_pos + 1
        else:
            break
    return last_letter_pos


def create_subList(str_list, end_point):
    new_list = [elem[1:] for elem in str_list[:end_point]]  # list spliting, comprehension. pasalinam pirmas raides
    if all(value is '' for value in new_list):
        new_list = ['']
    return new_list

def create_index(str_list):
    index = IndexTree([])
    if str_list[0] or len(str_list) > 1:
        str_list.sort()
        ref_point = 0

        while len(str_list) != 0:
            letter = get_first_letter(str_list[0])  # apie kuria raide kalbam
            end_point = find_end_point(str_list)  # kada baigiasi ta pati raide
            sub_list = create_subList(str_list, end_point)  # nukerpu pirmas raides
            interval = range(ref_point, ref_point + end_point)

            index_interval_tuple = (interval, create_index(
                sub_list))  # tuple. cia paduodu tos pacios raides sublista kuriam nukirptos pirmos raides
            # also rekursija
            index_info = {letter: index_interval_tuple}  # dict. raide ir kur ji pasiroda ir jos tolimesne info

            index.branchList.append(index_info)

            # pareducinam lista ka butu nuo endpoint ir vaziuojam toliau

            str_list = str_list[end_point:]
            ref_point = ref_point + end_point

        return index

def binary_search(intList, item):  # assume sorted
    start = 0
    end = len(intList) - 1

    while start <= end:
        mid_point = (end + start) // 2
        if intList[mid_point] == item:
            return mid_point
        elif intList[mid_point] < item:
            start = mid_point + 1
        else:
            end = mid_point - 1

    return -1

def index_search(item, index):  # esme atrasti kur elementas yra susortintame list'e
    where_in_sorted_list = 0
    index_to_search = index
    for char in item:
        if index_to_search is None or not index_to_search.branch_with_key_exist(char):
            return -1
        # search letter in index
        #         print(indexToSearch.branchList)
        where_in_sorted_list = where_in_sorted_list + index_to_search.get_key_range_from_inclusive(char)
        index_to_search = index_to_search.get_key_index(char)

    return where_in_sorted_list