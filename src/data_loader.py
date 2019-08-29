"""
Description: Module containing helper functions to load in data
             used in notebooks
Author: Victor Xu
Date: Jun 2019
"""

import os
import pandas as pd


def load_monthly_data():
    """Loads monthly sales data from  csv"""

    project_root_dir = os.path.abspath(
        os.path.join(
            os.path.join(
                __file__,
                os.pardir),
            os.pardir))

    monthly = pd.read_csv(
        os.path.join(project_root_dir, 'data/monthly_sale_by_sku.csv'),
        delimiter=';',
        decimal=',',
        encoding='latin-1')
    monthly = monthly.rename(columns={
        'Date': 'date',
        'PKod': 'sku',
        'Pgroup': 'group',
        'Pname': 'name',
        'Pquantity': 'quantity',
        'pce_zn': 'unit_cogs',
        'pwa_zn': 'agg_cogs',  # aggregate cogs for this sku
        'pce_sn': 'unit_revenue',
        'pwn_sn': 'agg_rev',  # aggregate revenue for this sku
        'pmarza': 'gross_margin',
        'pmarzajedn': 'unit_contribution',
        'pkwmarza': 'agg_dollar_contribution',
        'pudzmarza': 'share_of_margin'
    })

    monthly = monthly.drop(['pwa_sn', 'pce_sb', 'pwa_sb', 'pudzsb'], axis=1)
    monthly.group = monthly.group.str.lower()
    monthly.name = monthly.name.str.lower()
    monthly.date = pd.to_datetime(monthly.date, format="%d.%m.%Y")
    monthly.unit_cogs = monthly.unit_cogs.str.replace(
        ',', '.').str.replace(
        ' ', '')

    monthly.group = monthly.group.replace(
        {"ketch_concetrate_mustard_majo_horseradish": "sauce"})

    return monthly
