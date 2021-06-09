# This is a sample Python script.
import psycopg2
from datetime import datetime, timezone
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi():
    conn = psycopg2.connect("dbname=postgres user=j3_g2 password=Blaat1234 host=145.74.104.145")    #connectie maken aan database
    cur = conn.cursor()

    date = '2000-09-09'     #moduleren zodat we later dingen in de querry konden zetten

    #vorbeeldquerrys voor het testen van inputten in de database
    cur.execute(
        """INSERT INTO location(location_id, address_1, address_2, city, state, zip, county, location_source_value) VALUES (9, 1,2,3,4,5,6,7)""")
    cur.execute(
        """INSERT INTO person(person_id, gender_concept_id, year_of_birth, month_of_birth, day_of_birth, birth_datetime, race_concept_id, ethnicity_concept_id, location_id, provider_id, care_site_id, person_source_value, gender_source_value, gender_source_concept_id, race_source_value, race_source_concept_id, ethnicity_source_value, ethnicity_source_concept_id) VALUES (1,2,3,4,5,'1999-01-08 04:05:06',7,8,9,NULL,NULL,2,3,4,5,6,7,8)""")
    cur.execute("""INSERT INTO condition_occurrence(condition_occurrence_id, person_id, condition_concept_id, condition_start_date, condition_start_datetime, condition_end_date, condition_end_datetime, condition_type_concept_id, stop_reason, provider_id, visit_occurrence_id, visit_detail_id, condition_source_value, condition_source_concept_id, condition_status_source_value, condition_status_concept_id) VALUES (12, 1, 32435, '{}', '1999-01-08 04:05:06', '2000-09-09', '1999-01-08 04:05:06', 0, 65 ,null,null,18 ,12,43,88, 32);""".format(date))


    cur.execute('SELECT * from condition_occurrence;')
    db_version = cur.fetchone()
    print(db_version)


    cur.close()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
