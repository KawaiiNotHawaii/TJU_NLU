import json
data = []
nums = 0
for path in ('data/dev.json', 'data/test.json'):
    with open(path, encoding='utf-8') as f, open(path + '1.json', 'w', encoding='utf-8') as fw:
        for line in f.readlines():
            json_obj = json.loads(line)
            json_obj['novel_id'] = nums
            nums += 1
            fw.write(json.dumps(json_obj, ensure_ascii=False) + '\n')
        f.close()