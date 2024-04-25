"""
This is the main file for your Flask app, containing app set-up and all of the routes.
In a more complex application you would split your routes into other files as needed.
"""
from datetime import datetime

from flask import  jsonify
from models import event  # Adjust import based on your project structure



from flask import Flask, render_template, request
from peewee import IntegrityError
from models import mydb, chapter, member, event, donation
from flask_wtf import CSRFProtect
from flask import redirect
from flask import url_for


# from logic import *

app = Flask(__name__)

@app.before_request
def before_request():
    mydb.connect()

@app.after_request
def after_request(response):
    mydb.close()
    return response

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db/data'


@app.route('/')
def admin_panel():
    # courses = Course.select()
    return render_template("index.html")

@app.route('/members')
def members():
    members_query = member.select()
    members_list = [member_to_dict(m) for m in members_query]  # Convert each member to a dict
    return render_template("members.html", members=members_list)

@app.route('/main')
def main_page():
    # Get the sort parameter or use a default value
    sort_by = request.args.get('sort_by', 'chaptername-asc')
    # Use a try-except block to handle the possibility of unpacking failure
    try:
        field, order = sort_by.split('-')
    except ValueError:
        # Set default values if the input is not valid
        field = 'chaptername'
        order = 'asc'
    
    # Logic to determine how to sort the query
    if field == 'chaptername':
        if order == 'desc':
            chapters = chapter.select().order_by(chapter.chaptername.desc())
        else:
            chapters = chapter.select().order_by(chapter.chaptername.asc())
    elif field == 'numberofmembers':
        if order == 'desc':
            chapters = chapter.select().order_by(chapter.numberofmembers.desc())
        else:
            chapters = chapter.select().order_by(chapter.numberofmembers.asc())
    else:
        # Fallback if the field is unknown
        chapters = chapter.select()

    return render_template("main.html", chapters=chapters)



@app.route('/events')
def events():
    events_query = event.select()  # Or your ORM's equivalent query
    event_data = [
        {
            'eventname': e.eventname,
            'venue': e.venue,
            'eventdate': e.eventdate.strftime('%Y-%m-%d'),
            'theme': e.theme,  # Make sure 'theme' is the correct field name
            'attendance': e.numberofmembersattended  # Ensure this is the correct field name
        }
        for e in events_query
    ]
    return render_template("events.html", events=event_data)


   
@app.route('/donations')
def donations():
    donations_query = donation.select().join(member)
    print(donations_query)
    return render_template("donations.html", donations=donations_query)



@app.route('/add_member', methods=['POST'])
def add_member():
    try:
        # Assuming you are sending these fields in the request
        first_name = request.form['first_name']
        middle_name = request.form.get('middle_name', '')  # Use .get for optional fields
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        score = request.form['score']
        address = request.form['address']
        number_of_events_attended = request.form['number_of_events_attended']
        status = request.form['status'] 

        # Create new member instance and save to the database
        new_member = member.create(
            firstname=first_name,
            middlename=middle_name,
            lastname=last_name,
            phonenumber=phone_number,
            score=score,
            memberaddress=address,
            numberofeventsattended=number_of_events_attended,
            status = status
        )
        status = 'active'
        new_member.save()
        return redirect(url_for('members'))

    except Exception as e:
        # If an error occurs, log it and send a 500 error response
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500


    
@app.route('/add_event', methods=['POST'])
def add_event():
    try:
        new_event = event.create(
            eventname=request.form['event_name'],
            venue=request.form['venue'],
            eventdate=request.form['event_date'],
            theme=request.form['theme'],
            numberofmembersattended=request.form['attendance']
        )
        new_event.save()
        return redirect(url_for('events'))
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred", 500
    


@app.route('/add_donation', methods=['POST'])
def add_donation():
    try:
        donor_id = request.form['donor_id']
        item = request.form['item']
        monetaryWorth = request.form['monetaryWorth']

        new_donation = donation.create(
            donor=donor_id, 
            item=item,
            monetaryWorth=monetaryWorth
        )
        return jsonify({
            'id': new_donation.id,
            'donor_id': donor_id,
            'item': item,
            'monetaryWorth': monetaryWorth
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/update_donation', methods=['POST'])
def update_donation():
    try:
        donation_id = request.form['donation_id']
        donor_id = request.form['donor_id']
        item = request.form['item']
        monetaryWorth = request.form['monetaryWorth']

        donation_instance = donation.get_by_id(donation_id)
        donation_instance.donor = donor_id
        donation_instance.item = item
        donation_instance.monetaryWorth = monetaryWorth
        donation_instance.save()

        return jsonify({
            'id': donation_id,
            'donor_id': donor_id,
            'item': item,
            'monetaryWorth': monetaryWorth
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/update_event', methods=['POST'])
def update_event():
    try:
        event_id = request.form['event_id']  # Use a hidden input in your form to send the event's ID
        venue = request.form['venue']
        event_date = request.form['event_date']
        theme = request.form['theme']
        attendance = request.form['attendance']

        # Retrieve the event by ID
        event_to_update = event.get_by_id(event_id)

        # Update the event's properties
        event_to_update.venue = venue
        event_to_update.eventdate = datetime.strptime(event_date, '%Y-%m-%d')
        event_to_update.theme = theme
        event_to_update.numberofmembersattended = attendance
        event_to_update.save()

        # Redirect or return a success response
        return redirect(url_for('events'))
    
    except event.DoesNotExist:
        # Event with the given ID does not exist
        return jsonify({'error': 'Event not found'}), 404
    except Exception as e:
        # Handle other exceptions
        return jsonify({'error': str(e)}), 500



@app.route('/update_member', methods=['POST'])
def update_member():
    member_id = request.form['member_id']
    try:
        # Use a different variable name for the member instance
        member_instance = member.get_by_id(member_id)  # Assuming 'Member' is your model class name
        member_instance.firstname = request.form['first_name']
        member_instance.middlename = request.form['middle_name']
        member_instance.lastname = request.form['last_name']
        member_instance.phonenumber = request.form['phone_number']
        member_instance.score = request.form['score']
        member_instance.memberaddress = request.form['address']
        member_instance.numberofeventsattended = request.form['number_of_events_attended']
        member_instance.save()
        return jsonify({'message': 'Member updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500



def member_to_dict(member):
    return {
        "memberid": member.memberid,
        "firstname": member.firstname,
        "middlename": member.middlename,
        "lastname": member.lastname,
        "phonenumber": member.phonenumber,
        "score": member.score,
        "memberaddress": member.memberaddress,
        "numberofeventsattended": member.numberofeventsattended,
        "status": member.status
    }


@app.route('/delete_member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        member = member.get(member.memberid == member_id)
        member.delete_instance()
        return jsonify({'message': 'Member deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


"""
Flask can use a variety of decorators to enhance application functionality.
In this case we are using `before_request` to add code that executes before
every request to the application. 

This method gets a user from the database and assigns it to an attribute of 
Flask's global object, `g`.  `g` is available in all templates, and is defined
for the duration of the request. Note: `g` does NOT persist between different 
requests. Sessions, cookies, and the database must be used for true persistence.

Obviously, hard-coding one particular student as the logged-in user is not what
a real application would do. In practice, this function would get a user from 
whatever the login/authentication system has stored in the session.
"""
# from flask import g
# @app.before_request
# def load_user():
#     g.user = Student.get_by_id(2)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)