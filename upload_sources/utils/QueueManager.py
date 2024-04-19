import os
import time
import numpy
from dataclasses import dataclass

@dataclass
class QueueManager:
    """ QueueManager - is useful for managing the dataflow in a queue. """
    files: list

    def display_items(self) -> str:
        res = ", ".join([ file for file in self.files ])
        return res

    def count_items(self) -> str:
        res = len(self.files)
        return res
