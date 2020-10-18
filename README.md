# gyul_hap_bot
A Discord bot to play the game Gyul Hap, a variant of the board game Set from the game show <i><a href="https://en.wikipedia.org/wiki/The_Genius_(TV_series)">The Genius</a></i>.

## Creating a .env file

Note that to use this bot, you must create a .env file containing the token of the Discord bot you make with this code. To do so, follow the instructions <a href="https://stackoverflow.com/questions/63530888/how-would-i-go-about-creating-an-env-file-for-my-discord-bot-token">outlined here</a>. Specifically:

<ul>
  <li>Install dotenv using pip, with the command <code>pip install python-dotenv</code>.</li>
  <li>Create a file named .env in the same directory as the rest of the project.</li>
  <li>Copy the text below into the file, replacing "your_token" with the bot token and "your_server" with the name of the server you're using the bot in.</li>
</ul>

<pre>
DISCORD_TOKEN=your_token
DISCORD_GUILD=your_server
</pre>
