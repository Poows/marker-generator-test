import numpy as np
import hashlib
import pandas as pd
import json
from generators import ip_addresses2bits
from marker import hash_bit_string
from tqdm import tqdm
import os
import re


MARKER_BIT_LEN = 32


def compute_prob(hash, length):
    return (length - len(np.unique(hash))) / length


def test_marker_generator(hash_algorithms, labels_type, ip_bin_lengths, databases_files):

    dataframe_columns = ["Размер набора данных", "Алгоритм хэширования", "Тип формирования метки", "Размер строки битов для ip адреса", "Вероятность коллизии"]
    df = pd.DataFrame(columns=dataframe_columns)

    for label_type in labels_type:
        for database_file in os.listdir(databases_files):
            database = json.load(open(os.path.join(databases_files, database_file)))
            database = database[f"database_{int(''.join(filter(str.isdigit, database_file)))}"]
            for hash_algorithm in hash_algorithms:
                for ip_bin_length in tqdm(ip_bin_lengths):
                    hash_list = []
                    if hash_algorithm == "sha1":
                        hash_obj = hashlib.sha1()
                    elif hash_algorithm == "sha256":
                        hash_obj = hashlib.sha256()
                    for (ip, name, disk) in database:
                        if label_type == "all":
                            union = ip_addresses2bits(ip) + name + disk
                            hash_bit = hash_bit_string(union, hash_obj)
                            hash_list.append(hash_bit[:MARKER_BIT_LEN])
                        else:
                            hash_ip_bit = hash_bit_string(ip_addresses2bits(ip), hash_obj)[:ip_bin_length]
                            hash_name_disk_bit = hash_bit_string(name + disk, hash_obj)[:MARKER_BIT_LEN-ip_bin_length]
                            hash_bit = hash_ip_bit + hash_name_disk_bit
                            hash_list.append(hash_bit)
                    #database = np.column_stack((database, hash_list))
                    prob = compute_prob(hash_list, len(database))
                    list_row = [len(database), hash_algorithm, label_type, ip_bin_length, prob]
                    df.loc[len(df)] = list_row
    print(df)

    df.to_csv('testing_result.csv', index=False)  

    # if label_type == "all":
    #     #array_of_union_str = np.array(ip_addresses_binary_list, dtype=str) + np.array(names_list, dtype=str) + np.array(serial_number_list, dtype=str)
    #     #array_of_union_str = [a + b + c for a, b, c in zip(ip_addresses_binary_list, names_list, serial_number_list)]
    #     hash_list = []
    #     for (ip, name, disk) in database:
    #         union = ip_addresses2bits(ip) + name + disk
    #         hash_bit = hash_bit_string(union, hash_obj)
    #         hash_list.append(hash_bit[:MARKER_BIT_LEN])
    # if label_type == "split":
    #     hash_list = []
    #     for (ip, name, disk) in database:
    #         hash_ip_bit = hash_bit_string(ip_addresses2bits(ip), hash_obj)[:ip_bit_len]
    #         hash_name_disk_bit = hash_bit_string(name + disk, hash_obj)[:MARKER_BIT_LEN-ip_bit_len]
    #         hash_bit = hash_ip_bit + hash_name_disk_bit
    #         hash_list.append(hash_bit)
    #     #array_of_union_str = np.array(ip_addresses_binary_list) + np.array(names_list) + np.array(serial_number_list)
    # database = np.column_stack((database, hash_list))

    # compute_prob(hash_list, len(database), data_file_path[:len(data_file_path) - 5], ip_bit_len, label_type)
