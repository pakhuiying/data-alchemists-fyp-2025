Project Database — Docker Run Instructions

Requirements
- Docker and Docker Compose installed and available in your PATH.


Step 1:
docker compose -f db_files/docker-compose.yaml up -d

Step 2:
Get-Content db_files/db/local_copy.sql | docker exec -i data-alchemists-postgis-copy-ver psql -U postgres -d postgres

