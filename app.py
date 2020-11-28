from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from rq import Queue
from rq.job import Job
from worker import conn
from algorithm import fake_algorithm
import json

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
q = Queue(connection=conn)

from models import Result


def recolorate_image(image_json):
    
    new_image = fake_algorithm(image_json)
    try:
        result = Result(
            image = new_image
        )
        db.session.add(result)
        db.session.commit()
        return result.id
    except:
        errors.append("Unable to add item to database.")
        return {"error": errors}


@app.route('/', methods=['POST'])
def postimage():
    if 'img' in request.json:
        try:
            job = q.enqueue_call(
                func=recolorate_image, args=(request.json,), result_ttl=15
            )
            print(job.get_id())
            return jsonify(job_id= job.get_id())
        except:
            return jsonify(status= 'Image queue failed')
    else:
        return jsonify(status= 'Not image found')

@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):

    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        result = Result.query.filter_by(id=job.result).first()
        return result.image
    else:
        return "Not found", 202


def addHeaders(response):
    response.headers.add('Content-Type', 'application/json')
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Expose-Headers', 'Content-Type,Content-Length,Authorization,X-Pagination')
    return response



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
