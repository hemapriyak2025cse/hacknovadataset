SYNTHETIC CHENNAI PUBLIC TRANSPORT OD DATASET
===============================================

This dataset is FULLY SYNTHETIC and is intended only for a 24-hour hackathon
MVP/demo for "Predictive Public Transportation Reliability and Adaptive
Transit Management."

No real passenger records, real ticket IDs, names, phone numbers, addresses,
payment details, or other personally identifiable information are included.

FILES
-----
1. route_stops.csv

Columns:
- route_id: Synthetic route identifier (R01-R05).
- stop_sequence: Ordered position of the stop on that route.
- stop_id: Synthetic stop identifier.
- stop_name: Chennai geographical-context stop label used for the demo.

2. passenger_tickets.csv

Columns:
- ticket_id: Unique synthetic transaction identifier; not a real ticket ID.
- bus_id: Synthetic bus identifier.
- route_id: Route served by the bus.
- source_stop: Passenger boarding stop.
- destination_stop: Passenger destination stop.
- boarding_date: Synthetic service date for the hackathon demo.
- boarding_time: Synthetic boarding time between 06:00 and 22:00.
- passenger_count: Number of passengers represented by the synthetic transaction.

The synthetic boarding dates in this file range from 2026-09-01 to 2026-09-14.
They are demonstration dates only and do not represent real MTC ticketing data.

OD ANALYSIS
-----------
Every source_stop and destination_stop belongs to the same route, and the
destination always occurs later in stop_sequence.

The date column allows the MVP to simulate a disruption on a particular day.

Example:
1. Select disruption date = 2026-09-10.
2. Select broken bus = B101.
3. Select breakdown stop = Guindy.
4. Filter passenger_tickets.csv for B101 on that date.
5. Identify passengers whose journey has reached/started before Guindy and
   whose destination is after Guindy.
6. Sum passenger_count for the affected transactions.
7. Group the affected demand by source_stop -> destination_stop.
8. Search alternative routes/buses serving the required downstream stops.
9. Compare capacity, traffic, ETA, headway and disruption status.
10. Recommend the best alternative and estimate ripple impact.

Because every transaction has an ordered source and destination on its route,
the same logic can be used to simulate a breakdown at ANY stop on ANY route.

BREAKDOWN LOGIC
---------------
For a breakdown at a route stop with sequence K, a simple MVP rule is:

affected =
    same bus AND same service date
    AND source_stop_sequence <= K
    AND destination_stop_sequence > K

This identifies passengers whose planned trip continues beyond the breakdown
point. A production system can make this more precise using actual vehicle
position, boarding timestamp, stop arrival times and live AVL data.

ALTERNATIVE ROUTES / BUSES
--------------------------
For an MVP, consider an alternative route when it serves the affected
destination or a useful transfer stop. Then compare:
- available bus capacity
- expected arrival time
- traffic conditions
- route travel time
- current disruptions
- number of affected passengers

REPLACING THE SYNTHETIC DATA
----------------------------
Later, these CSV files can be replaced with an authorized electronic
ticketing API, automatic passenger counting (APC), automatic vehicle
location (AVL), GTFS/GTFS-Realtime, or another transport-operator data source.
Only data that the project is explicitly authorized to access should be used,
with appropriate privacy and security controls.

DATA VALIDATION
---------------
The files were programmatically checked for:
- exactly 5,000 passenger transactions
- unique ticket_id values
- correct bus_id -> route_id mapping
- valid source and destination stops
- source and destination on the same route
- destination sequence after source sequence
- boarding times within 06:00-22:00
- valid synthetic boarding dates
- no invalid route-stop combinations
- all five routes receiving passengers
- higher passenger_count during morning/evening peaks
- noticeably higher transaction volume at high-demand source stops
- Chennai-only stop names; no Coimbatore-specific locations

IMPORTANT
---------
This is synthetic demonstration data. It must NOT be represented as real
Chennai passenger or ticketing data.
