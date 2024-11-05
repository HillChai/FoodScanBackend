#!/bin/bash

minio server /data &

until mc alias set foodminio http://localhost:9000 minioadmin minio123 > /dev/null 2>&1; do
    echo "Waiting for minio to start"
    sleep 1
done

echo "Minio is up - creating bucket"

BUCKET_NAME=${BUCKET_NAME}

if ! mc ls foodminio/$BUCKET_NAME > /dev/null 2>&1; then
    mc mb foodminio/$BUCKET_NAME
    echo "Bucket $BUCKET_NAME created"
else
    echo "Bucket $BUCKET_NAME already exists"
fi

wait