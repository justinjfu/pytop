nvidia-smi --query-compute-apps=pid,name,used_memory,gpu_bus_id --format=csv
echo 'BREAK'
nvidia-smi --query-gpu=name,gpu_bus_id,memory.total,memory.used,utilization.gpu,temperature.gpu --format=csv
echo 'BREAK'
top -b -n 1
echo 'BREAK'
docker ps
