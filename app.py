import streamlit as st
import os, time, pathlib, json
import pandas as pd
from jinja2 import Environment, FileSystemLoader
import weasyprint

# INTERNAL LIBRARIES
from file_management import *
from state_machine import ResumeOptimizerStateMachine
from llm_agent import *

# GTK3 setup for WeasyPrint - cross-platform compatibility
import platform
if platform.system() == "Windows":
    # Only add GTK DLL directory on Windows if GTK is installed
    gtk_path = r"C:\Program Files\GTK3-Runtime Win64\bin"
    if os.path.exists(gtk_path):
        os.add_dll_directory(gtk_path)
    else:
        print("Warning: GTK3 not found at expected Windows path. Install GTK3 runtime for PDF generation.")
# On Linux/Mac, WeasyPrint should work with system libraries

# Initializing the state machine
if "machine" not in st.session_state:
    st.session_state.machine = ResumeOptimizerStateMachine()

st.title("ATS TAILORING SYSTEM (LLM)")

machine = st.session_state.machine

# Create output directory if not exists
output_path = pathlib.Path("output")
output_path.mkdir(exist_ok=True)
(output_path/".gitkeep").touch(exist_ok=True)

# --- GLOBAL VARIABLES USED FOR PDF GENERATION ----------

# Cross-platform path setup
output_dir = os.path.join(os.getcwd(), 'output')  # Local output directory
template_dir = os.path.join(os.getcwd(), 'templates')  # Local templates directory
# SETTING UP JINJA2 ENVIRONMENT
env = Environment(loader=FileSystemLoader(template_dir))
template = env.get_template('cv_template.html')                                  # Custom-made HTML template for the generated PDF Resume

# --- CONTROL STATE INITIALIZATIONS - SESSION CONTROL ---
if "user_checked" not in st.session_state:
    st.session_state.user_checked = False
if "user_exists" not in st.session_state:
    st.session_state.user_exists = False
if "user_confirmed" not in st.session_state:
    st.session_state.user_confirmed = False
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "job_id" not in st.session_state:
    st.session_state.job_id = None
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "linkedin_text" not in st.session_state:
    st.session_state.linkedin_text = ""
if "generated_cv" not in st.session_state:
    st.session_state.generated_cv = None

# It´s easier for this variable to managed inside app.py rather than llm_agent
starting_chat_prompt_model = """You are a helpful assistant specialized in career assistance.Your goal is to provide clear,
actionable, and practical advice to help users present themselves at their best,
land interviews, and succeed in their career transitions.
Take the following information as reference for the candidate and opportunity.

--- Candidate Resume ---
{resume_text}

--- Linkedin Export ---
{linkedin_text}

--- Job Description ---
{job_description}
"""

# --- GROQ API KEY PATH IN LOCAL ENVIRONMENT -------------------------------
# OpenAI API key will be read from environment variable OPENAI_API_KEY

# ------------------------------------
# APP FUNCTIONS TO IMPROVE READABILITY
# ------------------------------------
def display_jobs_with_selection(user_jobs):
    """Enhanced job selection UI with DataFrame display"""
    if not user_jobs:
        st.info("No existing jobs found for this user")
        return None

    jobs_df = pd.DataFrame(user_jobs,
                           columns=["ID", "Description", "Generated CV", "Created", "Last Modified"])

    st.dataframe(
        jobs_df,
        column_config={
            "ID": st.column_config.NumberColumn(width="small"),
            "Description": st.column_config.TextColumn(width="large"),
            "Generated CV": st.column_config.JsonColumn(),
            "Created": st.column_config.DatetimeColumn(),
            "Last Modified": st.column_config.DatetimeColumn()
        },
        hide_index=True,
        use_container_width=True
    )

    selected_id = st.selectbox(
        "Select job:",
        options=jobs_df["ID"].tolist(),
        format_func=lambda x: f"Job {x} - {jobs_df[jobs_df['ID'] == x]['Description'].iloc[0][:50]}..."
    )

    if st.button("Confirm Job Selection"):
        return selected_id
    return None

def show_loading_state():
    """Displays an animated loading screen"""
    progress_bar = st.progress(0)
    status_text = st.empty()

    for i in range(100):
        progress_bar.progress(i + 1)
        status_text.text(f"Generating optimized CV... {i + 1}%")
        time.sleep(0.03)  # Adjust speed as needed

    progress_bar.empty()
    status_text.empty()

# Step 1: Initialize user session and set st.session_state.user_name for use throughout the app
if machine.state == "start":

    user_name = st.text_input("Enter an user name for this configuration:")

    # Display existing users in a table
    st.subheader("Existing Users")
    all_users = get_all_users()

    if all_users:
        # Create DataFrame with user data
        users_df = pd.DataFrame(all_users, columns=["User ID", "Last Modified"])
        # Format the datetime
        users_df["Last Modified"] = pd.to_datetime(users_df["Last Modified"]).dt.strftime('%Y-%m-%d %H:%M')

        # Display a table of existing users
        st.dataframe(
            users_df,
            column_config={
                "User ID": st.column_config.TextColumn(width="medium"),
                "Last Modified": st.column_config.DatetimeColumn(width="medium")
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("No existing users found in the database")

    if user_name and not st.session_state.user_checked:
        # Check only once after typing
        user_exists = check_user_exists(user_name)
        st.session_state.user_exists = user_exists
        st.session_state.user_checked = True

    if user_name:
        user_exists_count = check_user_exists(user_name) or 0
        if user_exists_count > 0:
            st.warning(f"⚠️ User '{user_name}' already exists. Continuing with existing data?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Yes, continue"):
                    st.session_state.user_name = user_name
                    st.session_state.resume_text, st.session_state.linkedin_text = get_user_info(st.session_state.user_name) # HERE
                    st.session_state.user_confirmed = True
                    message = machine.next("select_user")
                    st.success(message)
                    st.rerun()  # Refresh to show next state

            with col2:
                if st.button("❌ No, input a new user"):
                    st.session_state.user_checked = False  # Reset check
                    st.session_state.user_exists = False
                    st.rerun()

        else:

            st.info(f"User '{user_name}' selected. Please, input your updated Resume PDF and Linkedin Export PDF to create your profile.")

            # Resume PDF
            resume_pdf = st.file_uploader("Resume PDF", type=["pdf"])

            # Linkedin PDF
            linkedin_pdf = st.file_uploader("Linkedin Default PDF Export", type=["pdf"])

            if resume_pdf and linkedin_pdf and user_name is not None:
                if st.button("📤 Upload & Continue", type="primary"):
                    try:
                        st.session_state.resume_text = extract_text_from_pdf(resume_pdf)
                        st.session_state.linkedin_text = extract_text_from_pdf(linkedin_pdf)
                        create_user(user_name, resume_pdf, linkedin_pdf)
                        st.session_state.user_name = user_name
                        message = machine.next("select_user")
                        st.success(message)
                        st.rerun()  # Refresh to show next state
                    except Exception as e:
                        st.error(f"Error creating user: {e}")

# Step 2: After user selection, select or create a new job
elif machine.state == "waiting_job_description":

    st.subheader("Select a Job Description for optimization:")

    # Get jobs for current user
    user_jobs = get_user_jobs(st.session_state.user_name)

    # Option 1: Create New Job (always shown)
    with st.expander("➕ Create New Job", expanded=True):
        new_job_text = st.text_area("Paste job description here:", height=200)
        if st.button("Save New Job"):
            if new_job_text.strip():
                try:
                    # Save the new job and automatically select it
                    job_id = create_new_job(st.session_state.user_name, new_job_text)
                    st.session_state.selected_job_text = new_job_text
                    st.session_state.job_id = job_id
                    message = machine.next("job_description_uploaded")
                    st.success(message)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error saving job: {e}")
            else:
                st.warning("Please enter a job description")

    # Option 2: Select Existing Jobs for the specific USER_ID/NAME
    st.subheader("Or select a previous Job configuration:")
    selected_id = display_jobs_with_selection(user_jobs)

    if selected_id:
        selected_job = next(job for job in user_jobs if job[0] == selected_id)
        st.session_state.job_id = selected_id
        st.session_state.selected_job_text = selected_job[1]
        message = machine.next("job_description_uploaded")
        st.success(f"Selected Job {selected_id}. {message}")
        st.rerun()

# Step 3: Process the input with the LLM to generate a tailored resume and render it as a PDF
elif machine.state == "processing_llm":
    st.subheader("Processing your data")
    with st.spinner("Initializing AI engine..."):
        time.sleep(1)  # Simulate setup

        show_loading_state()

        try:
            llm_agent = LLMAgent()
            result = llm_agent.generate_cv(
                st.session_state.user_name,
                st.session_state.resume_text,
                st.session_state.linkedin_text,
                st.session_state.selected_job_text
            )

            st.session_state.generated_cv = result
            save_dict_in_db(st.session_state.user_name, st.session_state.job_id, json.dumps(result))

            # PDF GENERATION PROCESS ----------------------------------------
            # RENDERING HTML
            rendered_html = template.render(st.session_state.generated_cv)
            # Saving HTML
            output_html_path = os.path.join(output_dir, 'output_cv.html')
            with open(output_html_path, 'w', encoding='utf-8') as f:
                f.write(rendered_html)
            # Generating the PDF - WEASY PRINT
            output_pdf_path = os.path.join(output_dir, f'Resume_{st.session_state.user_name}_{st.session_state.job_id}.PDF')
            weasyprint.HTML(string=rendered_html).write_pdf(output_pdf_path)

            message = machine.next("finished")
            st.success(message)
            st.rerun()

        except Exception as e:
            st.error(f"Generation failed: {str(e)}")
            machine.state = "waiting_job_description"  # Revert state

# Step 4: Final step – download resume and interact with the LLM-powered chatbot
elif machine.state == "job_exploration":

    # Create columns - most space empty, small space for button
    empty_col, button_col = st.columns([0.95, 0.05])

    with button_col:
        if st.button("↩️", help="Return to main menu"):
            st.session_state.clear()
            machine.next("menu")
            st.rerun()

    st.subheader("Download your Tailored Resume & Chat")

    # 1. Offer PDF download
    output_pdf_path = os.path.join(
        output_dir,
        f'Resume_{st.session_state.user_name}_{st.session_state.job_id}.PDF'
    )

    with open(output_pdf_path, "rb") as pdf_file:
        pdf_data = pdf_file.read()
    st.download_button(
        label="📄 Download Your Tailored Resume (PDF)",
        data=pdf_data,
        file_name=f"Tailored_Resume_{st.session_state.user_name}.pdf",
        mime="application/pdf"
    )

    st.divider()

    # 2. Chat with LLM based on the optimized resume
    st.subheader("💬 Chat with OpenAI Assistant")

    # Initialize or load chat history
    if "chat_history" not in st.session_state:
        # Try to load existing history from DB
        db_chat_history = get_chat_history(st.session_state.user_name, st.session_state.job_id)

        if db_chat_history:
            # Use existing history from DB
            st.session_state.chat_history = db_chat_history
        else:
            # Initialize new chat with default system prompt
            st.session_state.chat_history = [
                {
                    "role": "system",
                    "content": starting_chat_prompt_model.format(
                        resume_text=st.session_state.resume_text,
                        linkedin_text=st.session_state.linkedin_text,
                        job_description=st.session_state.selected_job_text
                    )
                }
            ]

    # Initialize the LLM Chat Agent
    llm_chat_agent = LLM_Chat()

    # Display chat messages (skip system prompt in display)
    for message in st.session_state.chat_history:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Handle chat input
    if prompt := st.chat_input("How can I help you today?"):
        # Constantly adding user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # Display user message while it finishes processing and rereun
        with st.chat_message("user"):
            st.markdown(prompt)

        assistant_response = llm_chat_agent.get_chat_answer(final_text_prompt=st.session_state.chat_history)

        # Constantly adding assistant response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

        # Save upd ated chat history to database as JSON
        save_chat_history(
            user_id=st.session_state.user_name,
            job_id=st.session_state.job_id,
            chat_history=json.dumps(st.session_state.chat_history)
        )

        # Rerun to refresh the display with updated history
        st.rerun()
