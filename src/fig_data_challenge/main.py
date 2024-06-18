import numpy as np
import pandas as pd


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


if __name__ == "__main__":
    main()
