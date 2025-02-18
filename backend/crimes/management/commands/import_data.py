import csv
import os
from django.core.management.base import BaseCommand
from crimes.models import CrimeData

class Command(BaseCommand):
    help = "Load crime data from CSV while changing years to 2014-2024"

    def handle(self, *args, **kwargs):
        file_path = "/Users/parthav./Documents/PROJECTS/CRIME RADAR AI BACKEND/backend/crimes/management/crime_dataset_india.csv"

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File {file_path} not found"))
            return
        
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = list(reader)  # Convert to list to iterate with index
        
        start_year = 2014
        end_year = 2024
        num_years = end_year - start_year + 1
        num_records_per_state = len(data) // num_years

        CrimeData.objects.all().delete()  # Clear old data

        for i, row in enumerate(data):
            state = row['STATE/UT']
            year = start_year + (i % num_years)  # Set year in cycle from 2014-2024

            crime_entry = CrimeData(
                state=state,
                year=year,
                murder=int(row['MURDER']),
                attempt_to_murder=int(row['ATTEMPT TO MURDER']),
                culpable_homicide=int(row['CULPABLE HOMICIDE NOT AMOUNTING TO MURDER']),
                rape=int(row['RAPE']),
                custodial_rape=int(row['CUSTODIAL RAPE']),
                other_rape=int(row['OTHER RAPE']),
                kidnapping_abduction=int(row['KIDNAPPING & ABDUCTION']),
                kidnapping_women_girls=int(row['KIDNAPPING AND ABDUCTION OF WOMEN AND GIRLS']),
                kidnapping_others=int(row['KIDNAPPING AND ABDUCTION OF OTHERS']),
                dacoity=int(row['DACOITY']),
                assembly_dacoity=int(row['PREPARATION AND ASSEMBLY FOR DACOITY']),
                robbery=int(row['ROBBERY']),
                burglary=int(row['BURGLARY']),
                theft=int(row['THEFT']),
                auto_theft=int(row['AUTO THEFT']),
                other_theft=int(row['OTHER THEFT']),
                riots=int(row['RIOTS']),
                criminal_breach_of_trust=int(row['CRIMINAL BREACH OF TRUST']),
                cheating=int(row['CHEATING']),
                counterfeiting=int(row['COUNTERFIETING']),
                arson=int(row['ARSON']),
                hurt_grievous_hurt=int(row['HURT/GREVIOUS HURT']),
                dowry_deaths=int(row['DOWRY DEATHS']),
                assault_women_modesty=int(row['ASSAULT ON WOMEN WITH INTENT TO OUTRAGE HER MODESTY']),
                insult_modesty_women=int(row['INSULT TO MODESTY OF WOMEN']),
                cruelty_by_husband=int(row['CRUELTY BY HUSBAND OR HIS RELATIVES']),
                importation_girls=int(row['IMPORTATION OF GIRLS FROM FOREIGN COUNTRIES']),
                causing_death_negligence=int(row['CAUSING DEATH BY NEGLIGENCE']),
                other_ipc_crimes=int(row['OTHER IPC CRIMES']),
                total_ipc_crimes=int(row['TOTAL IPC CRIMES'])
            )
            crime_entry.save()

        self.stdout.write(self.style.SUCCESS(f"Successfully loaded {len(data)} records with years 2014-2024"))
