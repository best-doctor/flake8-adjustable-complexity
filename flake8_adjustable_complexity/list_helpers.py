from typing import List


def flat(list_of_lists: List[List]) -> List:
    return [item for sublist in list_of_lists for item in sublist]
