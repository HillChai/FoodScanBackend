如果修改了数据表字段，需要删除以前的旧表，重新创建


docker-compose中配置了postgres的数据库后，会当挂载的data目录为空时自动创建

# 生成token
curl.exe -X POST "http://localhost:8000/auth" -H "Content-Type: application/json" -d "{\"code\": \"12345\"}"

# 修改头像
curl.exe -X POST "http://localhost:8001/head" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcGVuaWQiOiJ0ZXN0MiIsInBlcm1pc3Npb24iOiJVU0VSIiwiZXhwIjoxNzMwMDU1MjYwfQ.FZAZ2KqXjf5Q1vjhHvJoL5jzTAXtUk1WbUO2lDhz5-n4dHvRJ0nBqOXRFiu7UivZHK7DyWzrZvZjVTj3cva7nkvVM0o6TrPs8hcPor_vDo3mqLTPWNGwBF7tJP0oz5J3_S44WA5rQhXDOQwIDrRboyV1dN7ttxBn_gz2oVyzdWR7AWJzmUeje8fOcd73kYKIhN8fnsW6tomGnPvvCcMatThzqQNAywqS0zVCtQxq_KJkPWJeZj3z9zCz_tJ6yYzwm96q2oCuFzUp_Tywpf5Y09aDA-k0h4TVLrXrML7FjgoNxWfhFUE14aKPK0n0APAH9Vdhjs0Q4_FMbW3VUTOUWw" -F "file=@D:\FoodScanBackend\inveption_test\100332.jpg"
# 修改用户信息（名称、手机号、电邮、签名）
curl.exe -X PUT "http://localhost:8001/userinfo" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcGVuaWQiOiJ0ZXN0MiIsInBlcm1pc3Npb24iOiJVU0VSIiwiZXhwIjoxNzMwMDU1MjYwfQ.FZAZ2KqXjf5Q1vjhHvJoL5jzTAXtUk1WbUO2lDhz5-n4dHvRJ0nBqOXRFiu7UivZHK7DyWzrZvZjVTj3cva7nkvVM0o6TrPs8hcPor_vDo3mqLTPWNGwBF7tJP0oz5J3_S44WA5rQhXDOQwIDrRboyV1dN7ttxBn_gz2oVyzdWR7AWJzmUeje8fOcd73kYKIhN8fnsW6tomGnPvvCcMatThzqQNAywqS0zVCtQxq_KJkPWJeZj3z9zCz_tJ6yYzwm96q2oCuFzUp_Tywpf5Y09aDA-k0h4TVLrXrML7FjgoNxWfhFUE14aKPK0n0APAH9Vdhjs0Q4_FMbW3VUTOUWw" -d "{\"name\": \"new_costumer4\",\"phone_number\": \"12335667899\",\"email\": \"customer4@qq.com\",\"signature\": \"我思故我在\",\"gold_coin\": \"1000\",\"experience\": \"10000\"}" -H "Content-Type: application/json"
# 修改用户信息（金币）
curl.exe -X PUT "http://localhost:8001/gold_coin" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcGVuaWQiOiJ0ZXN0MiIsInBlcm1pc3Npb24iOiJVU0VSIiwiZXhwIjoxNzMwMDU1MjYwfQ.FZAZ2KqXjf5Q1vjhHvJoL5jzTAXtUk1WbUO2lDhz5-n4dHvRJ0nBqOXRFiu7UivZHK7DyWzrZvZjVTj3cva7nkvVM0o6TrPs8hcPor_vDo3mqLTPWNGwBF7tJP0oz5J3_S44WA5rQhXDOQwIDrRboyV1dN7ttxBn_gz2oVyzdWR7AWJzmUeje8fOcd73kYKIhN8fnsW6tomGnPvvCcMatThzqQNAywqS0zVCtQxq_KJkPWJeZj3z9zCz_tJ6yYzwm96q2oCuFzUp_Tywpf5Y09aDA-k0h4TVLrXrML7FjgoNxWfhFUE14aKPK0n0APAH9Vdhjs0Q4_FMbW3VUTOUWw" -d "{\"name\": \"new_costumer3\",\"phone_number\": \"12345667899\",\"email\": \"customer@qq.com\",\"signature\": \"我思故我在\",\"gold_coin\": \"1001\",\"experience\": \"10000\"}" -H "Content-Type: application/json"
# 修改用户信息（经验）
curl.exe -X PUT "http://localhost:8001/experience" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcGVuaWQiOiJ0ZXN0MiIsInBlcm1pc3Npb24iOiJVU0VSIiwiZXhwIjoxNzMwMDU1MjYwfQ.FZAZ2KqXjf5Q1vjhHvJoL5jzTAXtUk1WbUO2lDhz5-n4dHvRJ0nBqOXRFiu7UivZHK7DyWzrZvZjVTj3cva7nkvVM0o6TrPs8hcPor_vDo3mqLTPWNGwBF7tJP0oz5J3_S44WA5rQhXDOQwIDrRboyV1dN7ttxBn_gz2oVyzdWR7AWJzmUeje8fOcd73kYKIhN8fnsW6tomGnPvvCcMatThzqQNAywqS0zVCtQxq_KJkPWJeZj3z9zCz_tJ6yYzwm96q2oCuFzUp_Tywpf5Y09aDA-k0h4TVLrXrML7FjgoNxWfhFUE14aKPK0n0APAH9Vdhjs0Q4_FMbW3VUTOUWw" -d "{\"name\": \"new_costumer3\",\"phone_number\": \"12345667899\",\"email\": \"customer@qq.com\",\"signature\": \"我思故我在\",\"gold_coin\": \"1000\",\"experience\": \"10001\"}" -H "Content-Type: application/json"


# 上传图片
curl.exe -X POST "http://localhost:8001/image" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcGVuaWQiOiJ0ZXN0MiIsInBlcm1pc3Npb24iOiJVU0VSIiwiZXhwIjoxNzMwMDU1MjYwfQ.FZAZ2KqXjf5Q1vjhHvJoL5jzTAXtUk1WbUO2lDhz5-n4dHvRJ0nBqOXRFiu7UivZHK7DyWzrZvZjVTj3cva7nkvVM0o6TrPs8hcPor_vDo3mqLTPWNGwBF7tJP0oz5J3_S44WA5rQhXDOQwIDrRboyV1dN7ttxBn_gz2oVyzdWR7AWJzmUeje8fOcd73kYKIhN8fnsW6tomGnPvvCcMatThzqQNAywqS0zVCtQxq_KJkPWJeZj3z9zCz_tJ6yYzwm96q2oCuFzUp_Tywpf5Y09aDA-k0h4TVLrXrML7FjgoNxWfhFUE14aKPK0n0APAH9Vdhjs0Q4_FMbW3VUTOUWw" -F "file=@D:\FoodScanBackend\inveption_test\100332.jpg"

# 查询结果
curl.exe -G "http://localhost:8002/result?task_id=af79b50c-4895-4e79-a4fd-eda398788c2d" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcGVuaWQiOiJ0ZXN0MiIsInBlcm1pc3Npb24iOiJVU0VSIiwiZXhwIjoxNzMwMDU1MjYwfQ.FZAZ2KqXjf5Q1vjhHvJoL5jzTAXtUk1WbUO2lDhz5-n4dHvRJ0nBqOXRFiu7UivZHK7DyWzrZvZjVTj3cva7nkvVM0o6TrPs8hcPor_vDo3mqLTPWNGwBF7tJP0oz5J3_S44WA5rQhXDOQwIDrRboyV1dN7ttxBn_gz2oVyzdWR7AWJzmUeje8fOcd73kYKIhN8fnsW6tomGnPvvCcMatThzqQNAywqS0zVCtQxq_KJkPWJeZj3z9zCz_tJ6yYzwm96q2oCuFzUp_Tywpf5Y09aDA-k0h4TVLrXrML7FjgoNxWfhFUE14aKPK0n0APAH9Vdhjs0Q4_FMbW3VUTOUWw"

# 查询历史
curl.exe -G "http://localhost:8002/currentuser" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcGVuaWQiOiJ0ZXN0MiIsInBlcm1pc3Npb24iOiJVU0VSIiwiZXhwIjoxNzMwMDU1MjYwfQ.FZAZ2KqXjf5Q1vjhHvJoL5jzTAXtUk1WbUO2lDhz5-n4dHvRJ0nBqOXRFiu7UivZHK7DyWzrZvZjVTj3cva7nkvVM0o6TrPs8hcPor_vDo3mqLTPWNGwBF7tJP0oz5J3_S44WA5rQhXDOQwIDrRboyV1dN7ttxBn_gz2oVyzdWR7AWJzmUeje8fOcd73kYKIhN8fnsW6tomGnPvvCcMatThzqQNAywqS0zVCtQxq_KJkPWJeZj3z9zCz_tJ6yYzwm96q2oCuFzUp_Tywpf5Y09aDA-k0h4TVLrXrML7FjgoNxWfhFUE14aKPK0n0APAH9Vdhjs0Q4_FMbW3VUTOUWw"

# 修改结果
curl.exe -X PUT "http://localhost:8003/cache_result/707452d9-e3b2-4f86-b5c6-219013c59dae" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcGVuaWQiOiJ0ZXN0MiIsInBlcm1pc3Npb24iOiJVU0VSIiwiZXhwIjoxNzMwMDU1MjYwfQ.FZAZ2KqXjf5Q1vjhHvJoL5jzTAXtUk1WbUO2lDhz5-n4dHvRJ0nBqOXRFiu7UivZHK7DyWzrZvZjVTj3cva7nkvVM0o6TrPs8hcPor_vDo3mqLTPWNGwBF7tJP0oz5J3_S44WA5rQhXDOQwIDrRboyV1dN7ttxBn_gz2oVyzdWR7AWJzmUeje8fOcd73kYKIhN8fnsW6tomGnPvvCcMatThzqQNAywqS0zVCtQxq_KJkPWJeZj3z9zCz_tJ6yYzwm96q2oCuFzUp_Tywpf5Y09aDA-k0h4TVLrXrML7FjgoNxWfhFUE14aKPK0n0APAH9Vdhjs0Q4_FMbW3VUTOUWw" -d "{\"inference_result\": \"猕猴桃\",\"weight_result\": 300}" -H "Content-Type: application/json"



# nginx加之后：
# location /auth/  -> 81/auth/
# 生成token
curl.exe -X POST "http://localhost:81/login/auth" -H "Content-Type: application/json" -d "{\"code\": \"12345\"}"

# 上传图片
curl.exe -X POST "http://localhost:81/upload/image" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcGVuaWQiOiJ0ZXN0MiIsInBlcm1pc3Npb24iOiJVU0VSIiwiZXhwIjoxNzI5NjM3ODUzfQ.FxsJWbvaM7gRoCiDbSW3C9lix2Nw5VLnO7LaBC_gjv_EG-H5iEu2EDyCdRGXhSpZ69C2t1aAccrsrxydvGNUIOY_CXlaP1gMTxDU0Cx9DQ6cb9-nCv2OAejxoWgUs21cBWiuNRWwQwaZ-kEPTp50mDyg1UMj43W_AQmWxjS-dHhA8sYEbJA3OLWkXb9oQTZ9dv5ybcv3175t0aKvKhoqetvEzT7WhTzLU07JSSmdnFpzuyjmJCsyBr7bx670M-5DpO4TukbUQvxHHhlJ1zVldz-Pv4PPpoG3R3MAV4tkxa2ZcHBHOa1pcDvzb1ZnOdE_Dn39pxIP0oMHwNgE-URSjQ" -F "file=@D:\FoodScanBackend\inveption_test\100332.jpg"

# 查询结果
curl.exe -G "http://localhost:81/poll/result?task_id=409324d8-41e3-44c7-b5a0-2bffbdc9d48c" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcGVuaWQiOiJ0ZXN0MiIsInBlcm1pc3Npb24iOiJVU0VSIiwiZXhwIjoxNzI5NjM1NjM3fQ.Fr5sxrjSSt-PIrJYnlMEXQnelXd2kMX1xbvriUNp0hWRwe1heLCno6J0miire6-akhi_qlJmlO46flh6ULDLKNYVuFWHP-xak4jTE5AzUPOj5X83xK0BHZeB-qH8tEluJm_bcFyXa715mnlaA8frU7MWzn3YX2qL8BPGbPDC1K9hS9fWsJQwecssxoj6lOpYTJVyva3nsjLoJ7VZ1CUCWnj3sBbIf3rU-FMC2EgbF6x6W2877yyhGKR1_NJsHRBCfS1vEaJeKaS2SCUNB2m4y2Jmo2TOK2YLr9LC4_dcyBHC0Ks2OieIgn3aoGdRgAmXhXH83WdczTlEuL_I8aSaTA"

# 查询历史
curl.exe -G "http://localhost:81/poll/currentuser" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvcGVuaWQiOiJ0ZXN0MiIsInBlcm1pc3Npb24iOiJVU0VSIiwiZXhwIjoxNzI5NjEyMTUwfQ.go7d9hjr2WSGzTUfNgYLP3IOfylPdTvHoOgUG8cG5A01p9HftAVnygqQNCpN_2ax5xsgmhYYR-G0Soij_460uNdyuGdyLbf7Lwi8ZdX5CS56pE5d7VQSiECNWBEZosHFb693q4m4XieAX0WZVZZU0g8SkxxDxjDN0mZptl08E9qrAKgvXPLtEzqawy90ts7NBaOQtmXHhgLBAz5QBl9DZ--pBgEtSaiZPiyrvuZY1CZP-07lQJWm3LJOFkuDpVypK9OWS_IyNUJkRFdfkRAwOQTnsgY_N4Idxwrkx3AgKxEA2GWl442DLYTkX4kM5do_1qcs6wv3c8aqNLnhYZAWMA"

# 修改时用
DROP TABLE IF EXISTS history;
# 保留history，删除外键关系
ALTER TABLE history DROP CONSTRAINT history_openid_fkey;
DROP TABLE IF EXISTS users;
# 重建users，增加外键关系
INSERT INTO users (openid)
SELECT DISTINCT openid FROM history
WHERE openid NOT IN (SELECT openid FROM users);

ALTER TABLE history
ADD CONSTRAINT history_openid_key
FOREIGN KEY (openid)
ON DELETE CASCADE;
# 更新权限
UPDATE users
SET permission = 'USER
WHERE openid = 'test2';
# 更新为当前时间
UPDATE users
SET created_at = CURRENT_TIMESTAMP,
    updated_at = CURRENT_TIMESTAMP
WHERE openid = 'test2';
# 查询最新数据
SELECT * FROM history ORDER BY id DESC LIMIT 1;  -- 获取最新的一条记录