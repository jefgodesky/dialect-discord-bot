from typing import List
from discord import (
    app_commands,
    Client,
    File,
    Intents,
    Interaction,
    Member,
    Object,
    User,
)
import glob
from dotenv import load_dotenv
import os

from gamemanager.classes import GameManager
from player.classes import Player

languages = []

load_dotenv()
intents = Intents.default()
intents.message_content = True

token = os.getenv("DISCORD_BOT_TOKEN")
server = os.getenv("DISCORD_GUILD_ID")
client = Client(intents=intents)
tree = app_commands.CommandTree(client)
games = GameManager()


def oxford_list(items: List[any]) -> str:
    strings = [str(string) for string in items]
    if not items:
        return ""
    if len(items) == 1:
        return strings[0]
    if len(items) == 2:
        return " and ".join(strings)
    return ", ".join(strings[:-1]) + ", and " + strings[-1]


def unpack_interaction(interaction: Interaction) -> tuple[int, int, User | Member]:
    guild_id = interaction.guild_id
    channel_id = interaction.channel_id
    user = interaction.user
    return guild_id, channel_id, user


async def dm(member: Member, msg: str) -> None:
    await member.send(msg)


async def no_game(interaction: Interaction) -> None:
    response = (
        "There isn’t a game in this channel to join — or at least, there isn’t one _yet_. Use the "
        "**/start** slash command to start one."
    )
    await interaction.response.send_message(response, ephemeral=True)


async def send_hand(member: Member, guild_id: int, channel_id: int) -> None:
    game = games.get(guild_id, channel_id)
    index = game.get_player_index(member)
    if index is None:
        return

    player = game.players[index]
    if len(player.cards) == 0:
        return

    images = [File(f"cards/{card.filename}") for card in player.cards]
    labels = ", ".join([card.label for card in player.cards])
    channel_url = f"https://discord.com/channels/{guild_id}/{channel_id}"
    await member.send(f"{channel_url} Your current hand: {labels}", files=images)


async def card_autocomplete(
    interaction: Interaction, current: str
) -> List[app_commands.Choice[str]]:
    guild_id, channel_id, user = unpack_interaction(interaction)
    game = games.get(guild_id, channel_id)
    if game is None:
        return []

    accounts = [player.account for player in game.players]
    if user not in accounts:
        return []

    index = game.get_player_index(user)
    return [
        app_commands.Choice(name=card.label, value=card.label)
        for card in game.players[index].cards
        if current.lower() in card.label.lower()
    ]


async def language_autocomplete(
    interaction: Interaction, current: str
) -> List[app_commands.Choice[str]]:
    return [
        app_commands.Choice(name=lang, value=lang)
        for lang in languages
        if current.lower() in lang.lower()
    ]


@tree.command(
    name="start", description="Start a new game of Dialect.", guild=Object(id=server)
)
@app_commands.autocomplete(lang=language_autocomplete)
async def start(interaction: Interaction, lang: str) -> None:
    guild_id, channel_id, user = unpack_interaction(interaction)
    game = games.get(guild_id, channel_id)
    if game is not None:
        descriptions = {
            "voice": "It’s currently in the character creation phase, so anyone can use the **/join** slash command "
            "in this channel to join.",
            "age1": "It’s currently in the first age.",
            "age2": "It’s currently in the second age.",
            "age3": "It’s currently in the third age.",
            "legacy": "It’s currently in the legacy phase.",
        }
        description = descriptions[game.phase]
        response = f"There’s already a game in this channel. {description}"
        await interaction.response.send_message(response)
    elif games.create(guild_id, channel_id, user, base_language=lang):
        response = (
            "**Let’s play Dialect!** To join, use the **/join** slash command. New players can only join "
            "during the character creation phase."
        )
        await interaction.response.send_message(response)
        await send_hand(user, guild_id, channel_id)
    else:
        response = "**Something went wrong.** I couldn’t start a new game for you, and I’m not really sure why."
        await interaction.response.send_message(response)


@tree.command(
    name="join", description="Join a game of Dialect.", guild=Object(id=server)
)
async def join(interaction: Interaction) -> None:
    guild_id, channel_id, user = unpack_interaction(interaction)
    game = games.get(guild_id, channel_id)
    if game is None:
        await no_game(interaction)
    elif game.phase != "voice":
        phases = {
            "age1": "first age",
            "age2": "second age",
            "age3": "third age",
            "legacy": "legacy phase",
        }
        response = (
            f"Sorry, the game in this channel is already in the {phases[game.phase]}, so it’s too late to join "
            f"this one."
        )
        await interaction.response.send_message(response)
    elif user in [player.account for player in game.players]:
        await interaction.response.send_message("You’re already in.")
    else:
        game.join(Player(user))
        response = f"Welcome to the game, {user.mention}! Check your DM’s for your starting hand."
        await interaction.response.send_message(response)
        await send_hand(user, guild_id, channel_id)


@tree.command(
    name="status",
    description="Check where the game in this channel is right now.",
    guild=Object(id=server),
)
async def status(interaction: Interaction) -> None:
    guild_id, channel_id, _ = unpack_interaction(interaction)
    game = games.get(guild_id, channel_id)
    if game is None:
        await no_game(interaction)
        return

    if game.phase == "voice":
        response = (
            "We’re in the character creation phase right now, so you can still join by using the **/join** "
            "slash command."
        )
    else:
        phases = {
            "age1": "first age",
            "age2": "second age",
            "age3": "third age",
            "legacy": "legacy phase",
        }
        response = f"We’re in the {phases[game.phase]} right now."

        mention_gone = [player.account.mention for player, _ in game.plays]
        mention_left = [player.account.mention for player in game.players_left]
        mention_gone_oxford = oxford_list(mention_gone)
        mention_left_oxford = oxford_list(mention_left)
        gone_verb = (
            "has made a play" if len(mention_gone) < 2 else "have each made plays"
        )
        left_verb = (
            "is waiting for their turn"
            if len(mention_left) < 2
            else "are waiting for their turns"
        )
        gone_null = "No one has made a play yet in this round."
        left_null = "Everyone has already made a play in this round."
        gone = (
            gone_null
            if len(mention_gone) < 1
            else f"{mention_gone_oxford} {gone_verb}."
        )
        left = (
            left_null
            if len(mention_left) < 1
            else f"{mention_left_oxford} {left_verb}."
        )
        response = f"{response} {gone} {left}"

    await interaction.response.send_message(response)


@tree.command(
    name="words", description="Generate new random words.", guild=Object(id=server)
)
@app_commands.describe(num_words="The number of new words to generate.")
@app_commands.describe(num_syllables="The number of syllables these words should have.")
async def words(interaction: Interaction, num_words: int, num_syllables: int) -> None:
    guild_id, channel_id, user = unpack_interaction(interaction)
    game = games.get(guild_id, channel_id)
    if game is None:
        await no_game(interaction)
        return

    if game.base_language is None:
        await interaction.response.send_message(
            "Sorry, this game does not have a base language set, so I can’t "
            "generate new words for you.",
            ephemeral=True,
        )
        return

    words = game.base_language.generate_new_words(
        num_words, num_syllables=num_syllables
    )
    intro_many = f"Here are {num_words} {num_syllables}-syllable words that fit "
    intro_single = f"Here is a {num_syllables}-syllable word that fits "
    intro_head = intro_single if num_words == 1 else intro_many
    intro = f"{intro_head} your base language’s phonotactic and phonological rules."
    lines = [intro] + words
    await interaction.response.send_message("\n".join(lines), ephemeral=True)


@tree.command(
    name="play", description="Play a card from your hand.", guild=Object(id=server)
)
@app_commands.describe(card="The card you want to play.")
@app_commands.autocomplete(card=card_autocomplete)
async def play(interaction: Interaction, card: str) -> None:
    guild_id, channel_id, user = unpack_interaction(interaction)
    game = games.get(guild_id, channel_id)
    if game is None:
        await no_game(interaction)
        return

    accounts = [player.account for player in game.players]
    if user not in accounts:
        can_join = "You have to join the game before you can play. Use the **/join** slash command to join!"
        cannot_join = "Sorry, this game is already underway. It’s too late to join."
        response = can_join if game.phase == "voice" else cannot_join
        await interaction.response.send_message(response, ephemeral=True)
        return

    card_instance = game.play(user, card)
    response = f"{user.mention} plays {card}."
    images = [File(f"cards/{card_instance.filename}")]
    await interaction.response.send_message(response, files=images)
    await send_hand(user, guild_id, channel_id)


@tree.command(name="end", description="End the game.", guild=Object(id=server))
async def end(interaction: Interaction) -> None:
    guild_id, channel_id, _ = unpack_interaction(interaction)
    game = games.get(guild_id, channel_id)
    if game is None:
        await no_game(interaction)
        return

    legacy = game.phase == "legacy"
    games.end(guild_id, channel_id)

    if legacy:
        epilogue = (
            "And so ends the story of the Isolation. Take a few moments to reflect on the experience and talk "
            "openly about the game and the story you’ve told together."
        )
        questions = """

* How are you feeling?
* Did anything unexpected happen?
* Which parts of the language are going to stick with you?
* How will you remember this story?

"""
        coda = "**You are the sole speakers of your dialect now.**"
        await interaction.response.send_message(epilogue + questions + coda)
    else:
        response = (
            "**Game Over!** We weren’t able to play through the entire story of the Isolation. What has become "
            "of them? Like so many other communities throughout time, their fate will remain a mystery that "
            "we will never know."
        )
        await interaction.response.send_message(response)


@client.event
async def on_ready():
    global languages
    language_files = glob.glob("languages/*.yaml")
    languages = [os.path.splitext(os.path.basename(file))[0] for file in language_files]
    await tree.sync(guild=Object(id=server))
    print(f"Logged in as {client.user}")


client.run(token)
