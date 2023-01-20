import os
from flask import Flask, request, abort, jsonify, app
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import datetime as dt
from auth import requires_auth, AuthError
from models import Actors, Movies, setup_db


def create_app(test_config=None):
    app = Flask(__name__)

    # cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    #
    # CORS Headers
    # @app.after_request
    # def after_request(response):
    #     response.headers.add(
    #         'Access-Control-Allow-Headers',
    #         'Content-Type,Authorization,true'
    #     )
    #     response.headers.add(
    #         'Access-Control-Allow-Methods',
    #         'GET,PATCH,POST,DELETE,OPTIONS'
    #     )
    #     return response

    setup_db(app)


    '''
    Get List of all actors
    '''
    @app.route("/actors", methods=["GET"])
    @requires_auth('get:actors')
    def get_all_actors(payload):
        actors = Actors.query.all()
        return jsonify({
            'success': True,
            'actors': [q.format() for q in actors]
        })


    '''
    Get list of all the movies
    '''
    @app.route("/movies", methods=["GET"])
    @requires_auth('get:movies')
    def get_all_movies(payload):
        movies = Movies.query.all()

        return jsonify({
            'success': True,
            'movies': [q.format() for q in movies]
        })

    '''
    Delete the actor <actor_id> passed in the query parameter
    '''
    @app.route("/actor/<int:actor_id>", methods=["DELETE"])
    @requires_auth('delete:actor')
    def delete_actor(payload, actor_id):
        actor = Actors.query.get(actor_id)
        if actor == None:
            abort(404)
        actor.delete()
        return jsonify({
            "success": True,
            "deleted": actor_id
        })

    '''
    Delete the movie <movie_id> passed in the query parameter
    '''
    @app.route("/movie/<int:movie_id>", methods=["DELETE"])
    @requires_auth('delete:movie')
    def delete_movie(payload,movie_id):
        movie = Movies.query.get(movie_id)
        if movie == None:
            abort(404)
        movie.delete()
        return jsonify({
            "success": True,
            "deleted": movie_id
        })

    '''
    create new actor with name, age and gender details
    '''
    @app.route("/actor", methods=["POST"])
    @requires_auth('post:actor')
    def create_actor(payload):
        body = request.get_json()
        try:
            name = body.get("name", None)
            gender = body.get("gender", None)
            age = body.get("age", None)
            q = Actors(name=name, gender=gender, age=age)
            q.insert()

            return jsonify(
                {
                    "success": True,
                    "created": q.id
                }
            )

        except:
            abort(422)




    '''
    Create new movie with title and release_date
    '''
    @app.route("/movie", methods=["POST"])
    @requires_auth('post:movie')
    def create_movie(payload):
        body = request.get_json()
        now = dt.datetime.now().date()

        try:
            title = body.get("title", None)
            release_date = body.get("release_date", None)

            q = Movies(title=title, release_date=release_date)
            q.insert()
            return jsonify(
                {
                    "success": True,
                    "created": q.id
                })
        except Exception as ex:
            abort(422)

    '''
    Update the existing movie_id by patch request 
    '''
    @app.route('/movie/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def patch_movie(payload, movie_id):
        body = request.get_json()
        try:
            movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
            if not movie:
                abort(404)
            movie.title = body['title']
            movie.release_date = body['release_date']
            movie.update()
            return jsonify({
                'success': True,
                'updated': movie_id
            })
        except Exception as ex:
            print(ex)
            abort(422)

    '''
    Update the existing actor_id by patch request 
    '''
    @app.route('/actor/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def patch_actor(payload, actor_id):
        body = request.get_json()
        try:
            actor = Actors.query.filter(Actors.id == actor_id).one_or_none()
            if not actor:
                abort(404)
            actor.name = body['name']
            actor.age = body['age']
            actor.gender = body['gender']

            return jsonify({
                'success': True,
                'updated': actor_id
            })
        except Exception as ex:
            abort(422)


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': "unprocessable"
        }), 422


    @app.errorhandler(401)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': "unauthorised"
        }), 401


    @app.errorhandler(404)
    def notfound(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "resource not found"
        }), 404


    @app.errorhandler(AuthError)
    def autherror(error):
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error['description']
        }), error.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
