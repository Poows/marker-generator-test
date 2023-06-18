import sys
import argparse
import json
import numpy as np
from json import JSONEncoder
from configs import EncodeConfig
from marker_generator_test import test_marker_generator


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True)
    args = parser.parse_args()
    config_path = args.config
    config = EncodeConfig.parse_file(config_path)
    label_type = config.label_type
    hash_type = config.hash_type
    ip_bit_len = config.ip_bit_len
    data_file_path = config.data_file_path

    test_marker_generator(hash_type, label_type, ip_bit_len, data_file_path)


if __name__ == "__main__":
    sys.exit(main())