# data-alchemists-fyp-2025


### Build for local database

Requirements
- Docker and Docker Compose installed and available in your PATH. Ensure docker desktop is running and place backup_sql into db_files/db.



Step 1:
```sh
docker compose -f db_files/docker-compose.yaml up -d

```

Step 2:
```sh
docker exec -it data-alchemists-postgis-copy-ver psql -U postgres -c "CREATE DATABASE postgres;"
```


Step 3:
```sh
type db_files/db/local_copy.sql | docker exec -i data-alchemists-postgis-copy-ver psql -U postgres -d postgres

```



### Navigate to frontend folder
```sh
cd src
```

### Install dependencies 
```sh
pip install -r requirements.txt
```

### Run Flask app
```sh
python app.py
```

### Navigate to frontend folder
```sh
cd flood-viz
```

### Install dependencies
```sh
npm install
```

### Run development server
```sh
npm run dev
```

### Build for production
```sh
npm run build
```

### To access flask documentation after running application
```
http://localhost:5000/apidocs/#/
```



### To switch between supabase and local DB

```
1. Open `src/database.py` in an editor.

2. Swap the Supabase cloud client for the local Postgres wrapper or vice versa by commenting/uncommenting the blocks as mentioned in the comments. Only run either local or supabase ver.

```

