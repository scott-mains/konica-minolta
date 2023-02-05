# Hold That Line
A connect-the-dots game based on the original by Sid Sackson

Implemented in response to:

[Konica Minolta Business Solutions Technical Assessment](https://technical-assessment.konicaminoltamarketplace.com/)

## Framework
The API is implemented for Python 3.11 using [FastAPI](https://fastapi.tiangolo.com/) with 
[Pydantic](https://docs.pydantic.dev/) dataclasses (see `requirements/requirements.txt` for details).

## Installing
To install the API server use Pip in a Python 3.11 environment:

```shell
pip install -r requirements/requirements.txt
```

## Starting the API
To run the API, use the convenience script from root:

```shell
./scripts/up
```

This starts the api server on the local host.

## Client
A copy of the client has been included in this repo configured for the HTTP api type as follows:
```javascript
const app = Elm.Main.embed(node, {
    api: 'Http',
    hostname: 'http://localhost:8000'
});
```
Note: FastAPI serves on port 8000 by default, not port 8080

## Playing the Game

To play the game:
1. Start the API (see above).
2. Open `client/index.html` in Chrome or Firefox.

# Known Issues
1. In some cases when a selected end node is on a diagonal, valid end nodes are ruled invalid, and vice versa. 