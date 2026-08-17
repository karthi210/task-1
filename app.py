from flask import Flask, render_template, request, redirect, url_for
import uuid

app = Flask(__name__)

# Sample event data with image URLs from the internet (Picsum)
events = [
    {
        'id': 1,
        'title': 'Rock Concert 2026',
        'description': 'An electrifying night with top rock bands. Get ready to rock!',
        'image': 'https://picsum.photos/seed/rock/400/300',
        'available_tickets': 100
    },
    {
        'id': 2,
        'title': 'Tech Conference',
        'description': 'Learn about the latest in AI, cloud, and DevOps from industry experts.',
        'image': 'https://picsum.photos/seed/tech/400/300',
        'available_tickets': 50
    },
    {
        'id': 3,
        'title': 'Movie Premiere: The Last Journey',
        'description': 'Exclusive premiere of the most anticipated sci-fi movie of the year.',
        'image': 'https://picsum.photos/seed/movie/400/300',
        'available_tickets': 80
    }
]

# In-memory booking storage (list of dicts)
bookings = []

@app.route('/')
def index():
    return render_template('index.html', events=events)

@app.route('/event/<int:event_id>')
def event_detail(event_id):
    event = next((e for e in events if e['id'] == event_id), None)
    if not event:
        return "Event not found", 404
    return render_template('event.html', event=event)

@app.route('/book/<int:event_id>', methods=['GET', 'POST'])
def book_tickets(event_id):
    event = next((e for e in events if e['id'] == event_id), None)
    if not event:
        return "Event not found", 404

    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        quantity = int(request.form.get('quantity', 1))

        # Basic validation
        if not name or not email or quantity < 1:
            return "Invalid input. Please fill all fields correctly.", 400

        if quantity > event['available_tickets']:
            return "Not enough tickets available.", 400

        # Reduce available tickets
        event['available_tickets'] -= quantity

        # Store booking (generate a booking reference)
        booking_ref = str(uuid.uuid4())[:8].upper()
        bookings.append({
            'ref': booking_ref,
            'event_id': event['id'],
            'event_title': event['title'],
            'name': name,
            'email': email,
            'quantity': quantity
        })

        return redirect(url_for('confirmation', ref=booking_ref))

    return render_template('booking.html', event=event)

@app.route('/confirmation/<ref>')
def confirmation(ref):
    booking = next((b for b in bookings if b['ref'] == ref), None)
    if not booking:
        return "Booking not found", 404
    return render_template('confirmation.html', booking=booking)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
