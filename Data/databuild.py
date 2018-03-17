import pandas as pd
import numpy as np
import os

os.chdir ('Data')
df2016 = pd.read_csv('2016.CSV', low_memory=False)
df2016.columns = [
    'year',
    'respondent',
    'agency',
    'loan_type',
    'property_type',
    'loan_purpose',
    'occupancy',
    'loan_amount',
    'preapproval',
    'action_type',
    'msa_md',
    'state_code',
    'county_code',
    'census_tract_number',
    'applicant_ethnicity',
    'co_applicant_ethnicity',
    'applicant_race_1',
    'applicant_race_2',
    'applicant_race_3',
    'applicant_race_4',
    'applicant_race_5',
    'co_applicant_race_1',
    'co_applicant_race_2',
    'co_applicant_race_3',
    'co_applicant_race_4',
    'co_applicant_race_5',
    'applicant_sex',
    'co_applicant_sex',
    'applicant_income',
    'purchaser_type',
    'denial_reason_1',
    'denial_reason_2',
    'denial_reason_3',
    'rate_spread',
    'hoepa_status',
    'lien_status',
    'edit_status',
    'sequence_number',
    'population',
    'minority_population',
    'hud_median_family_income',
    'tract_to_msa',
    'number_of_owner_occupied_units',
    'number_of_family_units',
    'application_date_indicator']

institutions2016 = pd.read_csv('2016Institutions.csv', low_memory=False, encoding = 'latin1')
institutions2016.columns = ['drop', 'respondent', 'agency', 'panel_name', 'transmittal_name', 'lar_count']
dic2016 = institutions2016[['respondent', 'panel_name']].copy()
dic2016 = dict(zip(institutions2016.respondent, institutions2016.panel_name))

df2016['panel_name'] = df2016['respondent'].map(dic2016)


df2015 = pd.read_csv('2015.CSV', low_memory=False)
df2015.columns = [
    'year',
    'respondent',
    'agency',
    'loan_type',
    'property_type',
    'loan_purpose',
    'occupancy',
    'loan_amount',
    'preapproval',
    'action_type',
    'msa_md',
    'state_code',
    'county_code',
    'census_tract_number',
    'applicant_ethnicity',
    'co_applicant_ethnicity',
    'applicant_race_1',
    'applicant_race_2',
    'applicant_race_3',
    'applicant_race_4',
    'applicant_race_5',
    'co_applicant_race_1',
    'co_applicant_race_2',
    'co_applicant_race_3',
    'co_applicant_race_4',
    'co_applicant_race_5',
    'applicant_sex',
    'co_applicant_sex',
    'applicant_income',
    'purchaser_type',
    'denial_reason_1',
    'denial_reason_2',
    'denial_reason_3',
    'rate_spread',
    'hoepa_status',
    'lien_status',
    'edit_status',
    'sequence_number',
    'population',
    'minority_population',
    'hud_median_family_income',
    'tract_to_msa',
    'number_of_owner_occupied_units',
    'number_of_family_units',
    'application_date_indicator']

institutions2015 = pd.read_csv('2015Institutions.csv', low_memory=False, encoding = 'latin1')
institutions2015.columns = ['drop', 'respondent', 'agency', 'panel_name', 'transmittal_name', 'lar_count']
dic2015 = institutions2015[['respondent', 'panel_name']].copy()
dic2015 = dict(zip(institutions2015.respondent, institutions2015.panel_name))

df2015['panel_name'] = df2015['respondent'].map(dic2015)

df2014 = pd.read_csv('2014.CSV', low_memory=False)
df2014.columns = [
    'year',
    'respondent',
    'agency',
    'loan_type',
    'property_type',
    'loan_purpose',
    'occupancy',
    'loan_amount',
    'preapproval',
    'action_type',
    'msa_md',
    'state_code',
    'county_code',
    'census_tract_number',
    'applicant_ethnicity',
    'co_applicant_ethnicity',
    'applicant_race_1',
    'applicant_race_2',
    'applicant_race_3',
    'applicant_race_4',
    'applicant_race_5',
    'co_applicant_race_1',
    'co_applicant_race_2',
    'co_applicant_race_3',
    'co_applicant_race_4',
    'co_applicant_race_5',
    'applicant_sex',
    'co_applicant_sex',
    'applicant_income',
    'purchaser_type',
    'denial_reason_1',
    'denial_reason_2',
    'denial_reason_3',
    'rate_spread',
    'hoepa_status',
    'lien_status',
    'edit_status',
    'sequence_number',
    'population',
    'minority_population',
    'hud_median_family_income',
    'tract_to_msa',
    'number_of_owner_occupied_units',
    'number_of_family_units',
    'application_date_indicator']

institutions2014 = pd.read_csv('2014Institutions.csv', low_memory=False, encoding = 'latin1')
institutions2014.columns = ['drop', 'respondent', 'agency', 'panel_name', 'transmittal_name', 'lar_count']

dic2014 = institutions2014[['respondent', 'panel_name']].copy()
dic2014 = dict(zip(institutions2014.respondent, institutions2014.panel_name))

df2014['panel_name'] = df2014['respondent'].map(dic2014)

frames = [df2014, df2015, df2016]

df = pd.concat(frames)








#FROM cpfb github
# def hmda(metadata):
#     return Table('hmda', metadata,
#                  Column('year', Integer, nullable=False, index=True),
#                  Column('respondent', String(10)),
#                  Column('agency', Integer),
#                  Column('loan_type', Integer),
#                  Column('property_type', Integer),
#                  Column('loan_purpose', Integer),
#                  Column('occupancy', Integer, index=True),
#                  Column('loan_amount', Integer, index=True),
#                  Column('preapproval', Integer),
#                  Column('action_type', Integer),
#                  Column('msa_md', Integer, index=True),
#                  Column('state_code', Integer, index=True),
#                  Column('county_code', Integer),
#                  Index('state_code', 'county_code'),
#                  Column('census_tract_number', String(8), index=True),
#                  Column('applicant_ethnicity', Integer, index=True),
#                  Column('co_applicant_ethnicity', Integer),
#                  Column('applicant_race_1', Integer),
#                  Column('applicant_race_2', Integer),
#                  Column('applicant_race_3', Integer),
#                  Column('applicant_race_4', Integer),
#                  Column('applicant_race_5', Integer),
#                  Column('co_applicant_race_1', Integer),
#                  Column('co_applicant_race_2', Integer),
#                  Column('co_applicant_race_3', Integer),
#                  Column('co_applicant_race_4', Integer),
#                  Column('co_applicant_race_5', Integer),
#                  Column('applicant_sex', Integer),
#                  Column('co_applicant_sex', Integer),
#                  Column('applicant_income', Integer),
#                  Column('purchaser_type', Integer),
#                  Column('denial_reason_1', Integer),
#                  Column('denial_reason_2', Integer),
#                  Column('denial_reason_3', Integer),
#                  Column('rate_spread', String(10)),
#                  Column('hoepa_status', Integer),
#                  Column('lien_status', Integer),
#                  Column('edit_status', Integer),
#                  Column('sequence_number', Integer),
#                  Column('population', Integer),
#                  Column('minority_population', Float),
#                  Column('hud_median_family_income', Integer),
#                  Column('tract_to_msa', Float),
#                  Column('number_of_owner_occupied_units', Integer),
#                  Column('number_of_family_units', Integer),
#                  Column('application_date_indicator', Integer))
