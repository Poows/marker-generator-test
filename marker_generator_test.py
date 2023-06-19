import numpy as np
import hashlib
import pandas as pd
import json
from generators import ip_addresses2bits
from marker import hash_bit_string
from tqdm import tqdm
import os
import glob


MARKER_BIT_LEN = 32


def compute_prob(hash, length):
    return (length - len(np.unique(hash))) / length


def test_marker_generator(hash_algorithms, labels_type, ip_bin_lengths, databases_files):

    dataframe_columns = ["Размер набора данных", "Алгоритм хэширования", "Тип формирования метки", "Размер строки битов для ip адреса", "Вероятность коллизии"]
    hash_algorithms = {"md5": hashlib.md5(), "sha1": hashlib.sha1(), "sha256": hashlib.sha256(), "sha224": hashlib.sha224(), "sha384": hashlib.sha384()}
    df = pd.DataFrame(columns=dataframe_columns)

    list_of_files = filter( os.path.isfile,
                        glob.glob(databases_files + '/*') )
# Sort list of files in directory by size 
    list_of_files = sorted(list_of_files,
                            key =  lambda x: os.stat(x).st_size)

    for label_type in labels_type:
        for database_file in list_of_files:
            database = json.load(open(os.path.join(databases_files, database_file)))
            database = database[f"database_{int(''.join(filter(str.isdigit, database_file)))}"]
            for key, hash_obj in hash_algorithms.items():
                probs_list = []
                for ip_bin_length in tqdm(ip_bin_lengths):
                    hash_list = []
                    # if hash_algorithm == "sha1":
                    #     hash_obj = hashlib.sha1()
                    # elif hash_algorithm == "sha256":
                    #     hash_obj = hashlib.sha256()
                    for (ip, name, disk) in database:
                        if label_type == "all":
                            union = ip_addresses2bits(ip) + name + disk
                            hash_bit = hash_bit_string(union, hash_obj)
                            hash_list.append(hash_bit[:MARKER_BIT_LEN])
                        elif label_type == "split_ip_other":
                            hash_ip_bit = hash_bit_string(ip_addresses2bits(ip), hash_obj)[:ip_bin_length]
                            hash_name_disk_bit = hash_bit_string(name + disk, hash_obj)[:MARKER_BIT_LEN-ip_bin_length]
                            hash_bit = hash_ip_bit + hash_name_disk_bit
                            hash_list.append(hash_bit)
                        elif label_type == "split_ip_name_disk":
                            name_len = (MARKER_BIT_LEN-ip_bin_length) // 2
                            hash_ip_bit = hash_bit_string(ip_addresses2bits(ip), hash_obj)[:ip_bin_length]
                            hash_name = hash_bit_string(name, hash_obj)[:MARKER_BIT_LEN-ip_bin_length-name_len]
                            hash_disk = hash_bit_string(name, hash_obj)[:MARKER_BIT_LEN-ip_bin_length-len(hash_name)]
                            hash_bit = hash_ip_bit + hash_name + hash_disk
                            hash_list.append(hash_bit)
                        elif label_type == "ip_only":
                            ip_bit = ip_addresses2bits(ip)
                            hash_list.append(ip_bit)
                    prob = compute_prob(hash_list, len(database))
                    if (label_type == "all"):
                        ip_bin_length = -1
                        #list_row = [len(database), key, label_type, ip_bin_length, prob]
                        break
                    elif (label_type == "ip_only"):
                        ip_bin_length = 32
                        #list_row = [len(database), key, label_type, ip_bin_length, prob]
                        break
                    probs_list.append(prob)
                if label_type in ["split_ip_other", "split_ip_name_disk"]:
                    idx_min = np.argmin(probs_list)
                    ip_bin_length = ip_bin_lengths[idx_min]
                list_row = [len(database), key, label_type, ip_bin_length, prob]
                    #database = np.column_stack((database, hash_list))
                #list_row = [len(database), key, label_type, ip_bin_length, prob]
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
