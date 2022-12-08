#  Vest Schedule Generator

Generates a schedule for a stock option grant.

> This application is built using Python 3.9 and Django Rest Framework 3.12

I developed this formula to calculate values of a vest for a certain moment:

$$
quantity( month) =  quantity  * ((cliffpercentage  + ((month  /  duration) -  cliffpercentage))* (((duration  -  cliff) +  month) //  duration)) 
$$

# Installation instructions
You can run this application by choose either running via **Docker** **OR** **Locally**.


## Running with Docker
### Requirements

 - Docker desktop

 
### Steps

 1. Clone the project into your preferable directory on your machine
 2. Open your terminal and navigate to root of the the cloned directory

    `$ cd some-path/stock-option-grant/` 

3. Build the image
	
	`$ some-path/stock-option-grant> docker build .`
	
	or 
	
	`$ some-path/stock-option-grant> docker-compose build`

 4. Run the application
 
     `$ some-path/stock-option-grant> docker-compose up`




## Running locally
### Requirements

 - Python 3.9 installed in your machine.

 
### Steps

 1. Clone the project into your preferable directory on your machine.
 2. Open your terminal and navigate to root of the the cloned directory.

    `$ cd some-path/stock-option-grant/` 

3. Create and activate a python virtual environment .
	
     [Instructions of how to create a python virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)

 4. Install requirments.

    `$ (venv) some-path/stock-option-grant/> pip install -r /tmp/requirements.txt`

5. Run the application.

     `$ (venv) some-path/stock-option-grant/> python manage.py runserver 0.0.0.0:8000` 

## Running Application 

> **Note 1:** Even though the application was built using Django Rest Framework, the admin page isn't available for this current version.
> **Note 2:**No authentication needed for the current version.

In your browser your can access the following address `127.0.0.1:8000/`
### Documentation
You can find the api documentation by accessing `127.0.0.1:8000/api/docs/`
> **Note:**  The documentation was made using Swagger, by accessing this URL you can also make requests to all resources available.

### Generate schedule

**URL** : `127.0.0.1:8000/api/vesting/schedule/`

**Method** : `POST`

**Auth required** : NO

**Data example**

```json
{
	"option_grants": [
		{
		"quantity": 4800,
		"start_date": "01-01-2018",
		"cliff_months": 12,
		"duration_months": 48
		}
		],
		"company_valuations": [
		{
		"price": 10.0,
		"valuation_date": "09-12-2017"
		}
	]
}
```
For full documentation access  `127.0.0.1:8000/api/docs/`

## Running Tests
### Locally
`$ (venv) some-path/stock-option-grant/> python manage.py test` 

### Docker
`$ some-path/stock-option-grant/> docker-compose run app -rm sh -c "python manage.py test"` 


