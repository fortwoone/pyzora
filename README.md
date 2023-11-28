# pyzora
## Python decoder library for Zelda OoS/OoA secrets

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
