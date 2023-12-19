from flask import jsonify, make_response
from google.cloud import firestore

def visitor_count(request):

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600'
    }

    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return make_response(('OK', 204, headers))

    if request.method == 'POST':
        database = firestore.Client()
        visitor_ref = database.collection('visitors').document('websiteCounter')
        visitor_nb = 0

        # Get the current count and increment 
        doc = visitor_ref.get()
        if doc.exists:
            visitor_nb = int(doc.to_dict()['count'])
        new_visitor_count = visitor_nb + 1

        # Save the new count to db
        visitor_ref.set({'count': new_visitor_count})

        # Return the new visitor count
        response = make_response(jsonify({'currentVisitor': new_visitor_count}))
        response.headers.extend(headers)
        return response

    return make_response(('Error!', 405, headers))