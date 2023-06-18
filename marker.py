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