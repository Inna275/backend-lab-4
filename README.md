# backend-lab-3

## Variant

| Group number | Formula    | Variant    |
|--------------|------------|------------|
| 34           | 34 % 3 = 1 | Currencies |

## How to run

### 1. Access the deployed service
https://backend-lab-3-aark.onrender.com

### 2. Run locally
1. Make sure you have Docker and Docker Compose installed.
   - [Install Docker](https://www.docker.com/get-started)  
   - [Install Docker Compose](https://docs.docker.com/compose/install)
2. Clone the repository:
   ```bash
   git clone https://github.com/Inna275/backend-lab-3.git
   ```
3. Navigate to the project folder:
   ```bash
   cd backend-lab-3
   ```
4. Create a `.env` file with the following variables:
   ```env
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   POSTGRES_DB=backend_lab_3
   ```
5. Build and run the containers:
   ```bash
   docker-compose build
   docker-compose up
   ```
6. Access the endpoints on http://localhost:8080
