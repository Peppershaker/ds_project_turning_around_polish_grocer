import os
import pickle
import pandas as pd
from flask import request, Flask

app_root = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, root_path=app_root)


def get_n_similar_items_for_sku(sku, n, item_item_df,
                                product_description_df, print_item_desc=False,
                                return_as_json=False):
    """
    Looks through the item-item similarity matrix and returns the
    top n similar items for a given sku

    Args:
        sku: int
            SKU to get top n similar items

        n: int
            Number of similar items to return

        item_item_df: DataFrame
            Pre-computed item-item similarity matrix as pd.DataFrame
            and indexed on integer valued SKUs

        product_description_df: DataFrame
            Df holding item descriptions indexed on integer valued SKUs

        print_item_desc: bool
            Set true to print requestd sku product name and category

        return_as_json: bool
            Returns JSON instead of DataFrame

    Returns:
        items: DataFrame or JSON
            Df or JSON containing top n similar items with product information
            Use return_as_json argument to set return data type
    """

    top_n_skus = item_item_df.loc[:, sku].sort_values(ascending=False).iloc[:n]
    top_n_skus = pd.DataFrame(top_n_skus).join(
        product_description_df, how='left')
    top_n_skus.columns = ['similarity', 'category', 'name']

    if print_item_desc:
        item = product_description_df.loc[sku]
        s = "Top {} items /w similar purchase pattern to {} ({}) are as follows"
        print(s.format(n, item.loc["name"], item.group))

    if return_as_json:
        return top_n_skus.to_json(orient="records")

    return top_n_skus


def load_pickled_data():
    """Loads and returns the pickled model to be used for prediction"""

    with open("model/item_item_df.pickle", 'rb') as f:
        item_item_df, product_description_df = pickle.load(f)

    return item_item_df, product_description_df


@app.route('/api/v1.0/predict', methods=['GET'])
def process_api_call():
    """
    End point for item-item collaborative filter recommender system

    Parameters
    ==========
    sku
        The sku to get recommendations for

    n
        Number of recommendations to get
    """

    query_params = request.args
    sku = query_params.get('sku')
    n = query_params.get('n')

    response_json = get_n_similar_items_for_sku(sku,
                                                n,
                                                item_item_df,
                                                product_description_df,
                                                return_as_json=True)

    return response_json, 200


item_item_df, product_description_df = load_pickled_data()
