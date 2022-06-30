#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Common has base.py and tables.py


#base.py


from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base

engine = create_engine(
    "postgresql+psycopg2://repl:S3cretPassw0rd@localhost:5432/campdata_prod"
)
session = Session(engine)
Base = declarative_base()




#tables.py 

from sqlalchemy import cast, Column, Integer, String, Date
from sqlalchemy.orm import column_property

#from common.base import Base


class PprRawAll(Base):
    __tablename__ = "ppr_raw_all"

    id = Column(Integer, primary_key=True)
    date_of_sale = Column(String(55))
    address = Column(String(255))
    postal_code = Column(String(55))
    county = Column(String(55))
    price = Column(String(55))
    description = Column(String(255))
    transaction_id = column_property(
        date_of_sale + "_" + address + "_" + county + "_" + price
    )


class PprCleanAll(Base):
    __tablename__ = "ppr_clean_all"

    id = Column(Integer, primary_key=True)
    date_of_sale = Column(Date)
    address = Column(String(255))
    postal_code = Column(String(55))
    county = Column(String(55))
    price = Column(Integer)
    description = Column(String(255))
    transaction_id = column_property(
        cast(date_of_sale, String)
        + "_"
        + address
        + "_"
        + county
        + "_"
        + cast(price, String)
    )


# In[1]:


#Extract 

import os
import csv
import tempfile
from zipfile import ZipFile

import requests

# Settings
#/Users/zizeng/Downloads
base_path = os.path.abspath("/Users/zizeng/Downloads")

# START - Paths for new February 2021 data available

# External website file url
source_url = "https://assets.datacamp.com/production/repositories/5899/datasets/66691278303f789ca4acd3c6406baa5fc6adaf28/PPR-ALL.zip"

# Source path where we want to save the .zip file downloaded from the website
source_path = f"{base_path}/data/source/downloaded_at=2021-02-01/PPR-ALL.zip"

# Raw path where we want to extract the new .csv data
raw_path = f"{base_path}/data/raw/downloaded_at=2021-02-01/ppr-all.csv"

# Source path where we want to save the .zip file downloaded from the website
#source_path = f"{base_path}"

# Raw path where we want to extract the new .csv data
#raw_path = f"{base_path}"

# END - Paths for new February 2021 data available


def create_folder_if_not_exists(path):
    """
    Create a new folder if it doesn't exists
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)


def download_snapshot():
    """
    Download a new snapshot from the source
    """
    create_folder_if_not_exists(source_path)
    with open(source_path, "wb") as source_ppr:
        response = requests.get(source_url, verify=False)
        source_ppr.write(response.content)


def save_new_raw_data():
    """
    Save new raw data from the current snapshot from the source
    """

    create_folder_if_not_exists(raw_path)
    with tempfile.TemporaryDirectory() as dirpath:
        with ZipFile(
            source_path,
            "r",
        ) as zipfile:
            names_list = zipfile.namelist()
            csv_file_path = zipfile.extract(names_list[0], path=dirpath)
            # Open the CSV file in read mode
            with open(csv_file_path, mode="r", encoding="windows-1252") as csv_file:
                reader = csv.DictReader(csv_file)

                row = next(reader)  # Get first row from reader
                print("[Extract] First row example:", row)

                # Open the CSV file in write mode
                with open(
                    raw_path,
                    mode="w",
                    encoding="windows-1252",
                ) as csv_file:
                    # Rename field names so they're ready for the next step
                    fieldnames = {
                        "Date of Sale (dd/mm/yyyy)": "date_of_sale",
                        "Address": "address",
                        "Postal Code": "postal_code",
                        "County": "county",
                        "Price (€)": "price",
                        "Description of Property": "description",
                    }
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    # Write headers as first line
                    writer.writerow(fieldnames)
                    for row in reader:
                        # Write all rows in file
                        writer.writerow(row)


def main():
    print("[Extract] Start")
    print("[Extract] Downloading snapshot")
    download_snapshot()
    print(f"[Extract] Saving data from '{source_path}' to '{raw_path}'")
    save_new_raw_data()
    print(f"[Extract] End")


# 

# In[2]:


main()


# In[7]:


#import pandas as pd

#pd.read_csv('/Users/zizeng/Downloads/data/raw/downloaded_at=2021-02-01/ppr-all.csv', encoding = 'unicode_escape')


# In[3]:


#Transform 

import os
import csv
from datetime import datetime

from common.tables import PprRawAll
from common.base import session
from sqlalchemy import text

# Settings
base_path = os.path.abspath(__file__ + "/../../")

# START - Paths for new February 2021 data available

# Raw path where we want to extract the new .csv data
raw_path = f"{base_path}/data/raw/downloaded_at=2021-02-01/ppr-all.csv"

# END - Paths for new February 2021 data available


def transform_case(input_string):
    """
    Lowercase string fields
    """
    return input_string.lower()


def update_date_of_sale(date_input):
    """
    Update date format from DD/MM/YYYY to YYYY-MM-DD
    """
    current_format = datetime.strptime(date_input, "%d/%m/%Y")
    new_format = current_format.strftime("%Y-%m-%d")
    return new_format


def update_description(description_input):
    """
    Simplify the description field for potentialy future analysis, just return:
    - "new" if string contains "new" substring
    - "second-hand" if string contains "second-hand" substring
    """
    description_input = transform_case(description_input)
    if "new" in description_input:
        return "new"
    elif "second-hand" in description_input:
        return "second-hand"
    return description_input


def update_price(price_input):
    """
    Return price as integer by removing:
    - "€" symbol
    - "," to convert the number into float first (e.g. from "€100,000.00" to "100000.00")
    """
    price_input = price_input.replace("€", "")
    price_input = float(price_input.replace(",", ""))
    return int(price_input)


def truncate_table():
    """
    Ensure that "ppr_raw_all" table is always in empty state before running any transformations.
    And primary key (id) restarts from 1.
    """
    session.execute(
        text("TRUNCATE TABLE ppr_raw_all;ALTER SEQUENCE ppr_raw_all_id_seq RESTART;")
    )
    session.commit()


def transform_new_data():
    """
    Apply all transformations for each row in the .csv file before saving it into database
    """
    with open(raw_path, mode="r", encoding="windows-1252") as csv_file:
        # Read the new .csv snapshot ready to be processed
        reader = csv.DictReader(csv_file)
        # Initialize an empty list for our PprRawAll objects
        ppr_raw_objects = []
        for row in reader:
            # Apply transformations and save as PprRawAll object
            ppr_raw_objects.append(
                PprRawAll(
                    date_of_sale=update_date_of_sale(row["date_of_sale"]),
                    address=transform_case(row["address"]),
                    postal_code=transform_case(row["postal_code"]),
                    county=transform_case(row["county"]),
                    price=update_price(row["price"]),
                    description=update_description(row["description"]),
                )
            )
        # Bulk save all new processed objects and commit
        session.bulk_save_objects(ppr_raw_objects)
        session.commit()


def main():
    print("[Transform] Start")
    print("[Transform] Remove any old data from ppr_raw_all table")
    truncate_table()
    print("[Transform] Transform new data available in ppr_raw_all table")
    transform_new_data()
    print("[Transform] End")


# In[ ]:


#Load 


from common.base import session
from common.tables import PprRawAll, PprCleanAll

from sqlalchemy import cast, Integer, Date
from sqlalchemy.dialects.postgresql import insert


def insert_transactions():
    """
    Insert operation: add new data
    """
    # Retrieve all the transaction ids from the clean table
    clean_transaction_ids = session.query(PprCleanAll.transaction_id)

    # date_of_sale and price needs to be casted as their
    # datatype is not string but, respectively, Date and Integer
    transactions_to_insert = session.query(
        cast(PprRawAll.date_of_sale, Date),
        PprRawAll.address,
        PprRawAll.postal_code,
        PprRawAll.county,
        cast(PprRawAll.price, Integer),
        PprRawAll.description,
    ).filter(~PprRawAll.transaction_id.in_(clean_transaction_ids))

    # Insert the rows from the previously selected transactions
    stm = insert(PprCleanAll).from_select(
        ["date_of_sale", "address", "postal_code", "county", "price", "description"],
        transactions_to_insert,
    )

    # Execute and commit the statement to make changes in the database.
    session.execute(stm)
    session.commit()


def delete_transactions():
    """
    Delete operation: delete any row not present in the last dataset
    """
    # Get all ppr_raw_all transaction ids
    raw_transaction_ids = session.query(PprRawAll.transaction_id)

    # Filter all the ppt_clean_all table transactions that are not present in the ppr_raw_all table
    # and delete them.
    # Passing synchronize_session as argument for the delete method.
    transactions_to_delete = session.query(PprCleanAll).filter(
        ~PprCleanAll.transaction_id.in_(raw_transaction_ids)
    )
    
    # Print transactions to delete
    print("Transactions to delete:", transactions_to_delete.count())

    # Delete transactions
    transactions_to_delete.delete(synchronize_session=False)

    # Commit the session to make the changes in the database
    session.commit()
    
def main():
    print("[Load] Start")
    print("[Load] Inserting new rows")
    insert_transactions()
    print("[Load] Deleting rows not available in the new transformed data")
    delete_transactions()
    print("[Load] End")


# In[ ]:


import extract
import transform
import load

if __name__ == "__main__":
    extract.main()
    transform.main()
    load.main()

