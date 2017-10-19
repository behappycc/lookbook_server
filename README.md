# lookbook_server

## Setup

1. `$ virtualenv env -p 2`
2. `$ source env/bin/activate`
3. `$ pip install -r requirements.txt`
4. `$ python manage.py makemigrations`
5. `$ python manage.py migrate`

## Run

`$ python manage.py runserver 0.0.0.0:8000`

`Starting development server at http://0.0.0.0:8000/`

## API

GET `api/v1.0/user/[id]/`

Response body

```
{
  "city":"14",
  "gender":"male",
  "age":"14",
  "rank":[
    {
      "name":"Rio De Janeiro",
      "prob":"44.8"
    },
    {
      "name":"Prague",
      "prob":"24.1"
    },
    {
      "name":"Helsinki",
      "prob":"8.4"
    },
    {
      "name":"Casablanca",
      "prob":"4.7"
    },
    {
      "name":"Berlin",
      "prob":"3.0"
    },
    {
      "name":"others",
      "prob":"15.0"
    }
  ],
  "country":"14","id":"14",
  "imgUrl":"https://i.imgur.com/Sc59JV1.jpg"
}
```

POST `upload/[filen-ame]`

Request body:

```
{
  gender: "male", 
  age: "100", 
  country: "country", 
  city: "city", 
  image: "FILE"
}
```
