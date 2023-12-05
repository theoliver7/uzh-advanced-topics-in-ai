import pandas as pd
from conf import HUMAN_PICKLE_PATH
obj = pd.read_pickle(HUMAN_PICKLE_PATH)
print(obj)