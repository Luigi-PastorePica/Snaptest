import re
import csv
from string import capwords
import os


# Generates an ordered alphabetic list that spans from "start" to "finish" (inclusive)
# Asterisk added after each character (website's form's specific requirement)
# If "start"'s and "finish"'s order is inverted, the function puts them in order
def char_list_generator(start, finish):

    try:
        start, finish = char_fix(start, finish)
    except TypeError as e:                 # Needs to raise a flag instead
        print e
    except ValueError as e:                # Needs to raise a flag instead
        print e
    except UnboundLocalError as e:
        print e                             # Needs to raise a flag instead
    else:
        ascii_code_list = range(ord(start), ord(finish) + 1)

        char_list = [chr(code) + '*' for code in ascii_code_list]

        return char_list

    return "Not a character"        # Any idea on what to return here?

# Determines whether the characters "first" and "last" are in valid alphabetic range
# Returns uppercase version "first" and "last" in alphabetic order
def char_fix(first, last):

    if len(first) == 1 and first.isalpha():
        first = first.upper()
        if len(last) == 1 and last.isalpha():
            last = last.upper()

            # Places initial and final characters in order if required
            if ord(first) > ord(last):
                first, last = last, first

        else:
            print "Error: '" + last + "' is not an alpha character"   ##### Will update later, when I have a better understanding of error handling
            return None                                             ##### Address this. Multiple return statements.
    else:
        print "Error: '" + first + "' is not an alpha character"  ##### Will update later, when I have a better understanding of error handling
        return None                                             ##### Address this

    return (first, last)

# Divides and individual's name and cleans it from whitespaces and undesired strings
def name_splitter(raw_name):
    full_name = re.split(',+', raw_name, 1)
    full_name[0] = capwords(full_name[0].lstrip())                # Last name
    full_name[1] = full_name[1].lstrip()                # First name and middle name
    name_and_middle = re.split(' +', full_name[1],1)    # Splits first name and middle name
    full_name[1] = capwords(name_and_middle[0])                   # First name
    middle_name = (name_and_middle[1].replace('(Click to show details)', '')).rstrip()  # Middle name. Removes undesired string.
    full_name.append(capwords(middle_name))                  # Extra step only for readability
    return full_name


def export_to_csv(file_name, people_list):

        # Places heading in file. I know I will have to change this to apply only when file is new.
        # I also have to consider selecting whether Major is printed on file or not.
        if people_list[0].person_affiliation.startswith(("Student", "student")):
            row_heading = ['Last Name', 'Name', 'Middle Name', 'e-mail', 'Affiliation', 'Organization', 'Major']
        else:
            row_heading = ['Last Name', 'Name', 'Middle Name', 'e-mail', 'Affiliation', 'Organization']

        info_for_csv = [person.join_info() for person in people_list]    # Prepares data for csv writer

        # If the file exists and is not empty, just add data
        if os.path.isfile(file_name) and os.stat(file_name).st_size > 0:    # If file exists and

            with open(file_name, "ab") as csv_output_file:
                writer = csv.writer(csv_output_file)
                writer.writerows(info_for_csv)      # Writes data on file
                csv_output_file.close()

        # Else, first write a heading and then the data
        else:

            with open(file_name, "ab") as csv_output_file:
                writer = csv.writer(csv_output_file)
                writer.writerow(row_heading)        # Writes heading
                writer.writerows(info_for_csv)      # Writes data on file
                csv_output_file.close()


# Not used anymore
class CharacterDomainError (Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
