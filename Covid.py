import csv
import re
from collections import OrderedDict



def change_date_format(date):
    day, month, year = date.split('.')
    
    return month + "." + day + "." + year


def get_avg(column_name, curr):
    tot = 0
    values_count = 0
    tot = 0
    
    with open('covidTrain.csv', 'r') as file:
        reader = csv.reader(file) 

        header = next(reader)

        for row in reader:
            
            if(column_name == 'latitude'):
                
                value = row[6]
                
            if(column_name == 'longitude'):
                
                value = row[7]
                
            province = row[4]
            
            if(value != 'NaN' and province == curr):
                
                tot += float(value)
                
                values_count += 1
                    
        if (values_count > 0):
            
            return tot/values_count
        
        else:
            
            return 0
        
        
def getMostCommonCity(province):
    
    citdict = {}
    
    with open('covidTrain.csv', 'r') as file:
        
        reader = csv.reader(file) 

        header = next(reader)

        for row in reader:
            curr = row[4]
            city = row[3]
            
            if(city != 'NaN' and curr == province):
                
                if city in citdict.keys():
                    
                    citdict[city] += 1
                    
                else:
                    
                    citdict[city] = 1
        
    max_val= max(citdict.items(), key=lambda x: x[1])
    
    max_dict = {}
    
    for city, count in citdict.items():
        
        if(count == max_val[1]):
            
            max_dict[city] = count
    
    if (len(max_dict) > 1):
        
        max_dict = OrderedDict(sorted(max_dict.items(), key=lambda t: t[0]))
        
        max_val = max(max_dict.items(), key=lambda x: x[1])
        
    citycomm = max_val[0]
    
    return citycomm

def getMostCommonSymptom(province):
    
    symptom_dict = {}
    
    symptoms_list = []
    
    with open('covidTrain.csv', 'r') as file:
        
        reader = csv.reader(file) 

        header = next(reader)

        for row in reader:
            
            curr = row[4]
            
            symptoms = row[11]
            
            symptoms_list = []
            
            symptoms_list = symptoms.split(";")
            
            stripped_list = []
            
            for i in range(len(symptoms_list)):
                
                stripped_list.append(symptoms_list[i].strip())
            
            if(symptoms != 'NaN' and curr == province):
                
                for symptom in stripped_list:
                    
                    if symptom in symptom_dict.keys():
                        
                        symptom_dict[symptom] += 1
                        
                    else:
                        
                        symptom_dict[symptom] = 1
                        
    max_val= max(symptom_dict.items(), key=lambda x: x[1])
    
    max_dict = {}
    
    for symptom, count in symptom_dict.items():
        
        if(count == max_val[1]):
            
            max_dict[symptom] = count
    
    if (len(max_dict) > 1):
        
        max_dict = OrderedDict(sorted(max_dict.items(), key=lambda t: t[0]))
        
        max_val = max(max_dict.items(), key=lambda x: x[1])
        
    symptomcomm = max_val[0]
    
    return symptomcomm
    
def tasks_1_to_5():
    
    all_ages = []
    
    ages_count = 0
    
    average = 0 
    
    prev = ''
    
    with open('covidTrain.csv') as infile:
        
        reader = csv.DictReader(infile)
        
        with open('covidResult.csv','w',newline='') as csvfile:
            
            writer = csv.DictWriter(csvfile,fieldnames=reader.fieldnames)
            
            
            
            writer.writeheader()   
            
            for row in reader:
                
                if(prev == '' or prev != row['province']):
                    
                    prev = row['province']
                    
                    
                ''' Task 1 '''
                
                age = row['age']
                
                
                print(age)
                
                
                if(re.search('-',age) != None):
                    
                    
                    age1, age2 = age.split('-')
                    
                    age1 = int(age1)
                    
                    age2 = int(age2)

                    for i in range(age1, age2+1):
                        
                        all_ages.append(i)
                    

                    average = round(sum(all_ages)/len(all_ages))
                    
                    all_ages = []
                    
                    row['age'] = average
                    
                    
                ''' Task 2 '''
                
                row['date_onset_symptoms'] = change_date_format(row['date_onset_symptoms'])
                
                
                row['date_admission_hospital'] = change_date_format(row['date_admission_hospital'])
                
                
                row['date_confirmation'] = change_date_format(row['date_confirmation'])
                
                
                ''' Task 3 '''
                
                
                if(row['latitude'] == 'NaN'):
                    
                    
                    row['latitude'] = round(get_avg('latitude', row['province']), 2)
                    
                if(row['longitude'] == 'NaN'): 
                    
                    row['longitude'] = round(get_avg('longitude', row['province']), 2)
                    
                
                '''Task 4'''
                
                
                if(row['city'] == 'NaN'):
                    
                    
                    row['city'] = getMostCommonCity(row['province'])  
                    
                
                '''Task 5'''
                
                if(row['symptoms'] == 'NaN'):
                    
                    
                    row['symptoms'] = getMostCommonSymptom(row['province'])   

                writer.writerow(row)
    

            
def main():
    
    tasks_1_to_5()
  
if __name__ == "__main__":
    main()