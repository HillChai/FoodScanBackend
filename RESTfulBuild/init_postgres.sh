#!/bin/bash
set -e

echo "Waiting for postgres to start"
until psql -U "$POSTGRES_USER" -c '\q'; do
    echo "Postgres is unavailable - sleeping"
    sleep 1
done

echo "Postgres is up - executing command"

# 检查users表是否存在
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<EOSQL
    
    -- 创建 PERMISSION 枚举类型（如果不存在）
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'PERMISSION') THEN
            CREATE TYPE PERMISSION AS ENUM ('NO_PERMISSION', 'USER', 'ADMIN');
        END IF;
    END\$\$;

    -- 创建 users 表（如果不存在）
    CREATE TABLE IF NOT EXISTS users (
        openid VARCHAR(255) PRIMARY KEY,
        head_url VARCHAR(1024),
        name VARCHAR(255),
        gold_coin INTEGER,
        experience INTEGER,
        permission PERMISSION NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        email VARCHAR(50),
        phone_number VARCHAR(20),
        signature VARCHAR(255)
    );
EOSQL
echo "Database, permission enum type and users table created"

# 检查history表是否存在
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<EOSQL
    CREATE TABLE IF NOT EXISTS history (
        id SERIAL PRIMARY KEY,
        task_id UUID NOT NULL, 
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        image_path VARCHAR(255) NOT NULL,
        presigned_url VARCHAR(2048) NOT NULL,
        inference_result VARCHAR(255) NOT NULL,
        weight_result FLOAT NOT NULL,
        openid VARCHAR(255) NOT NULL,
        FOREIGN KEY (openid) REFERENCES users(openid)
    );
    CREATE INDEX IF NOT EXISTS idx_history_id ON history (id);
EOSQL
echo "history table created"