from django.shortcuts import redirect

# to check if the user is logged in or not.
def unauthneticated_user(view_function):
    def wrapper_function(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_function(request,*args,**kwargs)
    
    return wrapper_function

# to redirect admin only to the admin dashboard page if the request is comes from the admin otherwise redirect to user profile page.
def admin_only(view_function):
    def wrapper_function(request,*args,**kwargs):
        if request.user.is_staff:
            return view_function(request,*args,**kwargs)
        else:
            return redirect('/')
    
    return wrapper_function

