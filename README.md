Python bindings to the [Onadata][1] API
=====================
This repo contains the sources for the Onadata python client library. 
You can read more about Onadata [here][1]

####Installation:-
`pip install git+https://github.com/onaio/onaie.git`  
OR as a [pip editable](http://pip.readthedocs.org/en/latest/reference/pip_install.html#editable-installs) if you'd like to develop this in parallel with your project:-  
`pip install -e git://github.com/onaio/onapie.git#egg=onapie`  

####Example Usage
***Initialization:-***  
`from onapie.client import Client`  
`client = Client('https://ona.io', username='your_ona_username', password='S00p3rS3kret')`  
or if you prefer to use your api_token:-  
`client = Client('https://ona.io', api_token='your_ona_api_token')`  

***Working with forms:-***  
upload form:-  
 - From file `forminfo_dict = client.forms.create('/path/to/form.xls')`  
 - From URL  `forminfo_dict = client.forms.create('/path/to/form.xls')`  
Get form:-  
 - info `forminfo_dict = client.forms.get('form_pk')`  
 - Representation `json_form_repr = client.forms.get('form_pk', 'JSON')`  
List forms:- `form_list = client.forms.list()`  

***Working with Data:-***  
Endpoints:- `data_endpoints = client.data.list_endpoints()`  
Get submitted data for a given form:- 
 - All:- `form_data_list = client.data.get(form_pk)`  
 - Single:- `form_datum = client.data.get(form_pk, datum_id)`  
 - by tags:- `form_data_list = client.data.get(form_pk, None, tag1, tag2, tag3, tag4 )`  
 - by query:- `form_data_list = client.data.get(form_pk, None, param1=value1, param2=value2 )`  

####Contributing
- [Fork and] create a branch named according to the feature you want to work on  
- Clone your new repo & create a virtualenv for that
- Install the dev deps: `pip install -r dev-requirements.txt`
- Setup the pre-commit Hook: `ln -s ../../pre-commit.sh .git/hooks/pre-commit`
- Contribute/Develop/Hack
- Send a pull request against the [develop][2] branch


[1]: https://github.com/onaio/onadata
[2]: https://github.com/onaio/onapie/tree/develop
