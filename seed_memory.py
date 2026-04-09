import asyncio
import logging
from vanna_setup import agent
from vanna.core.tool import ToolContext
from vanna.core.user import User

# Configure logging
logging.basicConfig(level=logging.INFO)

# qa pairs
qa_pairs = [
    {
        "question": "How many total patients are registered in the clinic?",
        "sql": "SELECT COUNT(*) FROM patients"
    },
    {
        "question": "Who is the doctor with the most appointments?",
        "sql": "SELECT d.name, COUNT(a.id) as count FROM doctors d JOIN appointments a ON d.id = a.doctor_id GROUP BY d.id ORDER BY count DESC LIMIT 1"
    },
    {
        "question": "What is the total revenue generated from all paid invoices?",
        "sql": "SELECT SUM(paid_amount) FROM invoices WHERE status = 'Paid'"
    },
    {
        "question": "List all doctors in the 'Cardiology' department.",
        "sql": "SELECT name FROM doctors WHERE department = 'Cardiology Department'"
    },
    {
        "question": "Which city has the highest number of patients?",
        "sql": "SELECT city, COUNT(*) as count FROM patients GROUP BY city ORDER BY count DESC LIMIT 1"
    },
    {
        "question": "Show the total number of appointments scheduled for each month.",
        "sql": "SELECT strftime('%Y-%m', appointment_date) as month, COUNT(*) FROM appointments GROUP BY month"
    },
    {
        "question": "What is the average cost of all treatments provided?",
        "sql": "SELECT AVG(cost) FROM treatments"
    },
    {
        "question": "How many female patients are registered from Mumbai?",
        "sql": "SELECT COUNT(*) FROM patients WHERE gender = 'Female' AND city = 'Mumbai'"
    },
    {
        "question": "List the names of patients who have cancelled their appointments.",
        "sql": "SELECT DISTINCT p.first_name, p.last_name FROM patients p JOIN appointments a ON p.id = a.patient_id WHERE a.status = 'Cancelled'"
    },
    {
        "question": "Which doctor specializes in 'Pediatrics'?",
        "sql": "SELECT name FROM doctors WHERE specialization = 'Pediatrics'"
    },
    {
        "question": "What is the total amount of unpaid invoices?",
        "sql": "SELECT SUM(total_amount - paid_amount) FROM invoices WHERE status != 'Paid'"
    },
    {
        "question": "Show the busiest day of the week for appointments.",
        "sql": "SELECT strftime('%w', appointment_date) as day, COUNT(*) as count FROM appointments GROUP BY day ORDER BY count DESC LIMIT 1"
    },
    {
        "question": "List treatments that take longer than 60 minutes.",
        "sql": "SELECT treatment_name FROM treatments WHERE duration_minutes > 60"
    },
    {
        "question": "How many appointments did 'Dr. Aarav Sharma' handle?",
        "sql": "SELECT COUNT(*) FROM appointments a JOIN doctors d ON a.doctor_id = d.id WHERE d.name LIKE '%Aarav Sharma%'"
    },
    {
        "question": "What is the breakdown of patients by gender?",
        "sql": "SELECT gender, COUNT(*) FROM patients GROUP BY gender"
    }
]

async def seed_agent_memory():
    logging.info(f"Seeding Agent Memory with {len(qa_pairs)} Q&A pairs...")
    
    context = ToolContext(
        user=User(id="admin", roles=["admin"]),
        conversation_id="seed-process",
        request_id="seed-process",
        agent_memory=agent.agent_memory
    )
    
    for pair in qa_pairs:
        await agent.agent_memory.save_tool_usage(
            question=pair["question"],
            tool_name="run_sql",
            args={"sql": pair["sql"]},
            context=context,
            success=True
        )
        logging.info(f"Seeded: {pair['question']}")
        
    logging.info("Memory seeding complete.")

if __name__ == "__main__":
    asyncio.run(seed_agent_memory())
