from alayatodo import app, login_required, message
from flask import (
    redirect,
    flash,
    render_template,
    jsonify,
    request,
    session
)
import alayatodo.service.todo as todo_service

@app.route('/todo/<int:id>', methods=['GET'])
@login_required
def todo(id):
    todo = todo_service.get_by_id(id)
    if todo:
        return render_template('todo.html', todo=todo)
    return redirect('/todo')


@app.route('/todo/<int:id>/json', methods=['GET'])
@login_required
def todo_json(id):
    todo = todo_service.get_by_id(id)
    if todo:
        return jsonify({
            'id': todo['id'],
            'username': todo['username'],
            'description': todo['description'],
            'completed': todo['completed'],
        })

    return jsonify({}), 404


@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
@app.route('/todo/page/<int:page>', methods=['GET'])
@login_required
def todo_list(page = 1):
    [todos, pagination] = todo_service.get_all(page)
    return render_template('todos.html', todos=todos, pagination=pagination)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
@app.route('/todo/page/<int:page>', methods=['POST'])
@login_required
def todos_POST():
    ok = todo_service.create_todo(request.form.get('description', ''))
    if ok:
        flash(message.TODO_CREATED)
    else:
        flash(message.TODO_NOT_CREATED)

    return redirect('/todo')


@app.route('/todo/<int:id>/del', methods=['POST'])
@login_required
def todo_delete(id):
    ok = todo_service.delete_todo(id)
    if ok:
        flash(message.TODO_DELETED)
    else:
        flash(message.TODO_DELETE_FAIL)

    return redirect('/todo')


@app.route('/todo/<int:id>/toggle', methods=['POST'])
@login_required
def todo_toggle(id):
    todo_service.toggle_todo(id)
    return redirect('/todo')
