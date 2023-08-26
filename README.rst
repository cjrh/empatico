empatico
========

Emotion detection microservice based on natural language inference

.. raw:: html

    <p align="center" width="100%">
        <img width="100%" src="https://raw.githubusercontent.com/cjrh/empatico/main/clown.jpg">
    </p>


.. contents:: Table of Contents


Demo
----

Launch the model (dev mode, auto-reloading):

.. code-block:: bash

    $ python3 -m venv .venv
    $ source ./venv/bin/activate
    (.venv) $ pip install -r requirements.txt
    (.venv) $ pip install flit
    (.venv) $ flit install --symlink
    (.venv) $ uvicorn empatico:app --reload
    INFO:     Will watch for changes in these directories: ['/home/caleb/Documents/repos/empatico']
    INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
    INFO:     Started reloader process [303534] using watchgod

There are several classifications already set up. You just need to provide the
text:

.. code-block:: bash

    $ curl --request POST \
        --header "Content-Type: application/json" \
        --data '{"text": "I love when you speak to me rudely"}' \
        http://127.0.0.1:8000/emotions | jq
    [
      {
        "label": "mixed",
        "score": 92.90633797645569
      },
      {
        "label": "anger",
        "score": 95.19177079200745
      },
      {
        "label": "sarcastic",
        "score": 97.97245264053345
      }
    ]

Wow, a label for sarcasm! Here's another one:

.. code-block:: bash

    $ curl --request POST \
        --header "Content-Type: application/json" \
        --data '{"text": "Best insurance company in europe what a joke"}' \
        http://127.0.0.1:8000/emotions | jq
    [
      {
        "label": "negative",
        "score": 99.07029867172241
      },
      {
        "label": "mixed",
        "score": 92.89084672927856
      },
      {
        "label": "anger",
        "score": 99.08776879310608
      },
      {
        "label": "sadness",
        "score": 92.85369515419006
      },
      {
        "label": "bitter",
        "score": 99.18588995933533
      },
      {
        "label": "sarcastic",
        "score": 99.7484564781189
      },
      {
        "label": "fear",
        "score": 89.00700807571411
      },
      {
        "label": "disgust",
        "score": 99.62377548217773
      },
      {
        "label": "surprise",
        "score": 99.7963547706604
      }
    ]

Again sarcasm is detected (99.7% probability), with a few other comorbid emotions. Another test of 
the sarcasm detector:

.. code-block:: bash

    $ curl --request POST \
        --header "Content-Type: application/json" \
        --data '{"text": "yes go ahead and sue me, I''m sure that will work out fine for you"}' \
        http://127.0.0.1:8000/emotions | jq
    [
      {
        "label": "sarcastic",
        "score": 96.60570025444031
      },
      {
        "label": "helpful",
        "score": 87.13959455490112
      },
      {
        "label": "trust",
        "score": 89.57158923149109
      }
    ]

It isn't always negative:

.. code-block:: bash

    $ curl --request POST \
        --header "Content-Type: application/json" \
        --data '{"text": "Staff were wonderful and made the trip that much more pleasant. Thank you!"}' \
        http://127.0.0.1:8000/emotions | jq
    [
      {
        "label": "positive",
        "score": 94.82141733169556
      },
      {
        "label": "satisfied",
        "score": 95.2349305152893
      },
      {
        "label": "helpful",
        "score": 95.06783485412598
      },
      {
        "label": "joy",
        "score": 95.37110924720764
      }
    ]

By default, a rich array of emotional labels is provided:

.. code-block:: bash

    $ curl --request POST \
        --header "Content-Type: application/json" \
        --data '{"text": "The only way you could have done any worse is lose my package completely."}' \
        http://127.0.0.1:8000/emotions | jq
    [
      {
        "label": "negative",
        "score": 98.56123924255371
      },
      {
        "label": "anger",
        "score": 97.950679063797
      },
      {
        "label": "sadness",
        "score": 89.63329792022705
      },
      {
        "label": "disappointment",
        "score": 87.91854977607727
      },
      {
        "label": "bitter",
        "score": 90.94756841659546
      },
      {
        "label": "fear",
        "score": 90.21917581558228
      },
      {
        "label": "disgust",
        "score": 90.52256941795349
      },
      {
        "label": "surprise",
        "score": 83.91632437705994
      }
    ]

Default labels (and reporting threshold)
----------------------------------------

You can also control the cutoff threshold for reporting. Here we set it to zero,
which disables the filter. This shows all the default hypotheses (which are 
expressed as labels):

.. code-block:: bash

    $ curl --request POST \
        --header "Content-Type: application/json" \
        --data '{"text": "The kids were so looking forward to the trip but the rain washed away all our plans.", \
            "report_threshold": 0.0}' \
        http://127.0.0.1:8000/emotions | jq
    [
      {
        "label": "positive",
        "score": 0.7067840080708265
      },
      {
        "label": "negative",
        "score": 98.16489219665527
      },
      {
        "label": "mixed",
        "score": 98.80892634391785
      },
      {
        "label": "satisfied",
        "score": 0.7183659821748734
      },
      {
        "label": "neutral1",
        "score": 0.5342578981071711
      },
      {
        "label": "neutral2",
        "score": 0.034320083796046674
      },
      {
        "label": "neutral3",
        "score": 4.02584969997406
      },
      {
        "label": "factual",
        "score": 6.705068796873093
      },
      {
        "label": "anger",
        "score": 33.71554911136627
      },
      {
        "label": "sadness",
        "score": 98.14655780792236
      },
      {
        "label": "disappointment",
        "score": 99.36606287956238
      },
      {
        "label": "bitter",
        "score": 61.47879958152771
      },
      {
        "label": "sarcastic",
        "score": 31.848391890525818
      },
      {
        "label": "helpful",
        "score": 71.62957191467285
      },
      {
        "label": "fear",
        "score": 17.39620268344879
      },
      {
        "label": "disgust",
        "score": 4.311040416359901
      },
      {
        "label": "surprise",
        "score": 90.2463436126709
      },
      {
        "label": "hope",
        "score": 0.21583051420748234
      },
      {
        "label": "trust",
        "score": 37.46950924396515
      },
      {
        "label": "joy",
        "score": 0.47363536432385445
      }
    ]

It is really interesting that while the "overall" positive score is 0.7% and
the "overall" negative score is 98%, we do still see a "mixed" score
of 98.8%. This can be interpreted as "while there were both positive and
negative sentiments expressed, the negative outweighs the positive".

Customizable hypotheses
-----------------------

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

Background
----------

The underlying technique for using natural language inference for classification
was described by Joe Davison here: 

https://joeddav.github.io/blog/2020/05/29/ZSL.html

The underlying idea is that, instead of using a model specifically trained for
binary, ternary, or n-ary classification, we might instead try to use a model
designed for *inference* and test whether a particular hypothesis is supported
by a piece of text. This dramatically expands the scope of possible labels 
to apply to a given piece of text, and you don't need the model to have been
specifally trained for those labels either.

The model being used in the code is 
`facebook/bart-large-mnli <https://huggingface.co/facebook/bart-large-mnli>`_.

Running the server in dev
-------------------------

.. code-block:: bash

    $ uvicorn empatico:app --reload

