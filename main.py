from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import json

user_language = {}

with open("translations.json", "r", encoding="utf-8") as f:
    translations = json.load(f)

# Buttons form translations.json
language_names = {
    "en": "🇬🇧English",
    "uk": "🇺🇦Українська",
    "pl": "🇵🇱Polski",
    "de": "🇩🇪Deutsch",
    "fr": "🇫🇷Français",
    "es": "🇪🇸Español",
    "it": "🇮🇹Italiano",
    "zh": "🇨🇳中文",
    "ja": "🇯🇵日本語",
    "ko": "🇰🇷한국어",
}
buttons = []
for lang_code in translations.keys():
    lang_name = language_names.get(lang_code, lang_code)
    buttons.append([InlineKeyboardButton(lang_name, callback_data=lang_code)])
Keyboard_inline = InlineKeyboardMarkup(buttons)

async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    lang = query.data
    user_language[user_id] = lang
    await query.answer()
    lang_name = language_names.get(lang, lang)
    text = translations[lang].get("language_selected", "Language selected.").replace("{language}", lang_name)
    await query.edit_message_text(text=text)

# Command /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = user_language.get(user_id, "en")
    await update.message.reply_text(
        translations[lang].get("start", "Welcome!"),
        reply_markup=Keyboard_inline
    )

# Command /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = user_language.get(user_id, "en")
    await update.message.reply_text(
        translations[lang].get("help", "Help is not available.")
    )

if __name__ == "__main__":
    application = ApplicationBuilder().token("YOUR_TOKEN").build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(language_callback))
    application.run_polling()