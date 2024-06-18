import numpy as np
import pandas as pd


def main() -> None:
    # read both sheets in as pandas dataframes
    df_menu_items = pd.read_excel(
        "data/restaurant_data.xlsx", sheet_name="Restaurant Menu Items"
    )
    # df_reference_categories = pd.read_excel(
    #     "data/restaurant_data.xlsx", sheet_name="Reference categories"
    # )

    # drop rows where "Product Name" is blank or null
    print(df_menu_items.shape)
    df_menu_items["Product Name"] = df_menu_items["Product Name"].replace("", np.nan)
    df_menu_items = df_menu_items.dropna(subset=["Product Name"])
    print(df_menu_items.shape)

    # drop rows where "Ingredients on Product Page" is blank or null
    print(df_menu_items.shape)
    df_menu_items["Ingredients on Product Page"] = df_menu_items[
        "Ingredients on Product Page"
    ].replace("", np.nan)
    df_menu_items = df_menu_items.dropna(subset=["Ingredients on Product Page"])
    print(df_menu_items.shape)


if __name__ == "__main__":
    main()
