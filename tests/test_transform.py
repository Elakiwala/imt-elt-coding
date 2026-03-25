import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

from src.transform import (
    _drop_internal_columns,
    transform_products,
    transform_users,
    transform_orders,
)


class TestDropInternalColumns:
    """Tests for the _drop_internal_columns() helper."""
    # Test that columns starting with '_' are removed
    def test_supprimer_underscore_colonnes(self):
        exemple = {"col1": [1, 2, 3], "col2": ["a", "b", "c"], "_internal_col": [1, 2, 3]}
        df = pd.DataFrame(exemple)
        sans_underscore = _drop_internal_columns(df)
        assert "_internal_col" not in sans_underscore.columns
        assert "col1" in sans_underscore.columns
        assert "col2" in sans_underscore.columns

    # Test that regular columns are kept
    def test_conserver_colonnes_normales(self):
        exemple = {"film": ["Fast and Furious", "The Matrix", "Dune 3"], "serie": ["Outlander", "The Walking Dead", "The Witcher"]}
        df = pd.DataFrame(exemple)
        resultat = _drop_internal_columns(df)
        assert list(resultat.columns) == ["film", "serie"]

    # Test edge case: empty DataFrame
    def test_dataframe_vide(self):
        df = pd.DataFrame()
        resultat = _drop_internal_columns(df)
        assert list(resultat.columns) == []


class TestTransformProducts:
    """Tests for transform_products()."""
    # Mock _read_bronze to return sample_products fixture
    @patch("src.transform._read_bronze")
    # Mock _load_to_silver so it doesn't hit the DB
    @patch("src.transform._load_to_silver")
    # Test that invalid prices (<=0) are removed
    def test_supprimer_prix_invalides(self, mock_load, mock_read, sample_products):
        mock_read.return_value = sample_products
        transform_products()
        df_charge = mock_load.call_args[0][0]  # Get the DataFrame passed to _load_to_silver
        assert all(df_charge["price_usd"] > 0), "Des prix invalides (<=0) ne devraient pas être présents"
    # Test that tags are normalized ('|' replaced with ', ')
    # Test that boolean columns are converted


class TestTransformUsers:
    """Tests for transform_users()."""
    # Test that PII columns (_hashed_password, _last_ip, etc.) are removed
    # Test that NULL loyalty_tier is filled with 'none'
    # Test that emails are lowercased and stripped


class TestTransformOrders:
    """Tests for transform_orders()."""
    # Test that invalid statuses are flagged/removed
    # Test that order_date is converted to datetime
    # Test that NULL coupon_code is replaced with ''