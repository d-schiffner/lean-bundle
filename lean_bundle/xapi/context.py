from . import actor

def parse(auth_grp, fibers, statement):
    if not 'context' in statement:
        return
    #TODO: Write context information here
    context = statement.context
    new_context = {}
    if 'instructor' in context:
        instructor = actor.create_user(auth_grp, context.instructor)
        instructor.attrs.modify('isInstructor', True)
        fibers.attrs['instructor'] = instructor.ref
        new_context['instructor'] = context.instructor
    statement.context = new_context
