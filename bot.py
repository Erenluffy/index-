
#!/usr/bin/env python3
import logging
import re
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Use ONLY ONE bot token - choose either:
BOT_TOKEN = os.getenv("BOT_TOKEN", "7859842889:AAFSn3HZFBRe48MR9LnndoVrX4WCQeo2Ulg")  # python-telegram-bot
# OR
# BOT_TOKEN = os.getenv("BOT_TOKEN", "8156690888:AAEMBoNHIUc5bNEqsICBk2X66WMhafsHeJg")  # Pyrogram

# Your anime index
anime_index = [
    # A
    "A Condition Called Love", "A Couple of Cuckoos", "A Salad Bowl of Eccentrics", 
    "A Silent Voice", "Accel World", "Afro Samurai", "Aharen Is Indecipherable", 
    "Akame ga Kill!", "Alya Sometimes Hides Her Feelings in Russian", "Angel Beats!", 
    "Anohana The Flower We Saw That Day", "Another", "Aoashi", "Arcane", 
    "Assassination Classroom", "Attack On Titan",

    # B
    "Baccano", "Banana Fish", "Basilisk", "Berserk", "Black Clover", "Bleach", 
    "Blue Lock", "Blue Spring Ride", "Bungou Stray Dogs", "Buddy Daddies", "Bunny Girl Senpai",

    # C
    "Call of The Night", "Castlevania", "Chainsaw Man", "Charlotte", "Clannad", 
    "Classroom of the Elite", "Claymore", "Code Geass Lelouch of the Rebellion", "Cowboy Bebop",

    # D
    "Darling in the Franxx", "Don't Toy With Me, Miss Nagatoro", "DanDaDan", 
    "Deadman Wonderland", "Death Note", "Death Parade", "Demon Slayer", 
    "Devilman Crybaby", "Domestic Girlfriend", "Dorohedoro", "Dororo", "Dr Stone",

    # E
    "Eden of the East", "Eighty Six 86", "Elfen Lied", "Eminence in Shadow", 
    "Engage Kiss", "Erased", "Ergo Proxy",

    # F
    "Fire Force", "Free", "Frieren Beyond Journey's End", "From Up on Poppy Hill", 
    "From the New World", "Fruits Basket", "Fullmetal Alchemist", "Future Diary",

    # G
    "Gangsta", "Golden Boy", "Gamers", "Garouden The Way of the Lone Wolf", 
    "Genius Princes Guide to Raising a Nation Out of Debt", "Girlfriend Girlfriend", 
    "Given", "Gleipnir", "Go Go Loser Ranger", "God Eater", "Golden Time", 
    "Good Night World", "Gosick", "Grand Blue Dreaming", "Grave of the Fireflies", 
    "Great Pretender", "Great Teacher Onizuka", "Guilty Crown", "Gurren Lagann",

    # H
    "Haikyuu", "Handa kun", "Heavenly Delusion", "Hells Paradise", "Hellsing", 
    "High School DxD", "High School of Dead", "Hokkaido Gals Are Super Adorable", 
    "Horimiya", "Hunter X Hunter",

    # I
    "I Got a Cheat Skill in Another World", "I Parry Everything", "I Shall Survive Using Potions", 
    "I am in Love with the Villainess", "I have Been Killing Slimes for 300 Years", 
    "If It's for My Daughter I'd Even Defeat a Demon Lord", "Insomniacs After School",

    # J
    "Jibaku Shounen Hanako-kun", "JoJo's Bizarre Adventure", "Joker Game", 
    "Joran The Princess of Snow and Blood", "Jormungand", "Joshiraku", "Jujutsu Kaisen", 
    "Junji Ito Collection", "Junketsu No Maria",

    # K
    "Kabaneri of the Iron Fortress", "Kaguya-sama: Love is War", "Kaiju No 8", "Kakegurui", 
    "Kakushigoto", "KamiKatsu Working for God in a Godless World", "Katanagatari", "Keijo!", 
    "Kengan Ashura", "Kenichi The Mightiest Disciple", "Kids on the Slope", "Kiki's Delivery Service", 
    "Kill la Kill", "Kingdoms of Ruin", "Kiss Him Not Me", "Komi Can't Communicate", 
    "Konosuba God's blessing on this wonderful world",

    # L
    "Last Dungeon", "Laughing Under the Clouds", "Level 1 Demon Lord and One Room Hero", 
    "Liar Liar", "Link Click", "Lookism", "Lord of Mysteries", "Love Flops", "Love Hina", 
    "Love Election and Chocolate", "Lovely Complex", "Lycoris Recoil",

    # M
    "Made in Abyss", "Magical Sempai", "Maid Sama!", "Makeine Too Many Losing Heroines", 
    "Maken Ki! Battling Venus", "Maquia When the Promised Flower Blooms", 
    "Mashle Magic And Muscles", "Mf Ghost", "More than a Married Couple, but Not Lovers", 
    "Moriarty the Patriot", "Mushishi", "Mushoku Tensei Jobless Reincarnation", 
    "My Daemon", "My Deer Friend Nokotan", "My Dress Up Darling", 
    "My First Girlfriend is a Gal", "My Happy Marriage", "My Hero Academia", 
    "My Hero Academia Vigilantes", "My Home Hero", "My Isekai Life", "My Little Monster", 
    "My Love Story", "My Love Story with Yamada kun at Lv999", "My Neighbor Totoro", 
    "My New Boss is Goofy", "My Oni Girl", "My Roommate is a Cat", "My Tiny Senpai", 
    "My Unique Skill Makes Me OP even at Level 1", "My Wife Has No Emotion", 
    "Mysterious Disappearances", "Mysterious Girlfriend X", "Mieruko chan", 
    "Millennium Actress", "Miss Hokusai", "Mob Psycho 100", "Monster",

    # N
    "Nana", "Nekopara", "Neon Genesis Evangelion", "New Game", "Ninja Kamui", 
    "No Game, No Life", "Noblesse", "Noragami",

    # O
    "O Maidens in Your Savage Season", "Obey Me!", "Odd Taxi", "One Piece", 
    "One Punch Man", "Onimusha", "Orange", "Oresuki", "Oshi No Ko", 
    "Ouran High School Host Club",

    # P
    "Paprika", "Paradox Live The Animation", "Parallel World Pharmacy", "Paranoia Agent", 
    "Parasyte The Maxim", "Peach Boy Riverside", "Perfect Blue", "Pet Girl of Sakurasou", 
    "Plastic Memories", "Platinum End", "Pluto", "Ponyo", "Porco Rosso", 
    "Possibly the Greatest Alchemist of All Time", "Princess Mononoke", "Prison School", 
    "Promare", "Psycho Pass",

    # Q
    "Qualidea Code", "Quality Assurance in Another World", "Quintessential Quintuplets",

    # R
    "Radiant", "Ragna Crimson", "Rakshasa Street", "Ramayana The Legend of Prince Rama", 
    "Ranking of Kings", "Raven of the Inner Palace", "Re zero", "Record of Ragnarok", 
    "Red Ranger Becomes an Adventurer in Another World", "Redo of Healer", "Relife", 
    "Rent A Girlfriend", "Revenger", "Ride Your Wave", "Rinkai!", 
    "Rising of the Shield Hero", "Ron Kamonohashi's Forbidden Deductions",

    # S
    "SK8 the Infinity", "Sakamoto Days", "Samurai Champloo", "Sankarea Undying Love", 
    "Sarazanmai", "Sasaki and Miyano", "Scums Wish", "Seirei Gensouki: Spirit Chronicles", 
    "Serial Experiments Lain", "Servamp", "Shangri La Frontier", "Shiki", 
    "Shikimoris Not Just a Cutie", "Shirobako", "Shy", "Sing Yesterday For Me", 
    "Skip and Loafer", "Slam Dunk", "Sleepy Princess in the Demon Castle", 
    "Snow White with the Red Hair", "Solo Leveling", "Somali and the Forest Spirit", 
    "Sonny Boy", "Soul Eater", "Soul Eater Not!", "Sounds of Life", "Spirited Away", 
    "Spriggan", "Spy x Family", "Strawberry Marshmallow", "Steins Gate", 
    "Suicide Squad Isekai", "Summer Time Rendering", "Super Cub", "Super Hxeros", 
    "Suzume", "Sword Art Online",

    # T
    "Tada Never Falls In Love", "Taisho Otome Fairy Tale", "Takt Op Destiny", 
    "Tales from Earthsea", "Tales of Wedding Rings", "Tanaka-kun is Always Listless", 
    "Teasing Master Takagi san", "TenPuru No Way", "Tenchi Muyo War on Geminar", 
    "Terror in Resonance", "The Apothecary Diaries", "The Boy and the Heron", 
    "The Case Study of Vanitas", "The Cat Returns", "The Dangers in My Heart", 
    "The Day I Became a God", "The Demon Girl Next Door", "The Dreaming Boy is a Realist", 
    "The Elusive Samurai", "The Faraway Paladin", "The Foolish Angel Dances with the Devil", 
    "The Garden of Words", "The Girl I Like Forgot Her Glasses", "The God of High School", 
    "The Great Cleric", "The Greatest Demon Lord Is Reborn as a Typical Nobody", 
    "The Heike Story", "The Helpful Fox Senko san", "The Ice Guy and His Cool Female Colleague", 
    "The Legendary Hero is Dead", "The Millionaire Detective Balance UNLIMITED", 
    "The Misfit Of the Demon King Academy", "The Morose Mononokean", 
    "The Most Heretical Last Boss Queen: From Villainess to Savior", "The Royal Tutor", 
    "The Secret World of Arrietty", "The Seven Deadly Sins", 
    "The Tale of The Princess Kaguya", "The Testament of Sister New Devil", 
    "The Tunnel to Summer the Exit of Goodbyes", "The Unwanted Undead Adventurer", 
    "The Vexations of a Shut-In Vampire Princess", "The Wind Rises", 
    "The World's Finest Assassin Gets Reincarnated in Another World as an Aristocrat", 
    "The Wrong Way to Use Healing Magic", "The Yakuza's Guide to Babysitting", 
    "To Your Eternity", "Tokyo Ghoul", "Tokyo Godfathers", "Tokyo Magnitude 8.0", 
    "Tokyo Revengers", "Tomo chan Is a Girl", "Tomodachi Game", "Toradora", 
    "Tribe Nine", "Trigun Stampede", "Trinity Seven", "Tsukigakirei", 
    "Tying the Knot with an Amagami Sister",

    # U
    "Ubel Blatt", "Uncle from Another World", "Undead Unluck", "Unnamed Memory", 
    "Umamusume Pretty Derby", "Uzaki chan Wants to Hang Out",

    # V
    "Vampire Hunter D", "Vampire in the Garden", "Vermeil in Gold", "Vinland Saga", 
    "Violet Evergarden", "Vivy Flourite Eyes Song",

    # W
    "Weathering With You", "When Will Ayumu Make His Move", "Whisper Me a Love Song", 
    "Whisper of the Heart", "Wind breaker", "Wistoria Wand and Sword", 
    "Witch Craft Works", "Wolf Children", "Wonder Egg Priority", "Worlds End Harem", 
    "Wotakoi Love is Hard for Otaku",

    # X
    "Xenosaga The Animation", "Xam'd Lost Memories", "xxxHOLiC",

    # Y
    "Yakuza Fiance Raise wa Tanin ga Ii", "Yamada and the Seven Witches", 
    "You are Ms Servant", "Your Name", "Your lie in April",

    # Z
    "Zom 100 Bucket List of the Dead", "Zombie Land Saga",

    # #
    "4 Cut Hero", "5 Centimeters per Second", "91 Days"
]


INDEX_CHANNEL = "https://t.me/Animes2u_Index"

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class AnimeIndexBot:
    def __init__(self):
        self.application = Application.builder().token(BOT_TOKEN).build()
        self.setup_handlers()

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "🤖 **Anime Index Bot**\n\n"
            "I can check if anime titles are in our index! "
            "Add me to your group and I'll automatically check messages for anime titles.",
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🌸 Open Anime Index", url=INDEX_CHANNEL)
            ]])
        )

    async def check_anime_index(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Check if message contains anime from index"""
        try:
            text = update.message.text.strip()
            
            if len(text) < 3:
                return

            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("🌸 Open Anime Index", url=INDEX_CHANNEL)]
            ])

            found_anime = None
            for anime in ANIME_INDEX:
                pattern = rf'\b{re.escape(anime)}\b'
                if re.search(pattern, text, re.IGNORECASE):
                    found_anime = anime
                    break

            if found_anime:
                await update.message.reply_text(
                    f"✅ **{found_anime}** is in the index!",
                    reply_markup=buttons,
                    parse_mode='HTML'
                )
            else:
                await update.message.reply_text(
                    "🌀 Verify in index.",
                    reply_markup=buttons
                )
                
        except Exception as e:
            logger.error(f"Error: {e}")

    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, self.check_anime_index))

    def run(self):
        """Run the bot with conflict prevention"""
        logger.info("Starting Anime Index Bot...")
        
        # Add conflict prevention
        self.application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True,  # Important: drop pending updates
            close_loop=False
        )

def main():
    try:
        bot = AnimeIndexBot()
        bot.run()
    except Exception as e:
        logger.error(f"Bot crashed: {e}")

if __name__ == '__main__':
    main()
