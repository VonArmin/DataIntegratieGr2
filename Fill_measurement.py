import psycopg2
import random
from reset_table import empty_table


def print_hi():
    conn = psycopg2.connect("dbname=postgres user=j3_g2 password=Blaat1234 host=145.74.104.145")    #connectie maken aan database
    cur = conn.cursor()

    choices = (2, 12, 22)
    for i in range(1, 31):
        cur.execute("SELECT count(measurement_id) FROM measurement;")
        number_rows = cur.fetchone()
        number_rows = number_rows[0] + 1
        print(number_rows)
        measurement_id = number_rows  #notNullViolation
        person_id = random.choice(choices)          #notNullViolation
        measurement_concept_id = random.randint(45884779, 46369944)  #notNullViolation
        measurement_date = '2000-09-09'  #notNullViolation #date
        measurement_datetime = None
        measurement_time = None
        measurement_type_concept_id = 0       #notNullViolation
        operator_concept_id = None
        value_as_number = None
        value_as_concept_id = None
        unit_concept_id = None
        range_low   = None
        range_high  = None
        provider_id = None
        visit_occurrence_id = None
        visit_detail_id = None
        measurement_source_value    = None
        measurement_source_concept_id   = None
        unit_source_value = None
        value_source_value  = None

        value_list_measurement = (measurement_id, person_id, measurement_concept_id, measurement_date, measurement_datetime, measurement_time, measurement_type_concept_id, operator_concept_id, value_as_number, value_as_concept_id, unit_concept_id, range_low, range_high, provider_id, visit_occurrence_id, visit_detail_id, measurement_source_value, measurement_source_concept_id, unit_source_value, value_source_value)

        #cur.execute("""INSERT INTO measurement(measurement_id, person_id, measurement_concept_id, measurement_date, measurement_datetime, measurement_time, measurement_type_concept_id, operator_concept_id, value_as_number, value_as_concept_id, unit_concept_id, range_low, range_high, provider_id, visit_occurrence_id, visit_detail_id, measurement_source_value, measurement_source_concept_id, unit_source_value, value_source_value) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", value_list_measurement)

        conn.commit()



    cur.execute('SELECT * from measurement;')
    db_version = cur.fetchone()
    print("measurement")
    print(db_version)


    cur.close()




if __name__ == '__main__':
    print_hi()