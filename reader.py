def read_data():
    f = open("data.csv", "r")
    fdata = f.readlines()
    f.close()
    return fdata


def transform_data(fdata):
    data_dict = dict()
    for (index, line) in enumerate(fdata):
        if index == 0:
            props = line.strip('\n').split(',')
            for (index, prop) in enumerate(props):
                data_dict[prop] = list()
        else:
            data_line = line.strip('\n').split(',')
            for (index, prop) in enumerate(props):
                data_dict[prop].append(data_line[index])

    return data_dict
