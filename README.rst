empatico
========

Emotion detection microservice based on natural language inference

Demo
----

There are several classifications already set up. You just need to provide the
text:

.. code-block:: bash

    $ curl --request POST --header "Content-Type: application/json" \
        --data '{"text": "I hate this so much"}' \
        http://127.0.0.1:8000/emotions | jq
    [
      {
        "label": "negative",
        "score": 99.83717799186707
      },
      {
        "label": "mixed",
        "score": 88.92676830291748
      },
      {
        "label": "anger",
        "score": 99.70097541809082
      },
      {
        "label": "sadness",
        "score": 98.02180528640747
      },
      {
        "label": "disappointment",
        "score": 98.87089133262634
      },
      {
        "label": "bitter",
        "score": 99.58844780921936
      },
      {
        "label": "fear",
        "score": 86.27639412879944
      },
      {
        "label": "disgust",
        "score": 99.8855471611023
      }
    ]

You can also provide your own hypotheses, which means you can generalise this
to many difference kinds of classifications:

.. code-block:: bash

    $ curl --request POST --header "Content-Type: application/json" \
        --data '{"text": "The democrats are ruining this country", \
        "report_threshold": 0.0, \
        "hypotheses": {"politics": "this text is about politics", \
        "sport": "this text is about sport"}}' http://127.0.0.1:8000/emotions | jq
    [
      {
        "label": "politics",
        "score": 97.42230772972107
      },
      {
        "label": "sport",
        "score": 0.16288807382807136
      }
    ]
    ~
    $ curl --request POST --header "Content-Type: application/json" \
        --data '{"text": "The tour de france was exhilarating to watch", \
        "report_threshold": 0.0, \
        "hypotheses": {"politics": "this text is about politics", \
        "sport": "this text is about sport"}}' http://127.0.0.1:8000/emotions | jq
    [
      {
        "label": "politics",
        "score": 0.4232536070048809
      },
      {
        "label": "sport",
        "score": 97.9870855808258
      }
    ]


Running the server in dev
-------------------------

.. code-block:: bash

    $ uvicorn empatico:app --reload

