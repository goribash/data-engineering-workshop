Module 1: Docker & SQL
Focus: Homework solutions and key learnings for Docker, SQL, and Terraform basics.

Question 1. Understanding Docker images
Run docker with the python:3.13 image. Use an entrypoint bash to interact with the container.
What's the version of pip in the image?

docker run -it --entrypoint bash python:3.13
pip --version

Answer - 25.3

Question 2. Understanding Docker networking and docker-compose
Given the following docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?

services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data

Answer - db:5432


Question 3. Counting short trips
For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a trip_distance of less than or equal to 1 mile?

SELECT COUNT(*) AS short_trips_count
FROM public.green_trips
WHERE lpep_pickup_datetime >= '2025-11-01'
  AND lpep_pickup_datetime <  '2025-12-01'
  AND trip_distance IS NOT NULL
  AND trip_distance <= 1;

Answer -- 8,007

Question 4. Longest trip for each day
Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles (to exclude data errors).

WITH daily_max AS (
  SELECT
      DATE(lpep_pickup_datetime) AS pickup_day,
      MAX(trip_distance)         AS max_trip_distance
  FROM public.green_trips
  WHERE trip_distance < 100
    AND trip_distance IS NOT NULL
    AND lpep_pickup_datetime >= '2025-11-01'
    AND lpep_pickup_datetime <  '2025-12-01'
  GROUP BY 1
)
SELECT
    pickup_day,
    max_trip_distance
FROM daily_max
ORDER BY max_trip_distance DESC
LIMIT 1;

Answer - 2025-11-14

Question 5. Biggest pickup zone
Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?

SELECT
    z."Zone"             AS pickup_zone,
    SUM(t.total_amount) AS total_revenue
FROM public.green_trips t
JOIN public.zones z
  ON t."PULocationID" = z."LocationID"
WHERE t.lpep_pickup_datetime >= '2025-11-18'
  AND t.lpep_pickup_datetime <  '2025-11-19'
GROUP BY 1
ORDER BY total_revenue DESC
LIMIT 1;
Answer --- East Harlem North

Question 6. Largest tip
For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?

SELECT
  dz."Zone" AS dropoff_zone,
  MAX(t.tip_amount) AS largest_tip
FROM public.green_trips t
JOIN public.zones pz
  ON t."PULocationID" = pz."LocationID"
JOIN public.zones dz
  ON t."DOLocationID" = dz."LocationID"
WHERE pz."Zone" = 'East Harlem North'
  AND t.tip_amount IS NOT NULL
GROUP BY dz."Zone"
ORDER BY largest_tip DESC
LIMIT 1;

Answer - Yorkville West



Question 7. Terraform Workflow
Which of the following sequences, respectively, describes the workflow for:

Downloading the provider plugins and setting up backend,
Generating proposed changes and auto-executing the plan
Remove all resources managed by terraform`

Answer:
terraform init, terraform apply -auto-approve, terraform destroy

