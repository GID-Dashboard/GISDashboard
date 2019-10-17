import csv, re
from openpyxl import load_workbook
from django.contrib.auth.models import User, Group
from .models import Student, TutorGroup, House, SummativeDefinition, SummativeData, AptitudinalData, TeachingGroup, \
    YearGroup


def processstudent(path):
    with open(path, newline='') as csvfile:
        next(csvfile, None)
        students = csv.reader(csvfile, delimiter=',', quotechar='|')
        newstudents = []  # list of all the newly-created students

        # So that this may be a generic importer, we must set headers as the first line.

        for row in students:
            newstudent = {'student_id': row[0],
                          'first_name': row[1],
                          'last_name': row[2],
                          'preferred_forename': row[3],
                          'gender': row[4],
                          'tutor_group': row[5],
                          'sen_status': row[6],
                          'eal_status': row[7],
                          'exam_candidate_number': row[8],
                          'house': row[9],
                          'parent_salutation': row[10],
                          'student_email': row[11],
                          'parent_email': row[12]}

            newstudents.append(addstudent(newstudent))

        return newstudents


def addstudent(newstudent):
    # Test to see whether the user exists yet

    newuser, created = User.objects.get_or_create(username=newstudent['student_id'],
                                                  )

    # created will be true if the user didn't already exist.

    newuser.email = newstudent['student_email']
    newuser.first_name = newstudent['first_name']
    newuser.last_name = newstudent['last_name']
    newuser.save()

    # Place new user in the Students Auth group

    students_user_group, created = Group.objects.get_or_create(name='Students')
    students_user_group.user_set.add(newuser)

    new_tutor_group, created = TutorGroup.objects.get_or_create(group_name=newstudent['tutor_group'])
    if created:
        try:
            year_name = re.search('\d{1,2}', new_tutor_group.group_name).group(0)

        except AttributeError:
            year_name = new_tutor_group.group_name

        except IndexError:
            year_name = new_tutor_group.group_name

        year_group, created = YearGroup.objects.get_or_create(year=year_name)
        new_tutor_group.year_group = year_group
        new_tutor_group.save()
        if created:
            year_group.set_integer_year()

    new_house, created = House.objects.get_or_create(name=newstudent['house'])
    db_student, created = Student.objects.get_or_create(user=newuser)
    db_student.gender = newstudent['gender']
    db_student.student_id = newstudent['student_id']
    db_student.first_name = newstudent['first_name']
    db_student.last_name = newstudent['last_name']
    db_student.preferred_forename = newstudent['preferred_forename']
    db_student.tutor_group = new_tutor_group
    db_student.sen_status = newstudent['sen_status']
    db_student.eal_status = newstudent['eal_status']
    db_student.exam_candidate_number = newstudent['exam_candidate_number']
    db_student.house = new_house
    db_student.parent_email = newstudent['parent_email']
    db_student.parent_salutation = newstudent['parent_salutation']
    db_student.student_email = newstudent['student_email']
    db_student.save()

    return db_student


def process_fac_marksheet(path):
    with open(path, newline='') as fac_marksheet_file:
        next(fac_marksheet_file, None)
        records = csv.reader(fac_marksheet_file, delimiter=',')
        line_count = 0

        for row in records:
            if line_count == 0:  # Set up header names
                column_headings = []
                for column in row:
                    name = re.search(r'(^.+)KS\d', column).group(1)
                    column_headings.append(name)

            else:
                record = {}
                column_number = 0
                for column in row:
                    record_type = str(column_headings[column_number])
                    record[record_type] = column

                    addrecord(record)

            line_count = line_count + 1


def addrecord(record):
    """ Accepts a dictionary where keys are column names from a Factualy Marksheet,
     and values are the data in each row."""

    student = Student.objects.get(student_id=record['Admission No'])
    for key, value in record:
        if is_number(value):
            if key != 'Admission No':
                data_aspect, created = SummativeDefinition.objects.get_or_create(name=key)
                SummativeData.objects.get_or_create(data=data_aspect,
                                                    student=student,
                                                    value=value)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    except TypeError:
        return False


# Openpyxl:
def process_fac_marksheet(path):
    wb = load_workbook(path)

    # Iterate over the sheets
    for sheet in wb:
        rownumber = 0

        # Set a list of each column row
        column_headings = []
        # Iterate over rows
        for row in sheet.rows:

            # set names of columns:
            if rownumber == 0:
                # Iterate over each colmumn
                for column in row:
                    name = re.search(r'(^.+?)(?= KS\d|$)', column.value).group(1)
                    if name not in column_headings:
                        column_headings.append(name)
                    else:
                        final_digit = re.findall(r'(\d*)$', name)
                        if is_number(final_digit):
                            name = name + " " + final_digit
                        else:
                            name = name + " 1"

            else:
                record = {}
                column_number = 0
                for column in row:
                    record_type = str(column_headings[column_number])
                    record[record_type] = column.value
                    column_number = column_number + 1
                addrecord(record)

            rownumber = rownumber + 1


def addrecord(record):
    """ Adds a student's FAC record to the database, using a dictionary
    where keys = names of assessment areas and values are direct
    value to store in database. """
    created = False

    if record['Admission No.']:
        try:
            student, created = Student.objects.get_or_create(student_id=record['Admission No.'])
        except(KeyError):
            print('Tried to add a record with no Admission no on record' + str(record))
            return False

        if created:
            print('Created and deleted student with Admission no: ' + student.student_id)

        for data_point in record:

            # Skip blank records
            if not record[data_point]:
                continue

            # Add any classgroups
            if data_point == 'Class':
                teaching_group, created = TeachingGroup.objects.get_or_create(name=record['Class'])
                if created:
                    teaching_group.set_year_and_departmnet()

                student.teachinggroup_set.add(teaching_group)

            # The following should be done by the Students import, not marksheets.
            if data_point == 'Reg Group':
                pass

            if data_point == 'EAL':
                pass

            if data_point == 'Reg Group':
                pass

            if data_point == 'Surname Forename':
                pass

            # To enable us to record letter grades.
            else:
                data_aspect, created = SummativeDefinition.objects.get_or_create(name=data_point)
                student_db_data_records = SummativeData.objects.filter(data=data_aspect,
                                                                       student=student,
                                                                       ). \
                    order_by('-date')

                if student_db_data_records:  # record exists
                    student_record = student_db_data_records[0]
                    if student_record.letter_value != record[data_point]:
                        data = SummativeData.objects.create(student=student,
                                                     data=data_aspect,
                                                     raw_value=record[data_point])
                        data.value_from_raw()

                else:

                    data = SummativeData.objects.create(student=student,
                                                 data=data_aspect,
                                                 raw_value=record[data_point])
                    data.value_from_raw()



def add_CAT4_table():
    labels = ["CAT4 Verbal SAS",
              "CAT4 Non-Verbal SAS",
              "CAT4 Quantative SAS",
              "CAT4 Spatial SAS",
              "CAT4 Mean SAS",
              "CAT4 Maths Car",
              "CAT4 Maths Level", ]

    relevant_definitions = SummativeDefinition.objects.filter(name__in=labels)
    relevant_data = SummativeData.objects.filter(data__in=relevant_definitions)

    for point in relevant_data:
        student_a_data, created = AptitudinalData.objects.get_or_create(student=point.student,
                                                                        date=point.date)

        if point.name == 'CAT4 Verbal SAS':
            student_a_data.verbal = point.value
            student_a_data.save()
