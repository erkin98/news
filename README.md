# CRUD API WITH DJANGO REST FRAMEWORK

## Installation
After you cloned the repository and installed docker,
You can do this by running the command
```
docker-compose up --build
```
It will prepare containers

## Structure
In a RESTful API, endpoints (URLs) define the structure of the API and how end users access data from our application using the HTTP methods - GET, POST, PUT, DELETE. Endpoints should be logically organized around _collections_ and _elements_, both of which are resources.

In our case, we have one single resource, `posts` and `comments`, so we will use the following URLS - `/posts/` and `/posts/<id>` for collections and elements, respectively:

Endpoint |HTTP Method | CRUD Method | Result
-- | -- |-- |--
`posts` | GET | READ | Get all movies
`posts/:id` | GET | READ | Get a single movie
`posts`| POST | CREATE | Create a new movie
`posts/:id` | PUT | UPDATE | Update a movie
`posts/:id` | DELETE | DELETE | Delete a movie

## Use
We can test the API using [curl](https://curl.haxx.se/) or [httpie](https://github.com/jakubroztocil/httpie#installation), or we can use [Postman](https://www.postman.com/)

[Link to Postman collection](https://solar-shuttle-540014.postman.co/workspace/673ad0b5-f79d-4d26-aca9-e37a9e6947af)

[Link to Deployed API](http://64.225.98.124:8030/api/v1)
