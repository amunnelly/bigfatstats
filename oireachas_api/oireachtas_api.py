

import pandas as pd
import numpy as np
import requests


class OireachtasExaminer(object):
    """oireachtas_api.py
    URL dates are in the form `%Y-%m-%d`
    Use empty string where you don't want to filter a house, say - it seems to work.
    members may be the only reliable one.
    """
    def __init__(self):
        self.parties = "https://api.oireachtas.ie/v1/parties?chamber_id{:}=&chamber={:}&house_no={:}&limit={:}"
        self.members = "https://api.oireachtas.ie/v1/members?date_start={:}&chamber_id={:}&date_end={:}&limit={:}"
        self.constituency = "https://api.oireachtas.ie/v1/constituencies?chamber_id=&chamber=dail&house_no=32&limit=50"
if __name__ == "__main__":
    x = OireachtasExaminer()