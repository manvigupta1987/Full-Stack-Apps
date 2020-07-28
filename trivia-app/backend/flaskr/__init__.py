import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        if len(categories) == 0:
            abort(404)

        categories_dict = {}

        for category in categories:
            categories_dict[category.id] = category.type

        return jsonify({
            'success': True,
            'categories': categories_dict,
            'total_categories': len(categories)
        })

    '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

    @app.route('/questions')
    def get_questions():
        questions = Question.query.order_by(Question.difficulty).all()
        if len(questions) == 0:
            abort(404)
        categories = Category.query.order_by(Category.id).all()
        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = category.type
        formatted_questions = paginate_questions(request, questions)
        if len(formatted_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(questions),
            'categories': categories_dict,
            'currentCategory': list(set(question['category'] for question in formatted_questions))
        })

    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()
        if question is None:
            abort(422)
        question.delete()
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, questions)

        return jsonify({
            'success': True,
            'deleted': question_id,
            'questions': current_questions,
            'total_questions': len(questions)
        })

    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        question = body.get('question', None)
        answer = body.get('answer', None)
        difficulty = body.get('difficulty', None)
        category = body.get('category', None)
        search = body.get('searchTerm', None)
        try:
            if search:
                questions = Question.query.filter(Question.question.ilike(f'%{search}%')).all()

                if len(questions) == 0:
                    return jsonify({
                        'success': True,
                        'message': 'No results found!!!'
                    })
                formatted_questions = paginate_questions(request, questions)
                return jsonify({
                    'success': True,
                    'questions': formatted_questions,
                    'currentCategory': list(set(question['category'] for question in formatted_questions))
                })

            else:
                question = Question(question=question, answer=answer, difficulty=difficulty, category=category)
                question.insert()

                current_questions = Question.query.all()
                formatted_questions = paginate_questions(request, current_questions)

                return jsonify({
                    'success': True,
                    'created': question.id,
                    'total_questions': len(formatted_questions)
                })

        except:
            abort(422)

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_basedon_category(category_id):
        questions = Question.query.filter(Question.category == category_id).all()
        if len(questions) == 0:
            abort(404)

        formatted_questions = paginate_questions(request, questions)
        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'totalQuestions': len(questions),
            'currentCategory': list(set(question['category'] for question in formatted_questions))
        })

    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

    @app.route('/quizzes', methods=['POST'])
    def get_random_question():
        body = request.get_json()
        category = body.get('quiz_category', None)
        prev_questions = body.get('previous_questions', None)

        if (category is None) or (prev_questions is None):
            abort(400)

        if category['id'] == 0:
            questions = Question.query.all()
        else:
            questions = Question.query.filter(Question.category == category['id']).all()

        total = len(questions)

        if len(prev_questions) == total:
            return jsonify({
                'success': True
            })

        formatted_questions = paginate_questions(request, questions)

        if len(questions) == 0:
            abort(422)

        random_question = random.choice(formatted_questions)

        def is_question_used(ran_question):
            for question in prev_questions:
                if question == ran_question['id']:
                    return True

            return False

        while is_question_used(random_question):
            random_question = random.choice(formatted_questions)

        return jsonify({
            'success': True,
            'question': random_question
        })

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    return app
