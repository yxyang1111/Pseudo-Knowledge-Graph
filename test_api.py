import requests

# 调用 GET 端点并传递路径参数和查询参数



item_data = {
    "user_query": "罗国杰老师是谁？",
}

response = requests.post("http://127.0.0.1:8000/get_all_information/", json=item_data)
data = response.json()
print(data)