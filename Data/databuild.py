import pandas as pd
import numpy as np
import os

os.chdir ('Data')

#2016 data

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
dic2016 = dict(zip(institutions2016.respondent, institutions2016.panel_name))
df2016['panel_name'] = df2016['respondent'].map(dic2016)

#2015 data

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
dic2015 = dict(zip(institutions2015.respondent, institutions2015.panel_name))
df2015['panel_name'] = df2015['respondent'].map(dic2015)

#2014 data

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
dic2014 = dict(zip(institutions2014.respondent, institutions2014.panel_name))
df2014['panel_name'] = df2014['respondent'].map(dic2014)

#combines and exports to a csv

frames = [df2014, df2015, df2016]
df = pd.concat(frames)
df.to_csv('hmda_data.csv')

# df = pd.read_csv('hmda_data.csv')
