from application.models import User
from application.modelsTimesheet import Project, Assignment


q = Assignment.query.outerjoin(Project, Project.id == Assignment.project_id).all()

for i in q:
    print(i.__dict__)
