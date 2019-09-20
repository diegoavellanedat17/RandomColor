# RandomColor
The idea of this device "RANDOM COLOR" is to make a game for when you are with your friends. "RANDOM COLOR" works with Alexa and has the following functionalities:
- Assign a random color to each player
- Show which colors are at stake
- Choose a random color among the participants
- Finish the game

Basically there is a group of players, and each one will ask Alexa, "Alexa, what color do you want to assign me", she will choose a color and will light it on the device, (This will be the participant's color during the game). Thus each of the participants.
Once all the participants have an assigned color if we ask "Alexa, what colors are at stake", she will answer the corresponding colors to the participants that are in play.
With the command "Alexa, random color" she will randomly choose one of the participants who must complete a penance or answer a question.
Next I will teach you how to make the Device "RANDOM COLOR"
We are going to divide the development into two stages, the first one will be the Hardware and Firmware and the next one will be the Alexa Skill for operation.
The module used is an ESP32 which is connected to an MQTT Broker, subscribed to a RandomColor topic, the message that will arrive will correspond to the color which should illuminate the "RANDOM COLOR".
Initially to be able to connect the device you must be able to access the Broker, in this case https://cloudmqtt.com is used, they have very good plans and even some free when there is not much data traffic. When we activate our broker, we will find our user, password, host_server and port. (We will need this information later)
For example, if you want RANDOM COLOR alum in blue, the message will be as follows:

topic="RandomColor"
payload="BLUE"

Once this message is received, in NeoPixel Ring it will illuminate the corresponding color.

For the development of the Alexa code, it is in the repository, it is necessary to create an AWS account and program with lambda, for the persistence of the files in the game it is important to have a Bucket in Amazon S3 since the temporary files are deleted after a while and the game information is lost, I invite you to my repository where you will find more information on both Firmware and Lambda code.
