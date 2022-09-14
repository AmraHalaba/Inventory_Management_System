from django.shortcuts import render, redirect

#decorator is function that takes another function as a parameter, thereby enables adding some more functionality before the original function is called --> when I add it before functions in views.py, this main function it will take each that function as a parameter

# ---------------------------------------------------------------------------------------------------------------
# Decorator for authentication
def unauthenticated_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/system/dashboard')
        else:
            return view_function(request, *args, **kwargs)
    return wrapper_function


# ---------------------------------------------------------------------------------------------------------------
# Decorator for allowing users access to the pages
def allowed_users(allowed_roles=[]):
    def decorator(view_function):
        def wrapper_function(request, *args, **kwargs):
            
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name #this will set the name of the group to which the user belongs
            if group in allowed_roles: #if that group that I got above is in the list of allowed roles    
                return view_function(request, *args, **kwargs) #then return the view function --> allow access to the given page
            else:
                return render(request, 'system/access_denied.html')
        return wrapper_function
    return decorator