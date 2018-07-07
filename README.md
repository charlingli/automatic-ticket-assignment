# Automatic Ticket Assignment

Accenture Bootcamp July 2018, by Team 5 (for success!)
This project is an extension application using [Python 3.6](https://www.python.org/downloads/release/python-365/) that fetches ticket data (minus assignment) from a [ServiceNow](https://www.servicenow.com/) instance, indexes it using [ElasticSearch](https://www.elastic.co/products/elasticsearch), queries for the most logical resource assignment, and returns this both through a [Kibana](https://www.elastic.co/products/kibana) instance for realtime feedback and back to ServiceNow through Python using a [RESTful](https://www.reddit.com/r/explainlikeimfive/comments/1fevr4/eli5_representational_state_transfer_rest_or/) [API](https://www.reddit.com/r/explainlikeimfive/comments/5u1qq2/eli5_what_is_an_api_and_what_are_restful_apis/).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine. Currently, these instructions only support Win10 systems.

### Prerequisites

1. Python 3 (https://www.python.org/downloads/release/python-365/, recommend 3.5+)
2. Java JDK (http://www.oracle.com/technetwork/java/javase/downloads/index.html, **except Java 10**, recommend 8/9)
3. Git (https://git-scm.com/, *Optional*)
4. ElasticSearch (https://www.elastic.co/products/elasticsearch)
5. Kibana (https://www.elastic.co/products/kibana, *Optional*)

### Installing

#### Python

First, install the prerequisites through binaries available on the websites linked above. These set up Python 3.6, Java, and Git on the local machine if they aren't already.

Next, we'll install our Python prerequisites through command line (recommend Windows PowerShell) - our libraries that aren't part of the initial Python package that are needed to connect with everything. The `elasticsearch` library is needed to correctly connect to the elasticsearch server, which we'll set up in just a moment. The `requests` library is needed to correctly make REST calls.

```
pip install elasticsearch
pip install requests
```

Make a new directory somewhere for the project and cd into it in command line. Clone this repository into this directory (if using Git, otherwise, just download this repository and extract).

```
cd \Documents\Accenture\
mkdir automatic-traffic-assignment\
cd automatic-traffic-assignment\
git clone https://github.com/charlingli/automatic-ticket-assignment.git
```

#### ElasticSearch

ElasticSearch is the search engine that indexes the data we send it, and quickly query for what we want to know. Download [elasticsearch-6.3.0](https://www.elastic.co/products/elasticsearch) and extract anywhere memorable.

No set-up is needed!

#### Kibana (Optional)

Kibana is a data visualisation tool that shows us in a web browser what we want to know from ElasticSearch. Download [kibana-6.3.0](https://www.elastic.co/products/kibana) and extract anywhere memorable.


And that's it; you're done!

### Setting Up

We'll first have to start up our two servers (ElasticSearch and Kibana). Think of these as background programs that run and provide us with the functionality that we need. Navigate to where you extracted the two downloads, and run them in command line.

```
cd \Documents\Accenture\automatic-traffic-assignment\elasticsearch-6.3.0\
.\elasticsearch
```

And

```
cd \Documents\Accenture\automatic-traffic-assignment\kibana-6.3.0-windows-x86_64\
.\kibana
```

You can check their up status (after they've finished spewing out debug text in the console window) in your web browser by navigating to their served ports

```
http://localhost:9200/
```

And

```
http://localhost:5601/
```

Now that both those things are up, go back to this git folder and run the Python script using the command line.
Find inside the script detailed comments about what to expect.

```
python fetchData.py
python sendAssignment.py
```

And you should be good!

## Deployment

Details of the test instance used for the Bootcamp have been removed - you'll have to replace these in the `TODO` sections yourself.
Additionally, the test data in /data is mostly unused. Change/remove these at will.

## Contributing

Send me a message or just chat to me :)

### Limitations/Future work

- Refactor code into functions
- Schedule the running of the code
- More efficient searching algorithm when finding incidents with no assignees
- Carefully tailored assignment algorithm taking into account priority, worker training, etc
- Increasing the security of the script by adding in SSL certificate verification
- Add ML cos everyone loves that

## Troubleshooting

- *Awaiting feedback*

## Authors

- **Charling Li** - [charlingli](https://github.com/charlingli)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

- Team 5 for the banter
- Shub and George for sick mentorship
