
# Sources  
Thanks to [@kgtechs](https://www.youtube.com/@kgtechs) for [the youtube walkthrough](https://www.youtube.com/watch?v=cy7Xk35iiGc) of the  [django_auth_adfs install docs](https://django-auth-adfs.readthedocs.io/en/latest/install.html) this readme and repo is a reference for these materials.  
You can follow along with this readme and the youtube referenced above, or you can just clone the repo run the install instructions and config ur client settings in the .env file
## notes on my environment:
### os
```
$ lsb_release -a

No LSB modules are available.
Distributor ID:	Ubuntu
Description:	Ubuntu 24.04.1 LTS
Release:	24.04
Codename:	noble
```
### conda
```
$ conda --version
conda 24.5.0
```
### python
```
$ python --version
Python 3.13.0
```
### django
```
$ python -m  django --version
5.1.3
```
## Note on pip  
my mostly vanilla conda install did not have pip installed so i also had to include that in my installation. 
```
conda install pip
```
# Installation:  
```
mkdir django_auth_example
cd django_auth_example/
conda create -n denv
conda activate denv
conda config --add channels conda-forge
conda config --set channel_priority strict 
conda install django --channel conda-forge
pip install django-auth-adfs
pip install python-dotenv
django-admin startproject azurelogin .
```
after install and running django admin setup you will have the following in your folder:
```
$ls 
azurelogin manage.py
$ls azurelogin
asgi.py  __init__.py  settings.py  urls.py  wsgi.py
```

# Configuration
1. Per [django_auth_adfs install docs](https://django-auth-adfs.readthedocs.io/en/latest/install.html)  
  Edit your `settings.py` as follows
    - insert the `AUTHENTICATION_BACKENDS`, `INSTALLED_APPS`, `MIDDLEWARE` settings
    - insert `LOGIN_URL` and `LOGIN_REDIRECT_URL`
    - also edit your `urls.py` 
    - edit the djanog import with include `from django.urls import path,include`
2. Update your `urls.py` to include new `urlpatterns` 
3. Create `.env`  file in your `azurelogin` folder  
    ```
    client_id = your_client_id
    client_secret = your_client_secret
    tenant_id = you_tenant_id
    ```
4.  Azure Config  
  [django_auth_adfs azure ad config guide](https://django-auth-adfs.readthedocs.io/en/latest/azure_ad_config_guide.html)  
  * Step 1 - Register a backend application
  * login to [azure](https://portal.azure.com/) ensure you are in the right AD directory for me i tested with [Default Directory](https://portal.azure.com/#view/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/~/Overview ) and configure the application updating `.env` file created above with your information
  * Step 2 - Configuring settings.py
    - update `settings.py`
      - insert `AUTHENTICATION_BACKENDS` per documentation
      - insert needed imports and variables as follows
      ``` 
      #imports
      from dotenv import load_dotenv
      import os
      load_dotenv()
        #.....
      client_id = os.getenv('client_id')
      client_secret = os.getenv('client_secret')
      tenant_id = os.getenv('tenant_id')
      #.....
      ```
    - insert `AUTH_ADFS` as follows:
        ```
        AUTH_ADFS = {
        'AUDIENCE': client_id,
        'CLIENT_ID': client_id,
        'CLIENT_SECRET': client_secret,
        'CLAIM_MAPPING': {'first_name': 'given_name',
                          'last_name': 'family_name',
                          'email': 'email'},
        'USERNAME_CLAIM': 'given_name',
        'TENANT_ID': tenant_id,
        'RELYING_PARTY_ID': client_id,
        }       
        ```
        '*'note 
          `GROUPS_CLAIM` and `MIRROR_GROUPS` removed as groups was not provided my my Azure
          `USERNAME_CLAIM` altered to use `given_name` as `upn` was not provided my my Azure
    - Update `urls.py` to include new `urlpatterns` 
  * Step 3 - Register and configure an Azure AD frontend application
  
5. Middleware Config 
  [django_auth_adfs install docs Login Middleware](https://django-auth-adfs.readthedocs.io/en/latest/middleware.html)   
  * update `settings.py` with new `MIDDLEWARE`
  * OPTIONAL: if desired may update `AUTH_ADFS` to also include `LOGIN_EXEMPT_URLS`
6.  start (create??) app
  *  `$ python manage.py startapp app`
  * add `app` to `INSTALLED_APPS` in `settings.py`
  * create `app\urls.py`
    ```
    from django.shortcuts import render
    from django.http import HttpResponse
    # Create your views here.
    def login_successful(request):
    return HttpResponse("200 ok")
    ```
  * update `urls.py` with new `urlpatters`
    - `path('', include('app.urls')),`

7. Optional: Debug loggin
  * update `settings.py` with the followign:
  ```
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(name)s %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
        },
        'loggers': {
            'django_auth_adfs': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
        },
    }
  ```
  
8. Migrations
  ```
  python manage.py makemigrations
  python manage.py migrate
  ```
# Running the Server:  
```
python manage.py runserver
#runserver with warnings enables
#python -Wd manage.py runserver
```
browse to http://127.0.0.1:8000/

