import streamlit as st
import pandas as pd
import plotly.express as px

def calculate_metrics(channels, campaigns, variations):
    # Calculate basic metrics
    total_creative_variations = campaigns * variations
    # Define formats per channel
    formats_per_channel = {
        'Display': 5,
        'Meta': 4, 
        'TikTok': 3,
        'YouTube': 3,
        'Digital OOH': 3
    }
    
    # Calculate total formats by summing formats for selected channels
    total_formats_per_campaign = sum(formats_per_channel[channel] for channel in channels)
    total_creative_formats = total_creative_variations * total_formats_per_campaign
    
    # Calculate hours
    hours_per_variation = 24  # Based on spreadsheet assumption
    hours_per_format = 4      # Based on spreadsheet assumption
    
    total_hours_variations = total_creative_variations * hours_per_variation
    total_hours_formats = total_creative_formats * hours_per_format
    total_hours = total_hours_variations + total_hours_formats
    
    # Calculate costs
    hourly_rate = 50  # Based on spreadsheet assumption
    total_cost = total_hours * hourly_rate
    
    # Calculate savings
    hours_with_solution = total_creative_formats * (2/60)  # 2 minutes per asset
    hours_saved = total_hours - hours_with_solution
    platform_costs = 7500  # Based on spreadsheet assumption
    money_saved = total_cost - platform_costs
    
    # Calculate time per asset
    current_minutes_per_asset = (total_hours * 60) / total_creative_formats
    new_minutes_per_asset = (4 * 60) / total_creative_formats  # 4 hours to create assets on Cuttable, converted to minutes per asset
    
    return {
        "total_variations": total_creative_variations,
        "total_formats": total_creative_formats,
        "total_hours": total_hours,
        "total_cost": total_cost,
        "hours_saved": hours_saved,
        "money_saved": money_saved,
        "current_minutes_per_asset": current_minutes_per_asset,
        "new_minutes_per_asset": new_minutes_per_asset,
        "hours_with_solution": hours_with_solution
    }

def main():
    st.title("Cuttable ROI Calculator")
    st.write("Calculate potential time and cost savings with Cuttable.")
    
    # Input section
    # Main content area explanations
    with st.sidebar:
        st.markdown("""
            # Using This Calculator
            
            This calculator is designed to help you estimate the potential time and cost savings with Cuttable.\n
            It figures out how many assets you're creating per month for your marketing, the time and cost of creating them currently, and the time and cost of using Cuttable.
                    
            A few definitions:
            * A creative variation is an asset with large changes in messaging, design, or imagery. Think new headlines, different layouts, or different imagery.
            * A creative format is a resizing of an asset for a platform. There are no changes in layout otherwise.
        """)
    
    # Sidebar inputs
    with st.sidebar:
        st.markdown("# Input Parameters")
        
        # Channel selection
        st.write("Select advertising channels:")
        col1, col2 = st.columns(2)
        
        with col1:
            meta = st.checkbox("Meta")
            tiktok = st.checkbox("TikTok")
            display = st.checkbox("Display")
        
        with col2:
            youtube = st.checkbox("YouTube") 
            dooh = st.checkbox("Digital OOH")
        
        channels = []
        if meta: channels.append("Meta")
        if tiktok: channels.append("TikTok")
        if youtube: channels.append("YouTube")
        if dooh: channels.append("Digital OOH")
        if display: channels.append("Display")
        
        # Campaign and variation inputs
        st.write("Campaign Details:")
        campaigns = st.number_input("Number of campaigns running simultaneously", 
                                  min_value=1, 
                                  value=2,
                                  help="Enter the number of campaigns you plan to run at the same time")
        
        st.write("")  # Add some vertical spacing
        
        variations = st.number_input("Number of ad variations per campaign",
                                   min_value=1, 
                                   value=3,
                                   help="Enter how many different versions of each ad you need")
    
    if len(channels) > 0:
        # Calculate metrics
        metrics = calculate_metrics(channels, campaigns, variations)
        
        # Results section
        st.markdown("---")  # Add a visual separator
        st.markdown("### Total Assets Needed")


        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Creative Variations", metrics["total_variations"])
        with col2:
            st.metric("Total Creative Formats", metrics["total_formats"])

        st.markdown("---")  # Add a visual separator
        st.markdown("### Estimated Hours and Costs Using External / In-House Agency")
        
        col1, col2 = st.columns(2)
            
        col1, col2 = st.columns(2)    
        with col1:
            st.metric("Total Content Development Hours", f"{metrics['total_hours']:,.0f}")
        with col2:
            st.metric("Total Cost", f"${metrics['total_cost']:,.2f}")
            
        st.markdown("### Estimated Hours and Costs Using Cuttable")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Content Development Hours with Cuttable", f"{metrics['hours_with_solution']:,.0f}")
        with col2:
            st.metric("Total Costs with Cuttable", "$7,500")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Hours Saved", f"{metrics['hours_saved']:,.0f}")
        with col2:
            st.metric("Total Costs Saved", f"${metrics['money_saved']:,.2f}")
        
        st.markdown("### Time Saved With Cuttable")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Current Minutes per Asset", f"{metrics['current_minutes_per_asset']:.1f}")
        with col2:
            st.metric("New Minutes per Asset with Cuttable", f"{metrics['new_minutes_per_asset']:.1f}", delta=f"{(metrics['current_minutes_per_asset'] -metrics['new_minutes_per_asset'])/metrics['current_minutes_per_asset']*100:.0f}%")
            
        # Savings visualization
        time_comparison = pd.DataFrame({
            'Process': ['Current process', 'With Cuttable'],
            'Minutes per Asset': [metrics['current_minutes_per_asset'], metrics['new_minutes_per_asset']]
        })
        fig = px.bar(time_comparison, x='Minutes per Asset', y="Process", orientation='h')
        st.write(fig)
        
    else:
        st.warning("Please select at least one channel to see calculations.")

if __name__ == "__main__":
    main() 