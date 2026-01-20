/* Question 3 — Counting short trips

For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a trip_distance of less than or equal to 1 mile? */

SELECT COUNT(*) AS short_trips_count
FROM public.green_trips
WHERE lpep_pickup_datetime >= '2025-11-01'
  AND lpep_pickup_datetime <  '2025-12-01'
  AND trip_distance IS NOT NULL
  AND trip_distance <= 1;

Answer: 8007

/* Question 4 — Longest trip for each day

Which was the pickup day with the longest trip distance?
Only consider trips with trip_distance less than 100 miles (to exclude data errors).*/

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


Answer: 2025-11-14

/*Question 5 — Biggest pickup zone

Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?*/

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


Answer: East Harlem North

/* Question 6 — Largest tip (minimal version)

For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?*/
(Minimal version — assuming your table contains only November 2025 data.)

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