from generators import generate_random_users_names
from generators import generate_random_serial_disk_number
from generators import generate_random_ip_address
import numpy as np


def init_database(amount: int):
    # if load:
    #     data = json.load(open(data_file_path))[f"database_{hash_obj_type}"]
    #     ip_addresses_list = []
    #     names_list = []
    #     serial_number_list = []
    #     for (ip, name, disk_name, _) in data:
    #         ip_addresses_list.append(ip)
    #         names_list.append(name)
    #         serial_number_list.append(disk_name)
    # else:
    names_list = generate_random_users_names(amount)
    ip_addresses_list = generate_random_ip_address(amount)
    serial_number_list = generate_random_serial_disk_number(amount)
    #ip_addresses_binary_list = ip_addresses2bits(ip_addresses_list)
    
    database = np.column_stack((ip_addresses_list, names_list, serial_number_list))
    return database 