from data import db_session

from flask import Flask, render_template
from data.jobs import Jobs
from data.user import User
db_session.global_init("db/mars_explorer.db")
db_sess = db_session.create_session()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

@app.route('/')
@app.route('/jobs_table')
def index():
    lines = db_sess.query(Jobs).all()
    jobs = []
    for el in lines:
        jobs.append([f'Action #{el.id}', el.job, el.team_leader, f'{el.work_size} hours', el.collaborators,
                     'is finished'])
        jobs[-1][2] = db_sess.query(User).filter(User.id == el.team_leader).first()
        if jobs[-1][2]:
            jobs[-1][2] = jobs[-1][2].surname, jobs[-1][2].name
        if not el.is_finished:
            jobs[-1][-1] = jobs[-1][-1][:2] + ' not' + jobs[-1][-1][2:]
    return render_template('index.html', jobs=jobs)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
