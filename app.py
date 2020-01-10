from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import date
import os
host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/contractorv1')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
ists = db.ists
sessions = db.sessions



app = Flask(__name__)





@app.route('/ists/meeting')
def ists_meeting():
    """Create a new meeting."""
    return render_template('meeting.html')
# @app.route('/')
# def ist_index():
#     """Homepage"""
#     return render_template()





@app.route('/ists/<istid>/session')
def new_session(istid):
    """creates a new session within a client profile"""
    return render_template('session_form.html', istid=istid)


@app.route('/ists/session_submit',methods=['POST'])
def submit_session():
    istid=request.form.get('istid')
    print(istid)


    session = {
        'title' : request.form.get('title'),
        'content': request.form.get('content'),
        'date': str(date.today()),
        'ist_id': istid
    }
    sessions.insert_one(session)
    return redirect(f'/detail/{istid}')



@app.route('/')
def ist_index():
    """Return homepage."""
    return render_template('ists_index.html', ists=ists.find())

@app.route('/ists/new')
def ists_new():
    """Create a new ist."""
    return render_template('ists_new.html')

    
@app.route('/ists', methods=['POST'])
def ist_submit():
    """Submit a new ist."""
    ist = {
        'name': request.form.get('name'),
        'age': request.form.get('age'),
        'image': request.form.get('image'),
        'date': request.form.get('date'),
        'sessions': []
    }
    ists.insert_one(ist)
    #print(request.form.to_dict())
    return redirect(url_for('ist_index'))



@app.route('/detail/<ist_id>')
def ists_detail(ist_id):
    """Show a single ist."""
    ist = ists.find_one({'_id': ObjectId(ist_id)})
    all_sessions= sessions.find({'ist_id':ist_id})
    print (ist)
    return render_template('ists_detail.html', ist = ist, all_sessions=all_sessions)

@app.route('/update/<ist_id>', methods=['POST'])
def ists_update(ist_id):
    """Submit an edited ist."""
    
    # create our updated playlist
    updated_ist = {
        'name': request.form.get('name'),
        'age': request.form.get('age'),
        'image': request.form.get("image"),
        'date': request.form.get("date")    
    }
    # set the former playlist to the new one we just updated/edited
    ists.update_one(
        {'_id': ObjectId(ist_id)},
        {'$set': updated_ist})
    # take us back to the playlist's show page
    return redirect(url_for('ists_detail', ist_id=ist_id))


@app.route('/ists/<ist_id>/edit')
def ists_edit(ist_id):
    """Show the edit form for a ist."""
    ist = ists.find_one({'_id': ObjectId(ist_id)})
    # Add the title parameter here
    return render_template('ists_edit.html', ist=ist, title='Edit ist')


@app.route('/ists/<ist_id>/delete', methods=['POST'])
def ists_delete(ist_id):
    """Delete one ist."""
    ists.delete_one({'_id': ObjectId(ist_id)})
    return redirect(url_for('ist_index'))




# app.py

if __name__ == '__main__':
    # update the below line to the following:
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))

