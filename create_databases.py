from typing import List
from init_data import init_database
from json import JSONEncoder
import json
import numpy as np


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


def create_databases(amounts: List) -> None:
    for amount in amounts:
        database = init_database(amount)
        json_database = {f"database_{amount}": database}
        with open(f"USERS_DATABASE_{amount}.json", "w") as write_file:
            json.dump(json_database, write_file, cls=NumpyArrayEncoder)