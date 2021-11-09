import pandas as pd
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider


cloud_config = {
        'secure_connect_bundle': './secure-connect-flightfare.zip'
}
auth_provider = PlainTextAuthProvider(username='RpwgRzZyyZbpvRqWkhmEMJWN', password='uFdlw+RKmuro_5_2KtasNSA5cyKZFQ6r'
                                                                                    'm9234lImqaQWW7uC-1J4Ms1IwHR_yOOrC.'
                                                                                    'K8Ne6ca,Xf8jUUzlKWHY4j9naNbO9su8Du'
                                                                                    'Z5l_yQYWe4Cz_Bq3JaSQDyz0TIfz')
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect('mykeyspace')




def pandas_factory(colnames, rows):
    return pd.DataFrame(rows, columns=colnames)


def get_flight_dataframe():
    session.row_factory = pandas_factory
    session.default_fetch_size = None


    rows = session.execute("SELECT * FROM mykeyspace.good_data")
    df = rows._current_rows
    return df
