# TextAnalytics

The groupwork of CS7IS4 TEXT ANALYTICS.
By Group 3.

## Data Collection

## Preprocessing

**NEED TO INSTALL BY FOLLWING THE README IN THEIR REPO**

Preprocessing using tool: https://github.com/vasisouv/tweets-preprocessor

## Analyzing Methods

### Comparing Liguistic Features

#### Word Counting

- words
  - a plenty of lexicons to choose: https://web.stanford.edu/~jurafsky/slp3/slides/21_SentLex.pdf
  - sentiwordnet can be a good tool
    - see http://www.nltk.org/howto/sentiwordnet.html
- count slang on the internet
  - https://saveti.kombib.rs/twerminology-twitter-slang-words-and-abbreviations
  - https://mashable.com/2013/07/19/twitter-lingo-guide/?europe=true
- count emojis / emoticons
  - https://github.com/SEntiMoji/SEntiMoji

#### Others

- length of tweets/retweets
  - it's like other non-linguistic features

### Comparing Non-Linguistic Features

- the amount of tweets & retweets & replies
- the frecency of tweets/retweets
- the number of followers & following

About how to calculate and illustrate the numbers.

See the chapter `Co-Authors, References and Reported Experiments` in [Linguistic_Traces_of_a_Scientific_Fraud-_The Case_of_Diederik_Stapel](./references/Linguistic_Traces_of_a_Scientific_Fraud-_The%20Case_of_Diederik_Stapel.pdf)

### ~~The Big Five & Dark Triad Personalities~~

See [Cyberbullying_detection_on_twitter_using_Big_Five_and_Dark_Triad_features](./references/Cyberbullying_detection_on_twitter_using_Big_Five_and_Dark_Triad_features.pdf)

The key method is to use IBM's free API.
See [IBM Personality Insights](https://cloud.ibm.com/apidocs/personality-insights)

Or we can find other approach using lexicons availble on the internet.

There is relationships given in the paper.
Once the Big 5 is out, the Dark Triad personalities can be infered with mappings given in the paper.

### NRC Word-Emotion Association Lexicon (EmoLex)

check this: https://github.com/dropofwill/py-lex

use `py-lex` with lexicons (also with some papers) from here: http://saifmohammad.com/WebPages/NRC-Emotion-Lexicon.htm

## Visualization

## Discussion

## About

The paper should follow the instructions provided here (approved by professor):

https://sites.google.com/view/iwcs2019/instructions-for-authors
