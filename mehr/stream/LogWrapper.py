import sys
from io import TextIOWrapper, BytesIO
from tqdm import tqdm

class ProgbarWrapper(TextIOWrapper):
    def __init__(self, cnt=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pbar = tqdm(total=cnt)
    
    def write(self, string):
        for char in string:
            if char == "\n":
                self.pbar.update(1)

class LogProgress:
    def __init__(self, max_cnt=None):
        self.systems_stdout = None
        self.capture_stdout = None
        self.max_cnt = max_cnt
    
    def __enter__(self):
        self.systems_stdout = sys.stdout
        self.capture_stdout = ProgbarWrapper(self.max_cnt, BytesIO(), encoding=sys.stdout.encoding)
        sys.stdout = self.capture_stdout
        
    def __exit__(self, *args, **kwargs):
        sys.stdout = self.systems_stdout
        self.systems_stdout = None
        self.capture_stdout = None
