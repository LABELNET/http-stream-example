

import  requests


task = "122"

res = requests.get(f"http://127.0.0.1:5000/data?task={task}",stream=True)


results = []

for result in res.iter_content(chunk_size=1024):
    print("RESULT: ",result)
    results.append(result)

print(results)
