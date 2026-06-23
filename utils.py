import streamlit as st
import pandas as pd


# ==========================
# RESET FUNCTION
# ==========================

def reset_filters(min_date, max_date):
    st.session_state.category = "All"
    st.session_state.store = "All"
    st.session_state.loyalty = "All"
    st.session_state.payment = "All"
    st.session_state.promotion = "All"
    st.session_state.date = (min_date, max_date)


# ==========================
# GLOBAL FILTERS
# ==========================

def sidebar_filters(df):

    st.sidebar.header("🔍 Filters")

    # Date format
    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"]
    )

    min_date = df["transaction_date"].min()
    max_date = df["transaction_date"].max()


    # ==========================
    # DATE FILTER
    # ==========================

    date = st.sidebar.date_input(
        "📅 Date Range",
        value=(min_date, max_date),
        key="date"
    )


    # ==========================
    # SELECTBOX FILTERS
    # ==========================

    category = st.sidebar.selectbox(
        "Category",
        ["All"] + sorted(
            df["category"].dropna().unique().tolist()
        ),
        key="category"
    )


    store = st.sidebar.selectbox(
        "Store Location",
        ["All"] + sorted(
            df["store_location"].dropna().unique().tolist()
        ),
        key="store"
    )


    loyalty = st.sidebar.selectbox(
        "Customer Loyalty",
        ["All"] + sorted(
            df["customer_loyalty_level"].dropna().unique().tolist()
        ),
        key="loyalty"
    )


    payment = st.sidebar.selectbox(
        "Payment Method",
        ["All"] + sorted(
            df["payment_method"].dropna().unique().tolist()
        ),
        key="payment"
    )


    promotion = st.sidebar.selectbox(
        "Promotion",
        [
            "All",
            "Promotion Applied",
            "No Promotion"
        ],
        key="promotion"
    )


    # ==========================
    # RESET BUTTON AT BOTTOM
    # ==========================

    st.sidebar.divider()

    st.sidebar.button(
        "🔄 Reset Filters",
        use_container_width=True,
        on_click=reset_filters,
        args=(min_date, max_date)
    )


    # ==========================
    # APPLY FILTERS
    # ==========================

    filtered_df = df.copy()


    # Date
    if len(date) == 2:
        filtered_df = filtered_df[
            (filtered_df["transaction_date"] >= pd.to_datetime(date[0])) &
            (filtered_df["transaction_date"] <= pd.to_datetime(date[1]))
        ]


    # Category
    if category != "All":
        filtered_df = filtered_df[
            filtered_df["category"] == category
        ]


    # Store
    if store != "All":
        filtered_df = filtered_df[
            filtered_df["store_location"] == store
        ]


    # Loyalty
    if loyalty != "All":
        filtered_df = filtered_df[
            filtered_df["customer_loyalty_level"] == loyalty
        ]


    # Payment
    if payment != "All":
        filtered_df = filtered_df[
            filtered_df["payment_method"] == payment
        ]


    # Promotion
    if promotion == "Promotion Applied":
        filtered_df = filtered_df[
            filtered_df["promotion_applied"] == 1
        ]

    elif promotion == "No Promotion":
        filtered_df = filtered_df[
            filtered_df["promotion_applied"] == 0
        ]


    return filtered_df