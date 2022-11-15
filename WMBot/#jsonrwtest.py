import json

thisdict =	{
  "brand": "Porsche",
  "model": "911",
  "year": 1919
}
print(thisdict)
numbers = [114514, "1919810", 141547124, "fghdhdh", 11]
filename = "numbers.json"

with open(filename,'r',encoding='utf-8') as f :
    loadjsontf = json.load(f)
print(loadjsontf)
print(loadjsontf['model'])
loadjsontf['model'] = str(int(loadjsontf['model']) + 1)
with open(filename, 'w', encoding='utf-8') as file_obj:
    json.dump(loadjsontf, file_obj)