TOKEN = "8759468173:AAH-X91XvuBbZ2RAu54bJPXwYb1jc6-D4F4"

import logging

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from db import (
    get_leagues_by_sport,
    get_teams_by_league,
    get_team_details,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

SPORT, LEAGUE, TEAM = range(3)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Football"], ["Cancel"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text("Choose sport:", reply_markup=reply_markup)
    return SPORT


async def choose_sport(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Football":
        leagues = get_leagues_by_sport("Football")

        keyboard = [[league] for league in leagues]
        keyboard.append(["Cancel"])

        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        await update.message.reply_text("Choose league:", reply_markup=reply_markup)
        return LEAGUE

    elif text == "Cancel":
        await update.message.reply_text("Canceled.", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    else:
        await update.message.reply_text("Choose Football")
        return SPORT


async def choose_league(update: Update, context: ContextTypes.DEFAULT_TYPE):
    league = update.message.text

    if league == "Cancel":
        await update.message.reply_text("Canceled.", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    context.user_data["league"] = league

    teams = get_teams_by_league(league)

    keyboard = [[team] for team in teams]
    keyboard.append(["Back", "Cancel"])

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text("Choose team:", reply_markup=reply_markup)
    return TEAM


async def choose_team(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Back":
        leagues = get_leagues_by_sport("Football")
        keyboard = [[league] for league in leagues]
        keyboard.append(["Cancel"])

        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        await update.message.reply_text("Choose league:", reply_markup=reply_markup)
        return LEAGUE

    if text == "Cancel":
        await update.message.reply_text("Canceled.", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    team = get_team_details(text)

    if not team:
        await update.message.reply_text("Team not found")
        return TEAM

    team_id, sport, name, country, league, stadium, coach, founded_year, trophies, description = team

    msg = (
        f"Team: {name}\n"
        f"Country: {country}\n"
        f"League: {league}\n"
        f"Stadium: {stadium}\n"
        f"Coach: {coach}\n"
        f"Founded: {founded_year}\n"
        f"Trophies: {trophies}\n"
    )

    keyboard = [["Another team"], ["Another league"], ["Cancel"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(msg, reply_markup=reply_markup)
    return TEAM


async def handle_after(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Another team":
        league = context.user_data.get("league")
        teams = get_teams_by_league(league)

        keyboard = [[team] for team in teams]
        keyboard.append(["Back", "Cancel"])

        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        await update.message.reply_text("Choose team:", reply_markup=reply_markup)
        return TEAM

    elif text == "Another league":
        leagues = get_leagues_by_sport("Football")

        keyboard = [[league] for league in leagues]
        keyboard.append(["Cancel"])

        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        await update.message.reply_text("Choose league:", reply_markup=reply_markup)
        return LEAGUE

    elif text == "Cancel":
        await update.message.reply_text("Canceled.", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    else:
        return await choose_team(update, context)


def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SPORT: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_sport)],
            LEAGUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_league)],
            TEAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_after)],
        },
        fallbacks=[],
    )

    app.add_handler(conv_handler)

    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()