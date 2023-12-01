.. PyZora documentation master file, created by
   sphinx-quickstart on Thu Nov 30 22:03:29 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image::_static/pyzora.svg

Welcome to PyZora's documentation!
==================================

PyZora is a library meant for use with secrets from The Legend of Zelda: Oracle of Seasons/Ages (referred to as the Oracles from now on and throughout the docs for convenience).

It provides easy-to-use classes for each secret type, and allows the user to read and
write any type of secret to a string for use with the games.

OK, but... what's a "secret"?
==================================

A secret is a password the Oracles use to transfer data. No matter the type, you need to have completed at least one game to use secrets.

The data differs between each secret type, and there are three different types :

- **Game secrets** : these secrets are the most important ones out of them all. They allow players to start Linked Games. Linked Games continue the story from the completed game to the other one, and allow access to the true final boss (Ganon) and ending, as well as some additional events which differ depending on the game you completed first.
- **Ring secrets** : these ones are game-independent. You can use them to transfer your Magic Rings obtained in one game to the other one. To start using ring secrets, you need to talk to Red Snake in Vasu's shop in the non-complete file once. You can regenerate ring secrets at will if you obtained some more rings, and the ring list in the secret will not overwrite the potential rings you obtained in the destination game (meaning rings transferred through secrets add to your ring list).
- **Memory secrets** : these ones allow players to get items and buffs inaccessible during normal games. Memory secrets are obtained by talking to a specific NPC in one game which only appears after you reach a certain point in the story. You will then have to repeat the secret to a specific NPC in the other game, which will then give you something in return (you might have to play a minigame to get it). Most of the time, it's another memory secret you'll have to carry back to the original secret holder to receive your reward, but in some cases, you might get a ring you have to appraise (and transfer back to the non-complete game using a Ring Secret).

Quick Start
==================================

Nothing is more simple.
Just type ``pip install pyzora`` (or ``python3 -m pip install pyzora``) in your terminal to install the library in Python.
Then you'll be one ``import pyzora`` away from the ability to use it!
