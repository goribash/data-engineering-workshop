import pandas as pd
import click
from tqdm.auto import tqdm
from sqlalchemy import create_engine


@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL username')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default='5432', help='PostgreSQL port')
@click.option('--pg-db', default='green_ny_taxi', help='PostgreSQL database name')
@click.option('--green-url', default='https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet', help='Green taxi data URL')
@click.option('--zones-url', default='https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv', help='Taxi zones lookup URL')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, green_url, zones_url):
    """Load green taxi trips and zones data into PostgreSQL."""

    engine = create_engine(
        f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"
    )

    steps = [
        "Read green trips",
        "Read zones",
        "Write green trips",
        "Write zones",
    ]

    with tqdm(total=len(steps), desc="NY Taxi Ingestion", unit="step") as pbar:
        click.echo("Loading green trips...")
        df_green = pd.read_parquet(green_url)
        click.echo(f"Green shape: {df_green.shape}")
        pbar.update(1)

        click.echo("Loading zones...")
        df_zones = pd.read_csv(zones_url)
        click.echo(f"Zones shape: {df_zones.shape}")
        pbar.update(1)

        click.echo("Writing green trips...")
        df_green.to_sql(
            name="green_trips",
            con=engine,
            if_exists="replace",
            index=False,
            method="multi",
        )
        pbar.update(1)

        click.echo("Writing zones...")
        df_zones.to_sql(
            name="zones",
            con=engine,
            if_exists="replace",
            index=False,
            method="multi",
        )
        pbar.update(1)

    click.echo("Data loaded successfully!")


if __name__ == "__main__":
    run()
