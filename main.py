from index import *
import reader

index_data_list = []

print("Welcome. Select what to do:")
while True:
    print("1 - make index from property")
    print("2 - search data in index")
    print("3 - end")
    choice = input()

    if int(choice) == 1:
        print("Please select a property to create index from")
        prop = input()
        data_dict = reader.transform_data(reader.read_data())
        prop_is_set = False

        while not prop_is_set:
            if prop in data_dict.keys():
                print("Please a name for your index")
                name = input()
                print("Creating an index", name, "from property", prop)
                str_list = sorted(data_dict[prop])
                sort_to_orig_map = [i[0] for i in sorted(enumerate(data_dict[prop]), key=lambda x: x[1])]
                index_data = IndexData(index_tree=create_index(str_list), index_name=name, orig_list=str_list,
                                       sort_to_orig_map=sort_to_orig_map)
                index_data_list.append(index_data)
                print("Index", index_data.index_name, "was created.")
                prop_is_set = True
            else:
                print("No such property found! try again")

    elif int(choice) == 2:
        print("Select index to search from")
        name = input()
        while True:
            if name not in [elem.index_name for elem in index_data_list]:
                print("Index not found. Try again")
                name = input()
            else:
                index_data = [elem for elem in index_data_list if elem.index_name == name][0]
                break

        print("Enter data to search for")
        data = input()
        found_at = index_search(data, index_data.index_tree)
        found_at_to_orig = index_data.sort_to_orig_map[found_at]
        for prop in data_dict.keys():
            print(data_dict[prop][found_at_to_orig])
    elif int(choice) == 3:
        print("bye")
        break