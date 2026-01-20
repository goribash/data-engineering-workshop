import click
import pandas as pd
from tqdm.auto import tqdm
from sqlalchemy import create_engine



dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]


@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default='5432', help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database')
@click.option('--target_table', default='yellow_taxi_data', help='Target table name')
@click.option('--year', type=int, default=2021, help='Year of the data')
@click.option('--month', type=int, default=1, help='Month of the data')
@click.option('--chunksize', type=int, default=100000, help='Chunk size for reading CSV')
@click.option('--url', default=None, help='Custom URL for the CSV file')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, target_table, year, month, chunksize, url):
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    if url is None:
        url = f'{prefix}yellow_tripdata_{year}-{month:02d}.csv.gz'

    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize,
    )
#ingestion loop
    first = True  
    for df_chunk in tqdm(df_iter):
        if first:
            #Create table schema in the database(no data inserted yet)
            df_chunk.head(0).to_sql(
                name=target_table,
                con=engine, if_exists='replace'
            )
            first = False
            print("Table created successfully.")
            #Insert Chunk into the database
            df_chunk.to_sql(
                name=target_table, 
                con=engine, if_exists='append'         
            )
            print("Inserted chunk:", len(df_chunk))

if __name__ == '__main__':
    run()
