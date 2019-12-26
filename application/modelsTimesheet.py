from application import db
from application.models import User

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(120),nullable=False)
    name = db.Column(db.String(120))
    tsht = db.Column(db.Integer, db.ForeignKey('tsht_setting.id'), nullable=False)

    def __repr__(self):
        return '<Project {}>'.format(self.name)

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    project = db.relationship(Project, backref='assignments')
    user = db.relationship(User, backref='assignments')
    rate  = db.Column(db.Float(),nullable=False)
    currency  = db.Column(db.String(10),nullable=False)
    rate_basis  = db.Column(db.String(10),nullable=False)

    def __repr__(self):
        return '<Assignment -ID - {}>'.format(self.id)


class TshtSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    identifier = db.Column(db.String(20),nullable=False)
    description = db.Column(db.String(250))

    act_code_enable = db.Column(db.Boolean())
    act_title = db.Column(db.String(50))

    wla_hrs_enable = db.Column(db.Boolean())
    wla_code_enable = db.Column(db.Boolean())
    wla_title = db.Column(db.String(50))

    wlb_hrs_enable = db.Column(db.Boolean())
    wlb_code_enable = db.Column(db.Boolean())
    wlb_title = db.Column(db.String(50))

    lv_hrs_enable = db.Column(db.Boolean())
    lv_code_enable = db.Column(db.Boolean())
    lv_title = db.Column(db.String(50))

    tra_hrs_enable = db.Column(db.Boolean())
    tra_code_enable = db.Column(db.Boolean())
    tra_title = db.Column(db.String(50))

    trb_hrs_enable = db.Column(db.Boolean())
    trb_code_enable = db.Column(db.Boolean())
    trb_title = db.Column(db.String(50))

    ot_hrs_enable = db.Column(db.Boolean())
    ot_code_enable = db.Column(db.Boolean())
    ot_title = db.Column(db.String(50))

    remarks_enable = db.Column(db.Boolean())
    remarks_title = db.Column(db.String(50))



    def __str__(self):
        return self.description
