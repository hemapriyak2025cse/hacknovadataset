"""Passenger impact service."""
from app.utils.data_loader import tickets_df, route_stops_df


def get_affected_passengers(bus_id: str, route_id: str, breakdown_stop_seq: int, service_date: str = "2026-09-10") -> dict:
    df = tickets_df[
        (tickets_df["bus_id"] == bus_id) &
        (tickets_df["boarding_date"] == service_date)
    ]
    if df.empty:
        # Fallback: use any date for this bus
        df = tickets_df[tickets_df["bus_id"] == bus_id]

    affected = df[
        (df["source_seq"] <= breakdown_stop_seq) &
        (df["dest_seq"] > breakdown_stop_seq)
    ]

    affected_passengers = int(affected["passenger_count"].sum())
    affected_tickets = len(affected)

    # Group by source→destination
    od_groups = (
        affected.groupby(["source_stop", "destination_stop"])["passenger_count"]
        .sum()
        .reset_index()
        .rename(columns={"passenger_count": "count"})
        .to_dict("records")
    )

    # Downstream stops affected
    downstream = route_stops_df[
        (route_stops_df["route_id"] == route_id) &
        (route_stops_df["stop_sequence"] > breakdown_stop_seq)
    ]["stop_name"].tolist()

    return {
        "affected_passenger_count": affected_passengers,
        "affected_ticket_count": affected_tickets,
        "od_breakdown": od_groups,
        "downstream_stops": downstream,
        "service_date": service_date,
        "breakdown_stop_seq": breakdown_stop_seq,
    }
