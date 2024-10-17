import streamlit as st
import json
import os
from datetime import datetime

# File to store events
EVENT_FILE = "events.json"

# Load events from JSON file
def load_events():
    if os.path.exists(EVENT_FILE):
        with open(EVENT_FILE, 'r') as file:
            return json.load(file)
    return []

# Save events to JSON file
def save_events(events):
    with open(EVENT_FILE, 'w') as file:
        json.dump(events, file, indent=4, default=str)

# Main App Interface
def main():
    st.title("Event Management System")

    # Load existing events
    events = load_events()

    # Add Event Section
    st.header("Add New Event")
    with st.form("event_form", clear_on_submit=True):
        event_name = st.text_input("Event Name")
        event_date = st.date_input("Event Date", datetime.today())
        event_description = st.text_area("Event Description")
        event_category = st.selectbox("Event Category", ["Business", "Personal", "Conference", "Wedding"])
        event_budget = st.number_input("Event Budget", min_value=0)
        
        submitted = st.form_submit_button("Add Event")
        if submitted:
            new_event = {
                'id': len(events) + 1,
                'name': event_name,
                'date': event_date.strftime('%Y-%m-%d'),
                'description': event_description,
                'category': event_category,
                'budget': event_budget,
                'rsvp': [],
                'attendance': [],
                'planners': [],
                'notifications': [],
                'team': []
            }
            events.append(new_event)
            save_events(events)
            st.success(f"Event '{event_name}' added successfully!")

    # View Events Section
    st.header("Upcoming Events")
    for event in events:
        with st.expander(f"{event['name']} ({event['date']})"):
            st.write(f"**Category:** {event['category']}")
            st.write(f"**Description:** {event['description']}")
            st.write(f"**Budget:** ${event['budget']}")
            st.write(f"**RSVP:** {len(event['rsvp'])} attendees")
            st.write(f"**Attendance:** {len(event['attendance'])} attended")
            
            # RSVP Section
            attendee_name = st.text_input(f"Enter your name to RSVP for {event['name']}", key=f"rsvp_{event['id']}")
            if st.button(f"RSVP for {event['name']}", key=f"rsvp_btn_{event['id']}"):
                if attendee_name and attendee_name not in event['rsvp']:
                    event['rsvp'].append(attendee_name)
                    save_events(events)
                    st.success(f"{attendee_name} has successfully RSVP'd!")
                elif attendee_name in event['rsvp']:
                    st.warning(f"{attendee_name} has already RSVP'd!")
                else:
                    st.error("Please enter a valid name.")

            # Mark Attendance
            attendance_name = st.text_input(f"Enter attendee name to mark attendance for {event['name']}", key=f"att_{event['id']}")
            if st.button(f"Mark Attendance for {event['name']}", key=f"att_btn_{event['id']}"):
                if attendance_name in event['rsvp'] and attendance_name not in event['attendance']:
                    event['attendance'].append(attendance_name)
                    save_events(events)
                    st.success(f"{attendance_name} has been marked as attended!")
                elif attendance_name in event['attendance']:
                    st.warning(f"{attendance_name} has already been marked as attended!")
                else:
                    st.error(f"{attendance_name} has not RSVP'd yet!")

if __name__ == "__main__":
    main()
