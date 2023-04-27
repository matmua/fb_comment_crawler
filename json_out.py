import json


json_data = []
name = 'healthy_v4_蔡天鳳碎屍案'
for line in open(name + '.json', 'r', encoding='utf-8'):
    json_data.append(json.loads(line))
    #print(json_data)

with open("../fb_bc/tec_5_url/" + name + ".txt", 'w') as file_object:
    member = [members.get('post_url') for members in json_data]
    l = len(member)
    for i in range(0, l):
        if member[i] != 'https://www.facebook.com/permalink.php':
            # print("\""+ member[i] + '\",')
            file_object.write("\"" + member[i] + '\",\n')

