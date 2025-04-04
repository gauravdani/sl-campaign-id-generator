# Campaign ID Generator
# A Streamlit application to generate and track marketing campaign IDs based on targeting criteria
# Dependencies: streamlit, pandas

import streamlit as st
import pandas as pd
import hashlib
import uuid
import datetime
import json
from typing import Dict, List, Any

def generate_campaign_id(campaign_data: Dict[str, Any]) -> str:
    """Generate a unique campaign ID based on targeting criteria and timestamp."""
    # Create a base string with timestamp for uniqueness
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    
    # Create a shortened hash of the campaign data
    data_string = json.dumps(campaign_data, sort_keys=True)
    hash_object = hashlib.md5(data_string.encode())
    data_hash = hash_object.hexdigest()[:8]
    
    # Combine elements to create campaign ID
    platform_code = campaign_data.get("platform", "ALL")[:3].upper()
    objective_code = campaign_data.get("campaign_objective", "GEN")[:3].upper()
    
    # Create the final campaign ID
    campaign_id = f"{platform_code}-{objective_code}-{timestamp}-{data_hash}"
    
    return campaign_id

def save_campaign_data(campaign_data: Dict[str, Any], campaign_id: str) -> None:
    """Save campaign data to a CSV file."""
    # Create a record to save
    record = {
        "campaign_id": campaign_id,
        "creation_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "created_by": campaign_data.get("created_by", "Unknown"),
        "platform": campaign_data.get("platform", ""),
        "campaign_objective": campaign_data.get("campaign_objective", ""),
        "targeting_criteria": json.dumps(campaign_data.get("targeting", {})),
        "budget": campaign_data.get("budget", 0),
        "start_date": campaign_data.get("start_date", ""),
        "end_date": campaign_data.get("end_date", "")
    }
    
    # Load existing data if file exists
    try:
        df = pd.read_csv("campaign_records.csv")
        df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    except:
        df = pd.DataFrame([record])
    
    # Save updated dataframe
    df.to_csv("campaign_records.csv", index=False)

def main():
    """Main application function"""
    st.set_page_config(
        page_title="Campaign ID Generator",
        page_icon="🎯",
        layout="wide"
    )
    
    st.title("🎯 Marketing Campaign ID Generator")
    st.write("Complete the form below to generate a unique campaign ID for your marketing campaign.")
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Campaign Setup", "Audience Targeting", "Generated ID"])
    
    campaign_data = {}
    
    with tab1:
        st.header("Campaign Setup")
        
        col1, col2 = st.columns(2)
        
        with col1:
            campaign_data["created_by"] = st.text_input("Marketing Manager", placeholder="Your Name")
            campaign_data["platform"] = st.selectbox(
                "Platform", 
                ["Facebook", "Instagram", "Google Ads", "TikTok", "LinkedIn", "Twitter", "YouTube", "Other"]
            )
            campaign_data["campaign_objective"] = st.selectbox(
                "Campaign Objective",
                ["Brand Awareness", "Reach", "Traffic", "Engagement", "App Installs", 
                 "Video Views", "Lead Generation", "Messages", "Conversions", "Catalog Sales"]
            )
        
        with col2:
            campaign_data["start_date"] = st.date_input("Start Date").strftime("%Y-%m-%d")
            campaign_data["end_date"] = st.date_input("End Date").strftime("%Y-%m-%d")
            campaign_data["budget"] = st.number_input("Budget ($)", min_value=0.0, step=100.0)
            
        st.divider()
        st.write("Once you've completed the campaign setup, navigate to the Audience Targeting tab.")
    
    with tab2:
        st.header("Audience Targeting")
        
        # Initialize targeting dict
        targeting = {}
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Demographics")
            
            # Age Range
            age_min = st.slider("Minimum Age", 13, 65, 18)
            age_max = st.slider("Maximum Age", age_min, 65, 65)
            targeting["age_range"] = f"{age_min}-{age_max}"
            
            # Gender
            targeting["gender"] = st.multiselect(
                "Gender",
                ["Male", "Female", "All"],
                default=["All"]
            )
            
            # Languages
            targeting["languages"] = st.multiselect(
                "Languages",
                ["English", "Spanish", "French", "German", "Chinese", "Japanese", "Other"],
                default=["English"]
            )
            
            # Location targeting
            st.subheader("Location")
            targeting["location_type"] = st.radio(
                "Location Type",
                ["Countries", "Regions", "Cities", "Radius", "Custom"]
            )
            
            targeting["locations"] = st.text_area(
                "Target Locations (comma separated)",
                placeholder="Example: USA, Canada, UK"
            )
        
        with col2:
            st.subheader("Interests & Behaviors")
            
            # Interests
            targeting["interests"] = st.multiselect(
                "Interests",
                ["Technology", "Fashion", "Sports", "Gaming", "Travel", "Food & Drink", 
                 "Entertainment", "Business", "Fitness", "Education", "Family", "Music"]
            )
            
            # Behaviors
            targeting["behaviors"] = st.multiselect(
                "Behaviors",
                ["Frequent Travelers", "Online Shoppers", "Mobile Device Users", 
                 "International", "Early Technology Adopters", "Small Business Owners"]
            )
            
            # Device targeting
            st.subheader("Devices")
            targeting["devices"] = st.multiselect(
                "Target Devices",
                ["Desktop", "Mobile", "Tablet", "All"],
                default=["All"]
            )
            
            # Custom audience
            st.subheader("Custom Audience")
            targeting["custom_audience"] = st.text_area(
                "Custom Audience IDs (if applicable)",
                placeholder="Example: audience_id_12345"
            )
        
        # Additional targeting options
        st.subheader("Additional Targeting")
        targeting["additional"] = st.text_area(
            "Additional Targeting Criteria",
            placeholder="Any additional targeting information"
        )
        
        # Store targeting data in campaign_data
        campaign_data["targeting"] = targeting
    
    with tab3:
        st.header("Generated Campaign ID")
        
        if st.button("Generate Campaign ID", type="primary"):
            if not campaign_data.get("created_by") or not campaign_data.get("platform"):
                st.error("Please fill in at least the Marketing Manager name and Platform in the Campaign Setup tab.")
            else:
                # Generate ID
                campaign_id = generate_campaign_id(campaign_data)
                
                # Save data
                save_campaign_data(campaign_data, campaign_id)
                
                # Display the campaign ID
                st.success("Campaign ID generated successfully!")
                st.header(f"📋 {campaign_id}")
                st.button("Copy to Clipboard", key="copy")
                
                # Display targeting summary
                st.subheader("Campaign Summary")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Platform:** {campaign_data['platform']}")
                    st.write(f"**Objective:** {campaign_data['campaign_objective']}")
                    st.write(f"**Created By:** {campaign_data['created_by']}")
                    st.write(f"**Campaign Period:** {campaign_data['start_date']} to {campaign_data['end_date']}")
                
                with col2:
                    st.write(f"**Target Age:** {campaign_data['targeting']['age_range']}")
                    st.write(f"**Target Gender:** {', '.join(campaign_data['targeting']['gender'])}")
                    st.write(f"**Target Locations:** {campaign_data['targeting']['locations']}")
                
                # Export options
                st.divider()
                st.subheader("Export Options")
                
                export_col1, export_col2 = st.columns(2)
                
                with export_col1:
                    st.download_button(
                        label="Download Campaign Data (JSON)",
                        data=json.dumps(campaign_data, indent=2),
                        file_name=f"{campaign_id}_data.json",
                        mime="application/json"
                    )
                
                with export_col2:
                    st.button("Email Campaign Details")
        else:
            st.info("Complete the Campaign Setup and Audience Targeting tabs, then click 'Generate Campaign ID'.")
    
    # Display campaign history in sidebar
    st.sidebar.title("Campaign History")
    try:
        history_df = pd.read_csv("campaign_records.csv")
        st.sidebar.dataframe(
            history_df[["campaign_id", "creation_date", "platform", "campaign_objective"]],
            use_container_width=True
        )
        
        # Search functionality
        st.sidebar.divider()
        st.sidebar.subheader("Search Campaigns")
        search_term = st.sidebar.text_input("Search by ID or platform")
        
        if search_term:
            filtered_df = history_df[
                history_df["campaign_id"].str.contains(search_term, case=False) | 
                history_df["platform"].str.contains(search_term, case=False)
            ]
            st.sidebar.dataframe(filtered_df, use_container_width=True)
    except:
        st.sidebar.write("No campaign history available yet.")

if __name__ == "__main__":
    main()