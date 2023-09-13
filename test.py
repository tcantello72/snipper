import requests

BASE = "http://127.0.0.1:5000/"

data = [{"language" : "Python", "code": "this is a test"}]

response = requests.get(BASE)
print(response.json())
input()
response = requests.get(BASE + "snippet")
print(response.json())
input()
for i in range(len(data)):
    response = requests.post(BASE + "snippet/" + str(i), data[i])
    print(response.json())
