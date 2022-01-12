from flask_admin import  BaseView,AdminIndexView, expose
from flask_login import login_required, login_user,current_user, logout_user



class HomeView(AdminIndexView):

    @expose("/")
    def index(self):
    	return self.render('admin/home.html')

    def is_accessible(self):
        return current_user.is_authenticated
