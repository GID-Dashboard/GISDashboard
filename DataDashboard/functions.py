import csv, re
from openpyxl import load_workbook
from django.contrib.auth.models import User, Group
from .models import *


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
    db_student, created = LocalStudent.objects.get_or_create(user=newuser)
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

    student = LocalStudent.objects.get(student_id=record['Admission No'])
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
            student, created = LocalStudent.objects.get_or_create(student_id=record['Admission No.'])
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
                teaching_group, created = LocalTeachingGroup.objects.get_or_create(name=record['Class'])
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


def add_all_records(record):
    """ The previous function will try to do some clever thigns to add data to
    different tables. This one dumps everything in one single table,
    so we can sort it all out through Power BI queries. """

    if record['Admission No.']:
        try:
            student, created = LocalStudent.objects.get_or_create(student_id=record['Admission No.'])
        except(KeyError):
            print('Tried to add a record with no Admission no on record' + str(record))
            return False

        if created:
            print('Created and deleted student with Admission no: ' + student.student_id)

        for data_point in record:

            # Skip blank records
            if not record[data_point]:
                continue

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


def process_teacher(path):
    with open(path, newline='') as csvfile:
        next(csvfile, None)
        teachers = csv.reader(csvfile, delimiter=',', quotechar='|')
        newteachers = []  # list of all the newly-created students

        # So that this may be a generic importer, we must set headers as the first line.
        n = 0
        for row in teachers:
            if n == 0: # Skip headers
                n = n + 1
                continue

            newteacher = {'full_name': row[0],
                          'primary_email': row[1], #AUTHORATIVE
                          'staff_code': row[2], #AUTHORATIVE
                          'UPN': row[3], #AUTHORATIVE
                          }

            newteachers.append(update_teachers(newteacher))
            n = n + 1
        return newteachers


def assign_cat4_strategies():
    """
    First, import CAT4 profiles to the database. This funcrtion will assign interventions.
    """

    cat4_category = TeachingStrategyCategory.objects.get(name='CAT4 Suggested')
    strategies = TeachingStrategy.objects.filter(category=cat4_category)

    for strategy in strategies:
        strategy.students.clear()

    records = VerbalSpatialBias.objects.all()

    for record in records:
        intervention, int_created = TeachingStrategy.objects.get_or_create(title=record.bias)
        if int_created:
            print("Created an intervention called " + str(intervention.title))
            intervention.delete()
            continue
        student, stu_created = LocalStudent.objects.get_or_create(student_id=record.student_id)
        if stu_created:
            print("Created a student with ID " + str(student.student_id))
            student.delete()
            continue
        intervention.students.add(student)
        intervention.save()


def update_teachers(newteacher):
    teacher, created = Teacher.objects.get_or_create(staff_code=newteacher['staff_code'])
    teacher.email = newteacher['primary_email']
    teacher.UPN = newteacher['UPN']
    teacher.save()
    print("Added teacher: " + teacher.staff_code)


def sync_sims_and_internal_teachers():
    sims_teachers = SIMSTeacher.objects.all().filter(email_address__isnull=False)
    teacher_group, created = Group.objects.get_or_create(name='Teachers')

    for teacher in sims_teachers:
        print("Processing " + str(teacher.email_address))
        internal_teacher, created = Teacher.objects.get_or_create(email_address=teacher.email_address)

        internal_teacher.title_des = teacher.title_des
        internal_teacher.firstname = teacher.firstname
        internal_teacher.lastname = teacher.lastname
        internal_teacher.full_name = teacher.full_name
        internal_teacher.staff_code = teacher.staff_code
        internal_teacher.email_address = teacher.email_address
        internal_teacher.save()

        user, created = User.objects.get_or_create(email=internal_teacher.email_address)

        user.first_name = internal_teacher.firstname
        user.last_name = internal_teacher.lastname
        user.username = internal_teacher.email_address
        user.save()

        user.groups.add(teacher_group)
        internal_teacher.user = user
        internal_teacher.save()
        print("Created user: " + user.username)

        # Todo: Add logic for deleting students who have left


def sync_sims_and_internal_students():
    sims_students = Student.objects.all()

    for student in sims_students:
        print("Processing " + str(student.first_name ) + " " + str(student.last_name))
        internal_student, created = LocalStudent.objects.get_or_create(student_id=student.student_id)

        internal_student.last_name = student.last_name
        internal_student.first_name = student.first_name
        internal_student.house, created = House.objects.get_or_create(name=student.house_id)
        internal_student.preferred_forename = student.preferred_forename
        internal_student.gender = student.gender
        internal_student.sen_status = student.SEN_status
        internal_student.eal_status = student.EAL_status
        internal_student.exam_candidate_number = student.exam_candidate_number
        internal_student.parent_email = student.parent_email
        internal_student.tutor_group, created = TutorGroup.objects.get_or_create(group_name=student.tutor_group_id)
        internal_student.student_email = student.student_email

        internal_student.save()
