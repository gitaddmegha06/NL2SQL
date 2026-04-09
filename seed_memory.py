from vanna_setup import agent
import logging

logging.basicConfig(level=logging.INFO)

# 15 Domain-specific Q&A Pairs required in Step 5
# Must be SELECT ONLY per instructions
qa_pairs = [
    # Patient queries
    {
        "question": "How many patients do we have?",
        "sql": "SELECT COUNT(*) AS total_patients FROM patients"
    },
    {
        "question": "Which city has the most patients?",
        "sql": "SELECT city, COUNT(*) AS patient_count FROM patients GROUP BY city ORDER BY patient_count DESC LIMIT 1"
    },
    {
        "question": "List all female patients from Mumbai.",
        "sql": "SELECT first_name, last_name, gender, city FROM patients WHERE gender = 'Female' AND city = 'Mumbai'"
    },
    {
        "question": "What is the breakdown of patients by gender?",
        "sql": "SELECT gender, COUNT(*) AS patient_count FROM patients GROUP BY gender"
    },
    
    # Doctor queries
    {
        "question": "List all doctors and their specializations.",
        "sql": "SELECT name, specialization, department FROM doctors"
    },
    {
        "question": "Which doctor has the most appointments?",
        "sql": "SELECT d.name, COUNT(a.id) AS appointment_count FROM doctors d JOIN appointments a ON d.id = a.doctor_id GROUP BY d.name ORDER BY appointment_count DESC LIMIT 1"
    },
    {
        "question": "How many doctors are in the Cardiology department?",
        "sql": "SELECT COUNT(*) AS total_doctors FROM doctors WHERE department = 'Cardiology Department'"
    },

    # Appointment queries
    {
        "question": "Show me appointments for last month.",
        "sql": "SELECT * FROM appointments WHERE appointment_date >= date('now', '-1 month') AND appointment_date < date('now', 'start of month')"
    },
    {
        "question": "How many cancelled appointments last quarter?",
        "sql": "SELECT COUNT(*) AS cancelled_count FROM appointments WHERE status = 'Cancelled' AND appointment_date >= date('now', '-3 months')"
    },
    {
        "question": "What percentage of appointments are no-shows?",
        "sql": "SELECT (CAST(SUM(CASE WHEN status = 'No-Show' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*)) * 100 AS no_show_percentage FROM appointments"
    },

    # Financial queries
    {
        "question": "What is the total revenue?",
        "sql": "SELECT SUM(total_amount) AS total_revenue FROM invoices"
    },
    {
        "question": "Show revenue by doctor.",
        "sql": "SELECT d.name, SUM(i.total_amount) AS total_revenue FROM invoices i JOIN appointments a ON a.patient_id = i.patient_id JOIN doctors d ON d.id = a.doctor_id GROUP BY d.name ORDER BY total_revenue DESC"
    },
    {
        "question": "Show unpaid invoices.",
        "sql": "SELECT i.id, p.first_name, p.last_name, i.total_amount, i.paid_amount, i.status FROM invoices i JOIN patients p ON i.patient_id = p.id WHERE i.status != 'Paid'"
    },
    
    # Time-based / Trend queries
    {
        "question": "Show patient registration trend by month.",
        "sql": "SELECT strftime('%Y-%m', registered_date) AS registration_month, COUNT(*) AS new_patients FROM patients GROUP BY registration_month ORDER BY registration_month ASC"
    },
    {
        "question": "Show the busiest day of the week for appointments.",
        "sql": "SELECT CASE strftime('%w', appointment_date) WHEN '0' THEN 'Sunday' WHEN '1' THEN 'Monday' WHEN '2' THEN 'Tuesday' WHEN '3' THEN 'Wednesday' WHEN '4' THEN 'Thursday' WHEN '5' THEN 'Friday' WHEN '6' THEN 'Saturday' END AS day_of_week, COUNT(*) AS appointment_count FROM appointments GROUP BY day_of_week ORDER BY appointment_count DESC LIMIT 1"
    }
]

def seed_agent_memory():
    logging.info(f"Seeding Agent Memory with {len(qa_pairs)} Q&A pairs...")
    
    # The 'demo' agent memory allows saving questions explicitly, often wrapped in the Tool Registry.
    # In Vanna 2.0 we trigger the SaveQuestionToolArgsTool or manually store them if using DemoAgentMemory.
    for pair in qa_pairs:
        # Saving directly into memory to ensure robust learning initialization
        agent.agent_memory.save_question_and_sql(
            question=pair["question"],
            sql=pair["sql"]
        )
        
    logging.info("Memory seeding complete.")

if __name__ == "__main__":
    seed_agent_memory()
