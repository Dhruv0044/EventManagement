from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

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

# Home page: list all events
@app.route('/')
def index():
    events = load_events()
    return render_template('index.html', events=events)

# Add a new event
@app.route('/add-event', methods=['POST'])
def add_event():
    events = load_events()

    name = request.form['name']
    date_str = request.form['date']
    description = request.form['description']
    category = request.form['category']
    budget = request.form['budget']

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return "Invalid date format!", 400

    # Create event
    new_event = {
        'id': len(events) + 1,
        'name': name,
        'date': date_str,
        'description': description,
        'category': category,
        'budget': budget,
        'rsvp': [],
        'attendance': [],
        'planners': [],
        'notifications': [],
        'team': []
    }

    events.append(new_event)
    save_events(events)

    return redirect(url_for('index'))

# View event details
@app.route('/event/<int:event_id>')
def view_event(event_id):
    events = load_events()
    event = next((event for event in events if event['id'] == event_id), None)
    if event:
        return render_template('event.html', event=event)
    return "Event not found", 404

# RSVP to an event
@app.route('/rsvp/<int:event_id>', methods=['POST'])
def rsvp_event(event_id):
    events = load_events()
    attendee = request.form['attendee']
    
    for event in events:
        if event['id'] == event_id:
            if attendee not in event['rsvp']:
                event['rsvp'].append(attendee)
                save_events(events)
                return jsonify({"status": "RSVP added successfully"}), 200
            else:
                return jsonify({"status": "You have already RSVP'd"}), 400
    return jsonify({"status": "Event not found"}), 404

# Mark attendance for an event
@app.route('/attendance/<int:event_id>', methods=['POST'])
def mark_attendance(event_id):
    events = load_events()
    attendee = request.form['attendee']
    
    for event in events:
        if event['id'] == event_id:
            if attendee in event['rsvp'] and attendee not in event['attendance']:
                event['attendance'].append(attendee)
                save_events(events)
                return jsonify({"status": "Attendance marked successfully"}), 200
            else:
                return jsonify({"status": "Attendee has not RSVP'd or already marked"}), 400
    return jsonify({"status": "Event not found"}), 404

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
