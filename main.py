# Core Pkgs
import streamlit as st 

# EDA Pkgs
import pandas as pd 
import numpy as np 

# Data Viz Pkg
import matplotlib.pyplot as plt 
import seaborn as sns 

def main():
    """Semi Automated EDA App with Streamlit """

    activities = ["EDA","Plots"]    
    choice = st.sidebar.selectbox("Select Activities",activities)

    if choice == 'EDA':
        st.subheader("Exploratory Data Analysis")

        data = st.file_uploader("Upload a Dataset", type=["csv", "txt"])
        if data is not None:
            # Handle both CSV and text files
            if data.name.endswith('.csv'):
                df = pd.read_csv(data)
            else:
                df = pd.read_table(data)
            
            st.dataframe(df.head())
            all_columns = df.columns.tolist()  # Moved outside checkboxes

            if st.checkbox("Show Shape"):
                st.write(df.shape)

            if st.checkbox("Show Columns"):
                st.write(all_columns)

            if st.checkbox("Summary"):
                st.write(df.describe())

            if st.checkbox("Show Selected Columns"):
                selected_columns = st.multiselect("Select Columns", all_columns)
                new_df = df[selected_columns]
                st.dataframe(new_df)

            if st.checkbox("Show Value Counts"):
                column_to_analyze = st.selectbox("Select Column for Value Counts", all_columns)
                st.write(df[column_to_analyze].value_counts())

            if st.checkbox("Correlation Plot(Matplotlib)"):
                fig, ax = plt.subplots()
                ax.matshow(df.corr())
                st.pyplot(fig)

            if st.checkbox("Correlation Plot(Seaborn)"):
                fig, ax = plt.subplots(figsize=(10,6))
                sns.heatmap(df.corr(), annot=True, ax=ax)
                st.pyplot(fig)

            if st.checkbox("Pie Plot"):
                column_to_plot = st.selectbox("Select Column", all_columns)
                fig, ax = plt.subplots()
                df[column_to_plot].value_counts().plot.pie(autopct="%1.1f%%", ax=ax)
                st.pyplot(fig)

    elif choice == 'Plots':
        st.subheader("Data Visualization")
        data = st.file_uploader("Upload a Dataset", type=["csv", "txt", "xlsx"])
        if data is not None:
            # Handle different file types
            if data.name.endswith('.csv'):
                df = pd.read_csv(data)
            elif data.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(data)
            else:
                df = pd.read_table(data)
                
            st.dataframe(df.head())
            all_columns_names = df.columns.tolist()

            if st.checkbox("Show Value Counts"):
                column_to_analyze = st.selectbox("Select Column", all_columns_names)
                fig, ax = plt.subplots()
                df[column_to_analyze].value_counts().plot(kind='bar', ax=ax)
                st.pyplot(fig)

            # Customizable Plot
            type_of_plot = st.selectbox("Select Type of Plot", ["area","bar","line","hist","box","kde"])
            selected_columns_names = st.multiselect("Select Columns To Plot", all_columns_names)

            if st.button("Generate Plot"):
                st.success(f"Generating {type_of_plot} plot for {selected_columns_names}")
                
                # Plot By Streamlit
                if type_of_plot in ['area', 'bar', 'line']:
                    cust_data = df[selected_columns_names]
                    if type_of_plot == 'area':
                        st.area_chart(cust_data)
                    elif type_of_plot == 'bar':
                        st.bar_chart(cust_data)
                    elif type_of_plot == 'line':
                        st.line_chart(cust_data)
                # Custom Matplotlib plots
                else:
                    fig, ax = plt.subplots()
                    df[selected_columns_names].plot(kind=type_of_plot, ax=ax)
                    st.pyplot(fig)

if __name__ == '__main__':
    main()