# This is a sample Python script.
import psycopg2
from reset_table import empty_table
from datetime import datetime, timezone
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys

personfile="profile_C&S.csv"
conditionsfile="Conditions.csv"
personlist=[]
datadict=[]
conditionsdict={}


def persondata():
    with open(personfile,"r") as file:
        file.readline()
        for line in file:
            line = line.split(',')
            if line[0] not in personlist:
                personlist.append(line[0])
                datadict.append({line[0]:[int(line[0][5:]),int(line[2]),int(line[1])]})
                conditionsdict[line[0]]=[]
            conditionsdict[line[0]].append(line[10].strip('\n'))
    print('Adding perons to DB...')
    for person in datadict:
        for pers in person:
            person_query(person[pers][0],person[pers][1],person[pers][2])



def mapConditions():
    # print(conditionsdict)
    # print(datadict)
    mapdict={}
    with open(conditionsfile,'r') as file:
        file.readline()
        for line in file:
            line = line.split(',')
            mapdict[line[0]]=[line[9],line[10],line[0]]
    for dict in conditionsdict:
        for i, cond in enumerate(conditionsdict[dict]):
            conditionsdict[dict][i]=[mapdict[cond][0],mapdict[cond][2]]
    print('Adding conditions to DB')
    for person in datadict:
        for pers in person:
            for condition in conditionsdict[pers]:
                condition_query(person[pers][0],condition[0],condition[1])




def person_query(persid, yob, mob):
    conn = psycopg2.connect("dbname=postgres user=j3_g2 password=Blaat1234 host=145.74.104.145")    #connectie maken aan database
    cur = conn.cursor()

    person_id = persid           #not null contstraint
    gender_concept_id = 8507   #not-null constraint
    year_of_birth = yob       #Not null constraint
    month_of_birth = mob   #4
    day_of_birth = None    #5
    birth_datetime = None #'1999-01-08 04:05:06'
    race_concept_id = 4225446  #Not null constraint
    ethnicity_concept_id = 8527 #Not null constraint
    location_id = None      #9
    provider_id = None
    care_site_id = None
    person_source_value = None  #2
    gender_source_value = None #3
    gender_source_concept_id = None #4
    race_source_value = None #5
    race_source_concept_id = None #6
    ethnicity_source_value = None #7
    ethnicity_source_concept_id = None #8
    #1,2,3,4,5,'1999-01-08 04:05:06',7,8,9,NULL,NULL,2,3,4,5,6,7,8


    value_list_person = (person_id, gender_concept_id, year_of_birth, month_of_birth, day_of_birth, birth_datetime, race_concept_id, ethnicity_concept_id, location_id, provider_id, care_site_id, person_source_value, gender_source_value, gender_source_concept_id, race_source_value, race_source_concept_id, ethnicity_source_value, ethnicity_source_concept_id)
    # print(    """INSERT INTO j3_g2.person(person_id, gender_concept_id, year_of_birth, month_of_birth, day_of_birth, birth_datetime, race_concept_id, ethnicity_concept_id, location_id, provider_id, care_site_id, person_source_value, gender_source_value, gender_source_concept_id, race_source_value, race_source_concept_id, ethnicity_source_value, ethnicity_source_concept_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", value_list_person)
    cur.execute(
    """INSERT INTO j3_g2.person(person_id, gender_concept_id, year_of_birth, month_of_birth, day_of_birth, birth_datetime, race_concept_id, ethnicity_concept_id, location_id, provider_id, care_site_id, person_source_value, gender_source_value, gender_source_concept_id, race_source_value, race_source_concept_id, ethnicity_source_value, ethnicity_source_concept_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", value_list_person)

    conn.commit()

def condition_query(persid, conceptid, sourcename):
    conn = psycopg2.connect("dbname=postgres user=j3_g2 password=Blaat1234 host=145.74.104.145")    #connectie maken aan database
    cur = conn.cursor()

    ###moduleren van condition_occurrence zodat de querry's makkelijk kunnen worden aangepast
    condition_occurrence_id = conceptid    #number 12 #Not null constraint
    person_id = persid                    #number 1  verwijst naar tabel, Not null constraint
    condition_concept_id = conceptid   #number 32435 #Not null constraint
    condition_start_date = '2000-09-09'                 #date 2000-09-09 #Not null constraint
    condition_start_datetime = None     #'1999-01-08 04:05:06'    #datetime 1999-01-08 04:05:06
    condition_end_date = None #'2000-09-09'                   #date 2000-09-09
    condition_end_datetime = None #'1999-01-08 04:05:06'      #datetime 1999-01-08 04:05:06
    condition_type_concept_id = 0 #number 0
    stop_reason = 65               #number 65
    provider_id = None              #None   verwijst naar tabel
    visit_occurrence_id = None    #none     Verwijst naar tabel
    visit_detail_id = None #18            #number 18
    condition_source_value = None #12     #number 12
    condition_source_concept_id = None #43    #number 43
    condition_status_source_value = None #88  #number 88
    condition_status_concept_id = None #32    #number 32
    value_list_occurrence = (condition_occurrence_id, person_id, condition_concept_id, condition_start_date, condition_start_datetime, condition_end_date, condition_end_datetime, condition_type_concept_id, stop_reason, provider_id, visit_occurrence_id, visit_detail_id, condition_source_value, condition_source_concept_id, condition_status_source_value, condition_status_concept_id)



    # print("""INSERT INTO j3_g2.condition_occurrence(condition_occurrence_id, person_id, condition_concept_id, condition_start_date, condition_start_datetime, condition_end_date, condition_end_datetime, condition_type_concept_id, stop_reason, provider_id, visit_occurrence_id, visit_detail_id, condition_source_value, condition_source_concept_id, condition_status_source_value, condition_status_concept_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );""", value_list_occurrence)

    cur.execute(
        """INSERT INTO j3_g2.condition_occurrence(condition_occurrence_id, person_id, condition_concept_id, condition_start_date, condition_start_datetime, condition_end_date, condition_end_datetime, condition_type_concept_id, stop_reason, provider_id, visit_occurrence_id, visit_detail_id, condition_source_value, condition_source_concept_id, condition_status_source_value, condition_status_concept_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );""", value_list_occurrence)

    conn.commit()

    # cur.close()
    # empty_table()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    empty_table()
    persondata()
    mapConditions()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
