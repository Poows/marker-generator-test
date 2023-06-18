from typing import List
import names
import random


def generate_random_users_names(amount: int) -> List:
    uppercase_letters = "qwertyuiopasdfghjklzxcvbnmABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    names_set = set()

    while (len(names_set) < amount):
        #random_name = names.get_first_name()
        random_name = ''
        for i in range(7):
            random_letter = random.choice(uppercase_letters)
            random_name += random_letter
        names_set.add(random_name)

    return list(names_set)


def generate_random_ip_address(amount: int) -> List:
    random_ip_address_set = set()

    while (len(random_ip_address_set) < amount):
        random_ip = '.'.join(str(random.randint(0, 255)) for _ in range(4))
        random_ip_address_set.add(random_ip)

    return list(random_ip_address_set)


def generate_random_serial_disk_number(amount: int) -> List:
    uppercase_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    
    serial_disk_number_set = set()
    
    while (len(serial_disk_number_set) < amount):
        random_number = ''
        for i in range(15):
            random_letter = random.choice(uppercase_letters)
            random_number += random_letter
        serial_disk_number_set.add(random_number)

    return list(serial_disk_number_set)


def ip_addresses2bits(ip_addresses: List) -> List:
    #ip_addresses_bits = []

    # for ip in ip_addresses:
    ip_binary = ''.join([bin(int(x)+256)[3:] for x in ip_addresses.split('.')])
   # ip_addresses_bits.append(ip_binary)

    return ip_binary