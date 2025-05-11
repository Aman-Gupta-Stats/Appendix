import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
import pycountry
import geopandas as gpd
import folium
from folium.features import GeoJsonTooltip
from folium.plugins import AntPath
import itertools
import time
import bisect
from datetime import timedelta

# Setup
st.set_page_config(page_title="Transaction Network Map", layout="wide")
st.title("Transaction Network Map")

@st.cache_data
def load_data():
    df = pd.read_csv('Data/synthetic_company_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df.sort_values('date')

@st.cache_data
def load_world():
    url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json'
    world = gpd.read_file(url)
    def iso3_to_2(code):
        try:
            return pycountry.countries.get(alpha_3=code).alpha_2
        except:
            return None
    world['iso2'] = world['id'].map(iso3_to_2)
    proj = world.to_crs(epsg=3857)
    ctr = gpd.GeoSeries(proj.geometry.centroid, crs='epsg:3857') \
             .to_crs(epsg=4326)
    world['centroid_lat'] = ctr.y
    world['centroid_lon'] = ctr.x
    lookup = world.dropna(subset=['iso2']) \
                  .set_index('iso2')[['centroid_lat','centroid_lon']] \
                  .to_dict('index')
    return world, lookup

# Load data
df = load_data()
world, lookup = load_world()

# Add coordinates
df['origin_iso'] = df['origin'].apply(lambda x: pycountry.countries.lookup(x).alpha_2)
df['dest_iso']   = df['destination'].apply(lambda x: pycountry.countries.lookup(x).alpha_2)
for side, iso in [('origin', 'origin_iso'), ('destination', 'dest_iso')]:
    df[f'{side}_lat'] = df[iso].map(lambda c: lookup.get(c, {}).get('centroid_lat'))
    df[f'{side}_lon'] = df[iso].map(lambda c: lookup.get(c, {}).get('centroid_lon'))

# Color palette
t_palette = ["red", "green", "blue", "orange", "purple", "cyan", "magenta",
             "gold", "darkgreen", "darkred", "navy", "teal"]
t_palette_cycle = itertools.cycle(t_palette)
company_colors = {c: next(t_palette_cycle) for c in df['company'].unique()}

# Session-state defaults for playback
if 'play_date' not in st.session_state:
    st.session_state.play_date = None
if 'playing' not in st.session_state:
    st.session_state.playing = False

# Layout
col1, col2 = st.columns([1, 3])

with col1:
    # Date range picker
    min_date = df['date'].dt.date.min()
    max_date = df['date'].dt.date.max()
    start_date, end_date = st.slider(
        "Select Date Range:",
        min_value=min_date, max_value=max_date,
        value=(min_date, max_date),
        format="YYYY-MM-DD"
    )

    st.markdown("#### Filter by Company:")
    def _toggle_all():
        for c in company_colors:
            st.session_state[f"cb_{c}"] = st.session_state["all_companies"]

    st.checkbox("All companies", key="all_companies", value=True, on_change=_toggle_all)
    selected_companies = []
    for company, color in company_colors.items():
        def _unset_master(c=company):
            if not st.session_state[f"cb_{c}"]:
                st.session_state["all_companies"] = False

        cb_col, label_col = st.columns([1, 16])
        checked = cb_col.checkbox("", key=f"cb_{company}", value=True, on_change=_unset_master)
        label_col.markdown(
            f"""
            <div style="display:inline-flex; align-items:center; line-height:1; position:relative; top:10px;">
              <span>{company}</span>
              <span style="
                width: 30px; height: 6px;
                background-color: {color};
                display: inline-block;
                margin-left: 8px;
                position: relative; top:1px;
              "></span>
            </div>
            """,
            unsafe_allow_html=True
        )
        if checked:
            selected_companies.append(company)

with col2:
    # Apply filters
    subset = df[
        (df['date'].dt.date >= start_date) &
        (df['date'].dt.date <= end_date) &
        (df['company'].isin(selected_companies))
    ]

    if subset.empty:
        st.warning("No transactions in the selected filters.")
        st.stop()

    st.subheader(f"Transactions from {start_date} to {end_date}")

    # Prepare map
    m = folium.Map(location=[20, 0], zoom_start=2,
                   tiles='CartoDB_Positron', world_copy_jump=True)
    folium.GeoJson(
        world.__geo_interface__,
        style_function=lambda f: {
            'fillColor': '#f2f2f2',
            'color': '#444',
            'weight': 0.5,
            'fillOpacity': 0.6
        }
    ).add_child(GeoJsonTooltip(fields=['name'], aliases=['Country:'], labels=True))\
     .add_to(m)

    # --- transaction dates for Prev/Next buttons ---
    transaction_dates = sorted(subset['date'].dt.date.unique())
    min_tx, max_tx = transaction_dates[0], transaction_dates[-1]

    # --- full calendar dates for Play button only ---
    calendar_dates = [
        start_date + timedelta(days=i)
        for i in range((end_date - start_date).days + 1)
    ]

    # Ensure play_date is valid
    if st.session_state.play_date not in calendar_dates:
        st.session_state.play_date = calendar_dates[0]

    # Time slider over full calendar
    st.session_state.play_date = st.slider(
        "Time Slider:",
        min_value=start_date,
        max_value=end_date,
        value=st.session_state.play_date,
        format="YYYY-MM-DD",
        key="slider"
    )

    # Prev/Next transaction callbacks (unchanged)
    def go_previous():
        idx = bisect.bisect_left(transaction_dates, st.session_state.play_date) - 1
        if idx >= 0:
            st.session_state.play_date = transaction_dates[idx]

    def go_next():
        idx = bisect.bisect_right(transaction_dates, st.session_state.play_date)
        if idx < len(transaction_dates):
            st.session_state.play_date = transaction_dates[idx]

    def toggle_play():
        st.session_state.playing = not st.session_state.playing

    # Render buttons
    b1, b2, b3 = st.columns([1,1,1])
    with b1:
        st.button("⏮️ Previous Transaction", on_click=go_previous)
    with b2:
        label = "⏸️ Pause" if st.session_state.playing else "▶️ Play"
        st.button(label, on_click=toggle_play)
    with b3:
        st.button("⏭️ Next Transaction", on_click=go_next)

    # Auto-advance when playing (uses calendar_dates)
    if st.session_state.playing:
        idx = calendar_dates.index(st.session_state.play_date)
        if idx + 1 < len(calendar_dates):
            st.session_state.play_date = calendar_dates[idx + 1]
            time.sleep(0.1)
            st.rerun()
        else:
            st.session_state.playing = False

    # Draw cumulative paths up to play_date
    play_date = st.session_state.play_date
    cumulative = subset[subset['date'].dt.date <= play_date]
    for _, r in cumulative.iterrows():
        AntPath(
            locations=[(r.origin_lat, r.origin_lon),
                       (r.destination_lat, r.destination_lon)],
            color=company_colors[r.company],
            weight=3,
            delay=1000,
            dash_array=[10, 20]
        ).add_to(m).add_child(folium.Tooltip(
            f"<b>{r.company}</b><br>"
            f"{r.origin} → {r.destination}<br>"
            f"Date: {r.date.date()}<br>"
            f"Amount: ${r.amount:,}",
            sticky=True
        ))

    # Display map
    st_folium(m, width=1000, height=600)
