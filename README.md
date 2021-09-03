# Project 7: Create GrandPy Bot, the grandpa robot

This Python program is using Google and MediaWiki APIs in order to find geodata about the user request.

You can check project details on [Trello](https://trello.com/b/ms6LxJ9V/project-7).

## Installation

Create a virtual environment with the [venv](https://docs.python.org/3/tutorial/venv.html) module to install the program:

```bash
python3 -m venv .venv
```

Then, activate the virtual environment:

```bash
.venv/Scripts/activate
```

Install the dependencies using the package manager [pip](https://pip.pypa.io/en/stable/):

```bash
pip install -r requirements.txt
```

Finally, create a `.env` file at the project root, and insert the following:

```bash
API_KEY=your_key
```

Replace `your_key` with your Google API key.

## Usage

### Local usage

Start the program with `python3 main.py`.

Now, go to [localhost](https://localhost:5000/) and ask a question about a place.

The program will parse your request to find keywords.
After that, a request will be sent to the Google Maps API to get geodata and map about keywords.
Finally, another request will be sent, with the geodata, to the MediaWiki API in order to find details about a place.

## License

[MIT](https://www.wikipedia.org/wiki/MIT_License)
