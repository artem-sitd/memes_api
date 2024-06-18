# memes_api

IN PROGRES...

docker run -p 9000:9000 -p 9001:9001 -e MINIO_ROOT_USER=minioadmin -e MINIO_ROOT_PASSWORD=minioadmin
docker.io/minio/minio server /home/art/minio_data --console-address ":9001"

Необходимо проработать механизм создания бакета
я думаю, сначала в .env указываем имя будущего бакета, далее собираем все контйнеры, и перейдя в консоль бакета создать
такой же бакет