import sys
import hashlib


ENCODING = 'utf-8'


def hash_bit_string(hash_str, hash_obj):
    """Calculate hash value

    :param hash_str: hash input
    :type hash_str: string
    :return: hash value
    :rtype: zero filled hash bit string
    """
    #hash_obj = hashlib.sha1()
    encoded_hash_str = hash_str.encode(encoding=ENCODING)
    hash_obj.update(encoded_hash_str)

    digest = hash_obj.hexdigest()
    bit_digest_len = 8 * hash_obj.digest_size

    return format(int(digest, 16), 'b').zfill(bit_digest_len)


def main():
    test_str = "kdisafjheaw;gjaogwejh;gfeawhjgfw"

    hash_algorithms = {"md5": hashlib.md5(), "sha1": hashlib.sha1(), "sha256": hashlib.sha256(), "sha224": hashlib.sha224(), "sha384": hashlib.sha384()}

    for  key, value in hash_algorithms.items():
        h = hash_bit_string(test_str, value)
        print(f"{key}, {len(h)}")

    return


if __name__ == "__main__":
    sys.exit(main())