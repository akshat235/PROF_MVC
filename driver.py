
import pandas as pd
import random
from rec_test import rec

if __name__ == "__main__":

    user_id = 1

    my_rec = rec(user_id)

    my_questions = my_rec.get_questions()

    print(my_questions)

