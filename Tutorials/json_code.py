import json as json

#It is almost equal to a python dictionary, differences are:
#1) true,false are not capitalized, 
#2) null instead of none


#json.dump(): dump json data into file
#json.dumps(): dump python dict data into file

#json.load(): load json data from file 
#json.loads(): load data from string into json data

print("############################## Converting JSON to Python ##############################")
value="""
{ "name":"John", "age":30, "city":"New York", "lastname":null, "married":false}
  """

person_info_dict=json.loads(value)#s is for string
print("string value:",value)
print("person information as python dictionary:",person_info_dict)


print("##############################  Converting Python to JSON ##############################")
person_json_data=json.dumps(person_info_dict)
print(person_json_data )

############################## Storing JSON to file    ##############################

with open("data/person_info.json", 'w', encoding="utf-8") as file:
	json.dump(person_json_data,file,ensure_ascii=False )


print("############################## Loading a JSON file from file  ##############################")

file="data/person_info.json"
with  open(file, 'r',encoding="utf-8") as f:
	json_data=json.load(f)
print("person info loaded from json file:",json_data)



# list of dictionaries into dict
#https://stackoverflow.com/questions/5236296/how-to-convert-list-of-dict-to-dict
