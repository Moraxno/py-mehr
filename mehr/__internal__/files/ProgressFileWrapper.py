import io
from types import TracebackType
from typing import Any, Optional
from tqdm import tqdm

from mehr.__internal__.stream import WhenceMode


class ProgressFileWrapper(io.IOBase):
    def __init__(self, file_descriptor: io.IOBase, *, expected_size=None, guess_size=True):
        self.file_descriptor = file_descriptor
        self.size = None

        if expected_size is not None:
            self.size = expected_size
        elif guess_size and self.file_descriptor.seekable():
            pos = file_descriptor.tell()
            file_descriptor.seek(0, WhenceMode.END)
            self.size = file_descriptor.tell()
            file_descriptor.seek(pos, WhenceMode.START)
        else:
            pass

        self.progress_bar = tqdm(total=self.size)

    def __enter__(self):
        self.file_descriptor.__enter__()
        return self

    def __exit__(self, exc_type: Optional[type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[TracebackType]) -> None:
        self.file_descriptor.__exit__(exc_type, exc_val, exc_tb)
        return self

    def close(self) -> None:
        self.file_descriptor.close()

    def read(self, hint=-1):
        data = self.file_descriptor.read(hint)
        self.progress_bar.update(len(data))
        return data

    def seek(self, offset: int, whence: int) -> int:
        pos = self.file_descriptor.seek(offset, whence)
        self.progress_bar.n = pos
        self.progress_bar.update()
        return pos
