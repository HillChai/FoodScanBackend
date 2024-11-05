如果修改了数据表字段，需要删除以前的旧表，重新创建


docker-compose中配置了postgres的数据库后，会当挂载的data目录为空时自动创建

# 生成token
curl.exe -X POST "http://localhost:8000/auth" -H "Content-Type: application/json" -d "{\"code\": \"12345\"}"

# 上传图片
curl.exe -X POST "http://localhost:8001/image" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcGVuaWQiOiJ0ZXN0MiIsInBlcm1pc3Npb24iOiJVU0VSIiwiZXhwIjoxNzI5NjEwMTQ4fQ.MEvbHae9XYTf-cqynNw1nq0rS34F0Gzwb9Ln8A5yaMfr5xhgF_SuCigLtR1pUPMxVZ28mba24zHMOyn0g4IWmpZo-wmF9J_IEtkwdDhynZUZtfQXvehqmqY7U18nse613UN36AmfDgSFP2y7uUZsDSAvftxa_0rVA0jEE2fQv_gbzlqLAkCU_vXMckukgdqgUdKg7FyfoIma3itXWDrmpE2fWvoOAVODfLi5dtSQuBISHgNFUzBwqgUy2m71CEJGLTFD3AjJgjIfEdF8oy3tiA9ZTQIjiY_YZdK9JgnR7jhVvHbyYyI9k3Ln44e5NOs-IvFdDSZmETBeeQS-ykOgcA" -F "file=@D:\FoodScanBackend\inveption_test\100332.jpg"

# 查询结果
curl.exe -G "http://localhost:8002/result?task_id=e9645f4a-a13f-472a-bf1f-df6741d32bcb" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcGVuaWQiOiJ0ZXN0MiIsInBlcm1pc3Npb24iOiJVU0VSIiwiZXhwIjoxNzI5NjEwMTQ4fQ.MEvbHae9XYTf-cqynNw1nq0rS34F0Gzwb9Ln8A5yaMfr5xhgF_SuCigLtR1pUPMxVZ28mba24zHMOyn0g4IWmpZo-wmF9J_IEtkwdDhynZUZtfQXvehqmqY7U18nse613UN36AmfDgSFP2y7uUZsDSAvftxa_0rVA0jEE2fQv_gbzlqLAkCU_vXMckukgdqgUdKg7FyfoIma3itXWDrmpE2fWvoOAVODfLi5dtSQuBISHgNFUzBwqgUy2m71CEJGLTFD3AjJgjIfEdF8oy3tiA9ZTQIjiY_YZdK9JgnR7jhVvHbyYyI9k3Ln44e5NOs-IvFdDSZmETBeeQS-ykOgcA"

# 查询历史
curl.exe -G "http://localhost:8002/currentuser" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcGVuaWQiOiJ0ZXN0MiIsInBlcm1pc3Npb24iOiJVU0VSIiwiZXhwIjoxNzI5NjEwMTQ4fQ.MEvbHae9XYTf-cqynNw1nq0rS34F0Gzwb9Ln8A5yaMfr5xhgF_SuCigLtR1pUPMxVZ28mba24zHMOyn0g4IWmpZo-wmF9J_IEtkwdDhynZUZtfQXvehqmqY7U18nse613UN36AmfDgSFP2y7uUZsDSAvftxa_0rVA0jEE2fQv_gbzlqLAkCU_vXMckukgdqgUdKg7FyfoIma3itXWDrmpE2fWvoOAVODfLi5dtSQuBISHgNFUzBwqgUy2m71CEJGLTFD3AjJgjIfEdF8oy3tiA9ZTQIjiY_YZdK9JgnR7jhVvHbyYyI9k3Ln44e5NOs-IvFdDSZmETBeeQS-ykOgcA"

nginx加之后：
location /auth/  -> 81/auth/
# 生成token
curl.exe -X POST "http://localhost:81/login/auth" -H "Content-Type: application/json" -d "{\"code\": \"12345\"}"

# 上传图片
curl.exe -X POST "http://localhost:81/upload/image" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcGVuaWQiOiJ0ZXN0MiIsInBlcm1pc3Npb24iOiJVU0VSIiwiZXhwIjoxNzI5NjE2Njc2fQ.OaXGdt_0r4cGp42smVo0ldXKKNPW1_K5JU058kfiO1yyTeo1sCfoLnx_wMBkCDfCJff8y7EnCbVZve5u6x62C-5-u309rE8d7rCJGtvknZ2FRtoDqUpuLnvbYyw4UhMMlOnVGzUJTaMIAnzZim4viUFNJuHMOesDzpY6TBd34TkxQBT6tBpVO4PcTfp15dxXwC_jBYC_tjsFZF7N9LFfJxcemYz4q0HBsa76slxMk4d4vzMkKV_LQ_YXxhEgQpbltF2su0zuDX5SQNRJjH-WNFvLPtGlh-QKbuWoD3SEAH-hDv0xnR7ph1irfNLEc6H8UDLPGy89ujMSKSm-puAxJA" -F "file=@D:\FoodScanBackend\inveption_test\100332.jpg"

# 查询结果
curl.exe -G "http://localhost:81/poll/result?task_id=2fb657ba-8c64-4245-b237-f183fd34922c" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcGVuaWQiOiJ0ZXN0MiIsInBlcm1pc3Npb24iOiJVU0VSIiwiZXhwIjoxNzI5NjE2Njc2fQ.OaXGdt_0r4cGp42smVo0ldXKKNPW1_K5JU058kfiO1yyTeo1sCfoLnx_wMBkCDfCJff8y7EnCbVZve5u6x62C-5-u309rE8d7rCJGtvknZ2FRtoDqUpuLnvbYyw4UhMMlOnVGzUJTaMIAnzZim4viUFNJuHMOesDzpY6TBd34TkxQBT6tBpVO4PcTfp15dxXwC_jBYC_tjsFZF7N9LFfJxcemYz4q0HBsa76slxMk4d4vzMkKV_LQ_YXxhEgQpbltF2su0zuDX5SQNRJjH-WNFvLPtGlh-QKbuWoD3SEAH-hDv0xnR7ph1irfNLEc6H8UDLPGy89ujMSKSm-puAxJA"

# 查询历史
curl.exe -G "http://localhost:81/poll/currentuser" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcGVuaWQiOiJ0ZXN0MiIsInBlcm1pc3Npb24iOiJVU0VSIiwiZXhwIjoxNzI5NjE2Njc2fQ.OaXGdt_0r4cGp42smVo0ldXKKNPW1_K5JU058kfiO1yyTeo1sCfoLnx_wMBkCDfCJff8y7EnCbVZve5u6x62C-5-u309rE8d7rCJGtvknZ2FRtoDqUpuLnvbYyw4UhMMlOnVGzUJTaMIAnzZim4viUFNJuHMOesDzpY6TBd34TkxQBT6tBpVO4PcTfp15dxXwC_jBYC_tjsFZF7N9LFfJxcemYz4q0HBsa76slxMk4d4vzMkKV_LQ_YXxhEgQpbltF2su0zuDX5SQNRJjH-WNFvLPtGlh-QKbuWoD3SEAH-hDv0xnR7ph1irfNLEc6H8UDLPGy89ujMSKSm-puAxJA"

部署测试
# 生成token
curl.exe -X POST "https://www.coderccc.xyz/login/auth" -H "Content-Type: application/json" -d "{\"code\": \"12345\"}"

# 上传图片
curl.exe -X POST "http://localhost:81/upload/image" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcGVuaWQiOiJ0ZXN0MiIsInBlcm1pc3Npb24iOiJVU0VSIiwiZXhwIjoxNzI5NjE2Njc2fQ.OaXGdt_0r4cGp42smVo0ldXKKNPW1_K5JU058kfiO1yyTeo1sCfoLnx_wMBkCDfCJff8y7EnCbVZve5u6x62C-5-u309rE8d7rCJGtvknZ2FRtoDqUpuLnvbYyw4UhMMlOnVGzUJTaMIAnzZim4viUFNJuHMOesDzpY6TBd34TkxQBT6tBpVO4PcTfp15dxXwC_jBYC_tjsFZF7N9LFfJxcemYz4q0HBsa76slxMk4d4vzMkKV_LQ_YXxhEgQpbltF2su0zuDX5SQNRJjH-WNFvLPtGlh-QKbuWoD3SEAH-hDv0xnR7ph1irfNLEc6H8UDLPGy89ujMSKSm-puAxJA" -F "file=@D:\FoodScanBackend\inveption_test\100332.jpg"

# 查询结果
curl.exe -G "http://localhost:81/poll/result?task_id=2fb657ba-8c64-4245-b237-f183fd34922c" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcGVuaWQiOiJ0ZXN0MiIsInBlcm1pc3Npb24iOiJVU0VSIiwiZXhwIjoxNzI5NjE2Njc2fQ.OaXGdt_0r4cGp42smVo0ldXKKNPW1_K5JU058kfiO1yyTeo1sCfoLnx_wMBkCDfCJff8y7EnCbVZve5u6x62C-5-u309rE8d7rCJGtvknZ2FRtoDqUpuLnvbYyw4UhMMlOnVGzUJTaMIAnzZim4viUFNJuHMOesDzpY6TBd34TkxQBT6tBpVO4PcTfp15dxXwC_jBYC_tjsFZF7N9LFfJxcemYz4q0HBsa76slxMk4d4vzMkKV_LQ_YXxhEgQpbltF2su0zuDX5SQNRJjH-WNFvLPtGlh-QKbuWoD3SEAH-hDv0xnR7ph1irfNLEc6H8UDLPGy89ujMSKSm-puAxJA"

# 查询历史
curl.exe -G "http://localhost:81/poll/currentuser" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcGVuaWQiOiJ0ZXN0MiIsInBlcm1pc3Npb24iOiJVU0VSIiwiZXhwIjoxNzI5NjE2Njc2fQ.OaXGdt_0r4cGp42smVo0ldXKKNPW1_K5JU058kfiO1yyTeo1sCfoLnx_wMBkCDfCJff8y7EnCbVZve5u6x62C-5-u309rE8d7rCJGtvknZ2FRtoDqUpuLnvbYyw4UhMMlOnVGzUJTaMIAnzZim4viUFNJuHMOesDzpY6TBd34TkxQBT6tBpVO4PcTfp15dxXwC_jBYC_tjsFZF7N9LFfJxcemYz4q0HBsa76slxMk4d4vzMkKV_LQ_YXxhEgQpbltF2su0zuDX5SQNRJjH-WNFvLPtGlh-QKbuWoD3SEAH-hDv0xnR7ph1irfNLEc6H8UDLPGy89ujMSKSm-puAxJA"