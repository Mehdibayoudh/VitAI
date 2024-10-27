from .models import User

def user_context(request):
    user_id = request.session.get('user_id')
    user = User.objects(id=user_id).first() if user_id else None
    return {'user': user}