docker build -t visualcla .
docker run -it --rm --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=all -p 9321:9321 visualcla