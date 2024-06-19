import json

import numpy as np
import pandas as pd
from sqlalchemy import create_engine


def return_42() -> int:
    return 42


def drop_rows_blank_or_null(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    for col in cols:
        df.loc[:, col] = df[col].replace("", np.nan)
        df = df.dropna(subset=col)

    return df


def correct_mispellings(
    df: pd.DataFrame, col: str, corrections: dict[str, str]
) -> pd.DataFrame:
    for k, v in corrections.items():
        df.loc[df[col] == k, col] = v

    return df


def main() -> None:
    # read both sheets in as pandas dataframes
    df_menu_items = pd.read_excel(
        "data/restaurant_data.xlsx", sheet_name="Restaurant Menu Items"
    )
    df_reference_categories = pd.read_excel(
        "data/restaurant_data.xlsx", sheet_name="Reference categories"
    )

    # drop rows where blank or null
    print(
        "df_menu_items shape prior to removing blanks and nulls - "
        + str(df_menu_items.shape)
    )
    df_menu_items = drop_rows_blank_or_null(
        df=df_menu_items, cols=["Product Name", "Ingredients on Product Page", "Store"]
    )
    print(
        "df_menu_items shape after to removing blanks and nulls - "
        + str(df_menu_items.shape)
        + "\n\n"
    )

    # check the store names for any mispellings
    print("unique store names:")
    print(np.sort(df_menu_items["Store"].unique()))
    print("\n")
    # check the category names for any mispellings
    print("unique fig category names:")
    print(np.sort(df_reference_categories["Fig Category 1"].unique()))
    print("\n")
    # correct the mispellings
    df_menu_items = correct_mispellings(
        df=df_menu_items, col="Store", corrections={"MacDonald's": "McDonald’s"}
    )
    print("unique store names after correcting mispelling:")
    print(np.sort(df_menu_items["Store"].unique()))
    print("\n")

    # filter dataset to requested columns
    df_menu_items = df_menu_items[
        [
            "Store",
            "Product Name",
            "Product category",
            "Ingredients on Product Page",
            "Allergens and Warnings",
            "URL of primary product picture",
        ]
    ].rename(
        columns={
            "Store": "Restaurant",
            "Product Name": "Menu Item",
            "Product category": "Restaurant Category",
            "Ingredients on Product Page": "Ingredients",
            "Allergens and Warnings": "Allergens",
            "URL of primary product picture": "Picture URL",
        }
    )

    # join to the dataset in the second excel sheet to get the fig category
    df_reference_categories = df_reference_categories.rename(
        columns={
            "Restaurant name": "Restaurant",
            "Restaurant original category": "Restaurant Category",
        }
    )
    df_final = pd.merge(
        df_menu_items,
        df_reference_categories,
        how="left",
        on=["Restaurant", "Restaurant Category"],
    )
    df_final.info()

    # connect to local MySQL database
    CONFIG_MYSQL = json.load(open("CONFIG_MYSQL.json", "r"))
    engine = create_engine(
        "mysql+mysqldb://"
        + CONFIG_MYSQL["username"]
        + ":"
        + CONFIG_MYSQL["password"]
        + "@localhost:3306/fig",
        echo=False,
    )

    # insert into MySQL fig_category table
    df_fig_category = pd.DataFrame(
        df_final["Fig Category 1"].unique(), columns=["name"]
    ).dropna()
    df_fig_category.to_sql(
        con=engine, name="fig_category", if_exists="append", index=False
    )

    # insert into MySQL restaurant table
    df_restaurant = pd.DataFrame(
        df_final["Restaurant"].unique(), columns=["name"]
    ).dropna()
    df_restaurant.to_sql(con=engine, name="restaurant", if_exists="append", index=False)

    # get the information back from the MySQL tables
    # in order to retrieve the auto incremented ids
    df_fig_category_with_ids = pd.read_sql("SELECT * FROM fig_category", con=engine)
    df_restaurant_with_ids = pd.read_sql("SELECT * FROM restaurant", con=engine)
    df_final = pd.merge(
        df_final,
        df_fig_category_with_ids.rename(columns={"name": "Fig Category 1"}),
        how="left",
        on="Fig Category 1",
    )
    df_final = pd.merge(
        df_final,
        df_restaurant_with_ids.rename(columns={"name": "Restaurant"}),
        how="left",
        on="Restaurant",
    )

    # insert into MySQL menu_item table
    df_final = df_final[
        [
            "Menu Item",
            "Ingredients",
            "Allergens",
            "Picture URL",
            "restaurant_id",
            "fig_category_id",
        ]
    ].rename(
        columns={
            "Menu Item": "name",
            "Ingredients": "ingredients",
            "Allergens": "allergens",
            "Picture URL": "picture_url",
        }
    )
    df_final.to_sql(con=engine, name="menu_item", if_exists="append", index=False)


if __name__ == "__main__":
    main()
