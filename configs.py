from pydantic import BaseModel


class EncodeConfig(BaseModel):
    amount: int
    hash_type: list[str]
    load: bool
    label_type: list[str]
    ip_bit_len: list[int]
    data_file_path: str