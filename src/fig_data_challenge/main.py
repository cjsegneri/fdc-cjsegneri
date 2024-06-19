import numpy as np
import pandas as pd
from sqlalchemy import create_engine


def main() -> None:
    # read both sheets in as pandas dataframes
    df_menu_items = pd.read_excel(
        "data/restaurant_data.xlsx", sheet_name="Restaurant Menu Items"
    )
    df_reference_categories = pd.read_excel(
        "data/restaurant_data.xlsx", sheet_name="Reference categories"
    )

    # drop rows where blank or null
    print(df_menu_items.shape)
    df_menu_items["Product Name"] = df_menu_items["Product Name"].replace("", np.nan)
    df_menu_items["Ingredients on Product Page"] = df_menu_items[
        "Ingredients on Product Page"
    ].replace("", np.nan)
    df_menu_items["Store"] = df_menu_items["Store"].replace("", np.nan)
    df_menu_items = df_menu_items.dropna(
        subset=["Product Name", "Ingredients on Product Page", "Store"]
    )
    print(df_menu_items.shape)

    # check the store names for any mispellings
    print(np.sort(df_menu_items["Store"].unique()))
    # correct the mispellings
    df_menu_items.loc[df_menu_items["Store"] == "MacDonald's", "Store"] = "McDonald’s"
    print(np.sort(df_menu_items["Store"].unique()))

    # check the category names for any mispellings
    print(np.sort(df_reference_categories["Fig Category 1"].unique()))

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
    engine = create_engine("mysql+mysqldb://root:root@localhost:3306/fig", echo=False)

    # insert into MySQL fig_category table
    df_fig_category = pd.DataFrame(
        df_final["Fig Category 1"].unique(), columns=["name"]
    ).dropna()
    df_fig_category.to_sql(
        con=engine, name="fig_category", if_exists="append", index=False
    )

    # insert into MySQL menu_category table
    df_menu_category = pd.DataFrame(
        df_final["Restaurant Category"].unique(), columns=["name"]
    ).dropna()
    df_menu_category.to_sql(
        con=engine, name="menu_category", if_exists="append", index=False
    )

    # insert into MySQL restaurant table
    df_restaurant = pd.DataFrame(
        df_final["Restaurant"].unique(), columns=["name"]
    ).dropna()
    df_restaurant.to_sql(con=engine, name="restaurant", if_exists="append", index=False)

    # get the information back from the MySQL tables
    # in order to retrieve the auto incremented ids
    df_fig_category_with_ids = pd.read_sql("SELECT * FROM fig_category", con=engine)
    df_menu_category_with_ids = pd.read_sql("SELECT * FROM menu_category", con=engine)
    df_restaurant_with_ids = pd.read_sql("SELECT * FROM restaurant", con=engine)
    df_final = pd.merge(
        df_final,
        df_fig_category_with_ids.rename(columns={"name": "Fig Category 1"}),
        how="left",
        on="Fig Category 1",
    )
    df_final = pd.merge(
        df_final,
        df_menu_category_with_ids.rename(columns={"name": "Restaurant Category"}),
        how="left",
        on="Restaurant Category",
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
            "menu_category_id",
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
