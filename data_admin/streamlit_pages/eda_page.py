import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def eda_page():
    _, col, _ = st.columns([0.25, 0.5, 0.25])
    with col:
        st.header("Exploratory Data Analysis")

        uploaded_file = st.file_uploader("Upload CSV file for DataFrame", type=["csv"])    
        if uploaded_file: 
            df = pd.read_csv(uploaded_file)
            st.write(df)
            st.write("## Comparison between Answered and Unanswered Questions")
            
            df_with_answers = df[df['Answer_Count'] > 0]
            df_without_answers = df[df['Answer_Count'] == 0]
            
            answered_count = df_with_answers.shape[0]
            unanswered_count = df_without_answers.shape[0]

            data = {'Type': ['Answered', 'Unanswered'],
                    'Count': [answered_count, unanswered_count]}
            df_comparison = pd.DataFrame(data)

            st.write("### Answered vs. Unanswered Questions")
            st.dataframe(df_comparison)  

            st.write("### Bar Chart: Answered vs. Unanswered Questions")
            fig, ax = plt.subplots(figsize=(8, 4))  
            sns.barplot(data=df_comparison, x='Type', y='Count', palette={'Answered': 'green', 'Unanswered': 'red'}, ax=ax)
            ax.set_ylabel('Count')
            ax.set_title('Answered vs. Unanswered Questions')
            st.pyplot(fig)

            st.write("## Most Active Authors (by Number of Questions Asked)")
            most_active_authors_questions = df['Question_Owner_Display_Name'].value_counts().nlargest(10)
            most_active_authors_questions = most_active_authors_questions.sort_values(ascending=False)  
            st.write("### Top 10 Most Active Question Authors")
            st.dataframe(most_active_authors_questions, width=500)  

            st.write("### Horizontal Bar Chart: Most Active Question Authors")
            fig2, ax2 = plt.subplots()
            most_active_authors_questions.plot(kind='barh', color='skyblue', ax=ax2)
            ax2.set_xlabel('Number of Questions')
            ax2.set_ylabel('Authors')
            ax2.set_title('Top 10 Most Active Question Authors')
            st.pyplot(fig2)

            st.write("## Most Active Authors (by Number of Answers given)")

            most_active_authors_answers = df['Answer_Owner_Display_Name'].value_counts().nlargest(10)
            most_active_authors_answers = most_active_authors_answers.sort_values(ascending=False)  
            st.write("#### Top 10 Most Active Answer Authors")
            st.dataframe(most_active_authors_answers, width=500)

            st.write("#### Horizontal Bar Chart: Most Active Answer Authors")
            fig3, ax3 = plt.subplots()
            most_active_authors_answers.plot(kind='barh', color='skyblue', ax=ax3)
            ax3.set_xlabel('Number of Answers')
            ax3.set_ylabel('Authors')
            ax3.set_title('Top 10 Most Active Answer Authors')
            st.pyplot(fig3)


            st.write("## Accepted vs All Answers for Authors")
            author_answer_counts = df.groupby(['Answer_Owner_Display_Name', 'Is_Accepted'])['Question_ID'].count().unstack().fillna(0)
            author_answer_counts['Total_Answers'] = author_answer_counts.sum(axis=1)
            author_answer_counts['Acceptance_Rate'] = author_answer_counts[True] / author_answer_counts['Total_Answers']
            author_answer_counts = author_answer_counts.sort_values(by='Total_Answers', ascending=False).head(10)
            
            st.write("### Top 10 Authors by Answer Count, Accepted Answers, and Acceptance Rate")
            st.dataframe(author_answer_counts.style.format({'Acceptance_Rate': '{:.2%}'}))

            plt.figure(figsize=(10, 6))
            author_answer_counts['Acceptance_Rate'].plot(kind='bar', color='skyblue')
            plt.xlabel('Authors')
            plt.ylabel('Acceptance Rate')
            plt.title('Top 10 Authors by Acceptance Rate')
            plt.xticks(rotation=45)
            st.pyplot(plt)
