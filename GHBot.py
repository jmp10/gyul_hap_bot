import os
import discord
from io import BytesIO
from GHImages import *
from PIL import ImageDraw, ImageFont
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

bot = commands.Bot(command_prefix="!")

tiles = generate_tiles()
test_tiles = [tile for tile in tiles.values() if tile.shape == "C"]  # list of all the circle tiles, for testing
active_game = False
hap_font = ImageFont.truetype("RixVitaB.ttf", 60)
min_solutions = 2


def discord_image(pic):  # takes in Pillow image, returns Discord-compatible image file
    arr = BytesIO()
    pic.save(arr, "PNG")
    arr.seek(0)
    file1 = discord.File(fp=arr, filename="image.png")
    return file1


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f"{bot.user} is connected to the following guilds:\n"
        f"{guild.name} (id: {guild.id})"
    )


# Generate a new board to play.
@bot.command(name="new",
             help="Generate a new board. Cannot start a new board until the previous one is finished.")
@commands.guild_only()
async def start_game(ctx):
    global board, active_game, solutions, found_haps, board_image
    if active_game:  # if there's already a game in progress, don't let them start one
        await ctx.send(f"{ctx.message.author.mention} Please finish the previous board before starting a new one!")
    else:
        active_game = True
        found_haps = []
        solutions = []
        while len(solutions) < min_solutions:  # generate a new board if there's too few solutions
            board = generate_board(tiles)
            # board = test_tiles  # for testing
            solutions = solve_board_numbers(board)

        board_image = build_image(board, False)
        board_image_copy = board_image.copy()
        board_image_copy = board_image_copy.resize((417, 300))

        await ctx.send(file=discord_image(board_image_copy))
        await ctx.send(f"There are **{len(solutions)} haps** to find on this board. Good luck!")


# Submit a guess.
@bot.command(name="hap",
             help="Submit a guess, either in the format !hap 123 or !hap 1,2,3.")
@commands.guild_only()
async def hap_sent(ctx, hap_guess: str):
    global active_game, solutions, found_haps, board_image
    hap_guess = hap_guess.replace(",", "")  # get rid of commas
    hap_guess = "".join(sorted(hap_guess))  # sort the numbers in ascending order
    sender = ctx.message.author.mention

    if not active_game:  # if there's no active board
        await ctx.send(f"{sender} The last game has ended! Use `!new` to start another one.")
    elif not hap_guess.isnumeric() or len(hap_guess) != 3:  # if the hap's format is invalid
        await ctx.send(f"{sender} Please submit your guess in the format `!hap 123` or `!hap 1,2,3`.")
    elif hap_guess in found_haps:  # if the hap was found already
        await ctx.send(f"{sender} That hap has already been found!")
    elif hap_guess not in solutions:  # if the hap is not correct
        await ctx.send(f"{sender} That is not a valid hap.")
    elif hap_guess in solutions:  # if the hap is correct
        solutions.remove(hap_guess)
        solutions_left = len(solutions)
        found_haps += [hap_guess]

        hap_text = ImageDraw.Draw(board_image)
        top = 35 + 71 * (len(found_haps) - 1)
        hap_text.text((995, top), " ".join(hap_guess), fill="black", font=hap_font)

        board_image_copy = board_image.copy()
        board_image_copy = board_image_copy.resize((417, 300))
        await ctx.send(file=discord_image(board_image_copy))

        if solutions_left > 0:
            if solutions_left == 1:
                await ctx.send(f"{sender} Well done, you found a hap! Just **1 hap** left to find!")
            else:
                await ctx.send(f"{sender} Well done, you found a hap! Just **{solutions_left} haps** left to find!")
        else:
            active_game = False
            await ctx.send(f"{sender} Congratulations, you found the last hap! :tada: "
                           f"Type `!new` to start a new board.")


# Send the rules of the game.
@bot.command(name="howtoplay",
             help="See the rules of Gyul Hap.")
@commands.guild_only()
async def send_rules(ctx):
    await ctx.send(f"{ctx.message.author.mention} Gyul Hap is played with 27 tiles, each of which has one of three "
                   f"background colors (black, grey, or white), one of three shapes (circle, triangle, or square), and "
                   f"one of three shape colors (red, yellow, or blue). The object of the game is to find haps—sets of "
                   f"three tiles where each of the characteristics above is either all the same across the three "
                   f"tiles, or all different across them. For example, three triangles that are each different colors "
                   f"and each have different background colors would be a hap, but if two of the background colors "
                   f"were the same, it would not be hap.")


bot.run(TOKEN)
