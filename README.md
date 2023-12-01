# pyzora
## Python decoder library for Zelda OoS/OoA secrets

[![Documentation Status](https://readthedocs.org/projects/pyzora/badge/?version=latest)](https://pyzora.readthedocs.io/en/latest/?badge=latest)

This library has been inspired both by Paulygon's password generator for
The Legend of Zelda: Oracle of Seasons/Ages (referred to as the Oracle games from now on) and Amy Nagle 
(aka [kabili207](https://github.com/kabili207))'s [zora-sharp](https://github.com/kabili207/zora-sharp) 
library for C#. It can handle all three types of secrets in the games.

## But... what's a secret?

Let me explain. A secret is a password the Oracle games use to transfer data.
There are three types of secrets : 
<ul>
    <li>Game secrets : they allow a player who has finished 
    one of the two games to continue the story in the other game.</li>
    <li>Ring secrets : once one of the two games is completed, Red Snake in the completed file
will generate this kind of secret. It allows the player to transfer all their rings from one game
to the other (for this to work, you need to talk to Red Snake in the non-completed file at least once).</li>
    <li>Memory secrets : during a linked game, exclusive NPCs will spawn on the map. Some of these
NPCs can be interacted with to get a short secret to transfer to another NPC in the
completed file. The latter NPC will then give the player another code to transfer back to
the non-finished file to carry his bonus over. The player might be required to play a minigame
before getting the return secret.</li>
</ul>

As you can see, secrets are pretty vital if you want to have the full experience in
The Legend of Zelda: Oracle of Ages/Seasons. (which is why this library exists, duh).

## What does pyzora provide?

<ul>
    <li>One class per secret type, with its own attributes and uses</li>
    <li>Reading and writing secrets of any type in both available game regions (Japan and US. Note that PAL releases use the same encoding as US cartridges)</li>
    <li>Easy to use</li>
</ul>

## Okay, but how am I supposed to install this?

Don't worry! It's very simple! You just need to do the good old `pip install pyzora`!

If you want to manually install the library with the source code, follow the steps below:

<ol>
    <li><a href="https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository">Clone</a> the repository.</li>
    <li>Install <a href="https://python.org/downloads">Python</a> 3.10 or above.</li>
    <li>Run this command to get the dependencies :</li>
</ol>

```bash
python3 -m pip install -r requirements.txt
```

<ol start="4">
    <li>You're good to go!</li>
</ol>

## I noticed a bug or want to contribute!

Found a bug? Don't panic! Simply head towards the [Issues](https://github.com/fortwoone/pyzora/issues) section in this repository and describe your problem! A solution will be worked on as soon as possible afterwards.

Want to contribute? You can start by forking the project. Once you're done, <a href="https://github.com/fortwoone/pyzora/pulls">open a pull request</a> in the repository, and it'll be reviewed as soon as possible!
