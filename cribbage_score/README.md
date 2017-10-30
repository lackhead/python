# Cribbage Hand Scoring
I found this one on Reddit's [/r/dailyprogrammer](http://www.reddit.com/r/dailyprogrammer): [Cribbage Hand Scorer](https://www.reddit.com/r/dailyprogrammer/comments/75p1cs/20171011_challenge_335_intermediate_scoring_a/).
The idea is to create a program to calculate the score of a Cribbage hand (see the (Rules of Cribbage)[http://en.wikipedia.org/wiki/Rules_of_cribbage]).

There are two files here:

  * cribbage_score.py - the code itself. I created two classes, Card and CribbageHand, and used `@property` tags for the runs, score, etc.
  * cribbage_score_test.py - unit tests for the code
