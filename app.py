import streamlit as st
import pandas as pd
import time
import os

# Create a folder called data in the main project folder
DATA_FOLDER = "data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# Define CSV file paths for each part of the usability testing
CONSENT_CSV = os.path.join(DATA_FOLDER, "consent_data.csv")
DEMOGRAPHIC_CSV = os.path.join(DATA_FOLDER, "demographic_data.csv")
TASK_CSV = os.path.join(DATA_FOLDER, "task_data.csv")
EXIT_CSV = os.path.join(DATA_FOLDER, "exit_data.csv")

diff_dict = {
    "Very Difficult": 1,
    "Difficult": 2,
    "Neutral": 3,
    "Easy": 4,
    "Very Easy": 5
}

satisfied_dict = {
    "Not Satisfied": 1,
    "Barely Satisfied": 2,
    "Neutral": 3,
    "Satisfied": 4,
    "Very Satisfied": 5
}

TASKS = [
    "As a fishermen, upload an entry containing details about a recent catch and view it in the history page",
    "As a researcher, please view the statistics and talk about what you see",
    "As a researcher, look up the fish you caught and find its wikipedia page through the species page"
]

def save_to_csv(data_dict, csv_file):
    # Convert dict to DataFrame with a single row
    df_new = pd.DataFrame([data_dict])
    if not os.path.isfile(csv_file):
        # If CSV doesn't exist, write with headers
        df_new.to_csv(csv_file, mode='w', header=True, index=False)
    else:
        # Else, we need to append without writing the header!
        df_new.to_csv(csv_file, mode='a', header=False, index=False)


def load_from_csv(csv_file):
    if os.path.isfile(csv_file):
        return pd.read_csv(csv_file)
    else:
        return pd.DataFrame()


def main():
    st.title("Usability Testing Tool")

    home, consent, demographics, tasks, exit, report = st.tabs(["Home", "Consent", "Demographics", "Task", "Exit Questionnaire", "Report"])

    with home:
        st.header("Introduction")
        st.write("""
        Welcome to the Usability Testing Tool for HCI.

        In this app, you will:
        1. Provide consent for data collection.
        2. Fill out a short demographic questionnaire.
        3. Perform a specific task (or tasks).
        4. Answer an exit questionnaire about your experience.
        5. View a summary report (for demonstration purposes).
        """)


    with consent:
        st.header("Consent Form")

        # TODO: Create your consent form and a variable called consent_given

        st.markdown("By signing this consent form, you agree that the data you inputted is anonymous and will only be used for demographic and research purposes")

        consent_given = st.checkbox("I agree to the consent terms")

        if st.button("Submit Consent"):
            if not consent_given:
                st.warning("You must agree to the consent terms before proceeding.")
            else:
                # Save the consent acceptance time
                try:
                    data_dict = {
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "consent_given": consent_given
                    }
                    save_to_csv(data_dict, CONSENT_CSV)
                except Exception:
                    st.error("Failed to submit consent form. Please try again")
                else:
                    st.success("Successfully submitted consent form")

                

    with demographics:
        st.header("Demographic Questionnaire")

        with st.form("demographic_form"):
            #TODO: Create the demographic form
            name = st.text_input(label="What is your name?")
            age = st.text_input(label="How old are you?")
            occupation = st.radio("What is your title or occupation?", options=["Fisher", "Researcher", "Student", "Other"])
            other_occupation = st.text_input(label="If other, type in your occupation")
            familiarity = st.radio("Are you aware of the subject of this research page?", ("Yes", "No"))
            submitted = st.form_submit_button("Submit Demographics")
            if submitted:
                if occupation == "Other":
                    occupation = other_occupation
                try:
                    if name == "" or age == "" or occupation == "": 
                        raise Exception("Incomplete form. Please fill in every answer before submitting")
                    data_dict = {
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "name": name,
                        "age": age,
                        "occupation": occupation,
                        "familiarity": familiarity
                    }
                    save_to_csv(data_dict, DEMOGRAPHIC_CSV)
                except Exception as e:
                    st.error("Failed to upload form: " + str(e))
                else:
                    st.success("Successfully uploaded form")

    with tasks:
        st.header("Task Page")

        st.write("Please select a task and record your experience completing it.")

        # For this template, we assume there's only one task, in project 3, we will have to include the actual tasks
        selected_task = st.selectbox("Select Task", TASKS)
        st.write("Task Description: Perform the following task in our app.")

        # Track success, completion time, etc.
        start_button = st.button("Start Task Timer")
        if start_button:
            st.session_state["start_time"] = time.time()
            st.info("Timer started. Please click on the stop button to record it")

        stop_button = st.button("Stop Task Timer")
        if stop_button and "start_time" in st.session_state:
            try:
                duration = time.time() - st.session_state["start_time"]
                st.session_state["task_duration"] = duration
            except Exception:
                st.error("Failed to record task. Please try again")
            else:
                st.success("Successfully recorded the time")

        success = st.radio("Was the task completed successfully?", ["Yes", "No", "Partial"])
        notes = st.text_area("Observer Notes")

        if st.button("Save Task Results"):
            try:
                duration_val = st.session_state.get("task_duration", None)
                
                if not duration_val:
                    raise Exception("Please record the time before submitting.")

                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "task_name": selected_task,
                    "success": success,
                    "duration_seconds": duration_val if duration_val else "",
                    "notes": notes
                }
                save_to_csv(data_dict, TASK_CSV)
                
                # Reset any stored time in session_state if you'd like
                if "start_time" in st.session_state:
                    del st.session_state["start_time"]
                if "task_duration" in st.session_state:
                    del st.session_state["task_duration"]
            except Exception as e:
                st.error(f'Failed to record task: {e}')
            else:
                st.success("Successfully completed and recorded the task")

    
    with exit:
        st.header("Exit Questionnaire")

        with st.form("exit_form"):
            # TODO: likert scale or other way to have an exit questionnaire

            DEFAULT_OPTIONS = ["Very Difficult", "Difficult", "Neutral", "Easy", "Very Easy"]

            satisfaction = st.select_slider("How satsified are you with the app?", 
                                            options= ["Not Satisfied", "Barely Satisfied", "Neutral", "Satisfied", "Very Satisfied"],)
            difficulty = st.select_slider("How difficult did you find using the app?", 
                                   options=DEFAULT_OPTIONS,)
            usage = st.select_slider("How useful do you think this app is to you?", options=["Very Useful", "Useful", "Sometimes Useful", "Rarely Useful", "Useless"])
            image_difficulty = st.select_slider("How hard was it to upload files?", options=DEFAULT_OPTIONS)

            bug_rating = st.radio("Did you encounter any bugs, errors, or malfunctions with the program?", options=["Yes", "No"])
            bug_feedback = st.text_area("If yes, explain")
            open_feedback = st.text_area("Any additional feedback?")

            submitted_exit = st.form_submit_button("Submit Exit Questionnaire")
            if submitted_exit:
                try:
                    data_dict = {
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "satisfaction": satisfied_dict[satisfaction],
                        "difficulty": diff_dict[difficulty],
                        "usage": usage,
                        "image_diffculty": image_difficulty,
                        "bug_rating": bug_rating,
                        "bug_feedback": bug_feedback,
                        "open_feedback": open_feedback
                    }
                    save_to_csv(data_dict, EXIT_CSV)
                except Exception:
                    st.error("Failed to submit questionnaire data. Please try again.")
                else:
                    st.success("Exit questionnaire data saved.")

    with report:
        st.header("Usability Report - Aggregated Results")

        st.write("**Consent Data**")
        consent_df = load_from_csv(CONSENT_CSV)
        if not consent_df.empty:
            st.dataframe(consent_df)
        else:
            st.info("No consent data available yet.")

        st.write("**Demographic Data**")
        demographic_df = load_from_csv(DEMOGRAPHIC_CSV)
        if not demographic_df.empty:
            st.dataframe(demographic_df)
        else:
            st.info("No demographic data available yet.")

        st.write("**Task Performance Data**")
        task_df = load_from_csv(TASK_CSV)
        if not task_df.empty:
            st.dataframe(task_df)
        else:
            st.info("No task data available yet.")

        st.write("**Exit Questionnaire Data**")
        exit_df = load_from_csv(EXIT_CSV)
        if not exit_df.empty:
            st.dataframe(exit_df)
        else:
            st.info("No exit questionnaire data available yet.")

        # Example of aggregated stats (for demonstration only)
        if not exit_df.empty:
            st.subheader("Exit Questionnaire Averages")
            avg_satisfaction = exit_df["satisfaction"].mean()
            avg_difficulty = exit_df["difficulty"].mean()
            st.write(f"**Average Satisfaction**: {avg_satisfaction:.2f}")
            st.write(f"**Average Difficulty**: {avg_difficulty:.2f}")


if __name__ == "__main__":
    main()