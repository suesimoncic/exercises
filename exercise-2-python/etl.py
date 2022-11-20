
import pandas as pd
from datetime import datetime
from math import floor

RESULT_FILE_NAME = "results.csv"

class MergeFiles:
    def __init__(self, left_file, right_file):
        self.left_file = left_file
        self.right_file = right_file
        self.combined_df = None

    def load(self):
        try:
            self.df = pd.read_csv(self.left_file)
            self.df.set_index(["term_id","student_id"], inplace = True)

            # I began by keeping these methods generalized, but the overhead to keep it generalized is
            # of questionable value.
            right_df = pd.read_csv(self.right_file, parse_dates=[5], infer_datetime_format=True)
            right_df.set_index(["term_id", "student_id"], inplace=True)

            # Don't allocate a separate dataframe for the combined product, to save memory.
            self.df = self.df.join(right_df, how="inner")

        except Exception as e:
            print(f'Failed to load csv files into dataframe: {e.args}')
            return False

        return True

    def filter(self):
        try:
            self.df = self.df.loc[self.df['credits_earned'] > 90]
        except Exception as e:
            print(f'Failed to filter data: {e.args}')
            return False
        return True

    def add_age_column(self):
        try:
            # The following over-simplifies finding age. There are complications with leap years.
            # If I had the time, I would be inclined to partition date_of_birth and use a lambda function to derive age
            # in years from its parts
            # In the end, this approach didn't work anyway:
            now = datetime.now()
            self.df['age'] = floor((self.df['date_of_birth'] - now).days/365)
        except Exception as e:
            print(f'Failed to convert birth date to age: {e.args}')
            return False
        return True

    def add_age_column(self):
        try:
            # The following over-simplifies finding age. There are complications with leap years.
            # If I had the time, I would be inclined to partition date_of_birth and use a lambda function to derive age
            # in years from its parts
            now = datetime.now()
            def age_from_time_delta(date_of_birth):
                time_delta = now - date_of_birth
                return int(floor(time_delta.days/365))

            self.df['age'] = self.df.apply(lambda row: age_from_time_delta(row['date_of_birth']), axis=1)
        except Exception as e:
            print(f'Failed to convert birth date to age: {e.args}')
            return False
        return True

    def parse_class_id(self):
        try:
            def get_class_id_token(class_id, n):
                tokens = class_id.split('-')
                if len(tokens) > n:
                    return tokens[n]
                return None
            self.df['course_subject'] = self.df.apply(lambda row: get_class_id_token(row['class_id'], 0), axis=1)
            self.df['course_number'] = self.df.apply(lambda row: get_class_id_token(row['class_id'], 2), axis=1)
            self.df['course_section'] = self.df.apply(lambda row: get_class_id_token(row['class_id'], 3), axis=1)
        except Exception as e:
            print(f'Failed to parse class_id: {e.args}')
            return False
        return True

    def export(self):
        try:
            self.df.to_csv(RESULT_FILE_NAME, encoding='utf-8')
        except Exception as e:
            print(f'Failed to export to csv file {RESULT_FILE_NAME}: {e.args}')
            return False
        return True

    def print(self):
        with pd.option_context('display.max_columns', None, 'display.width', 1000):
            print(self.df.head())


def main():
    processor = MergeFiles("enrollments.csv", "students.csv")

    if not processor.load():
        exit(-1)
    if not processor.filter():
        exit(-2)
    if not processor.add_age_column():
        exit(-3)
    if not processor.parse_class_id():
        exit(-4)

    # Aggregation: I did not have time to complete this task. The string manipulation is easy enough, but I would have
    # needed to research how to group majors by student.

    if not processor.export():
        exit(-5)



if __name__ == '__main__':
    main()