import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import sqlite3
import json
from datetime import datetime
import os

# Bot Configuration
BOT_TOKEN = "8220207143:AAEtXWlpbEg_ghHc24USkb8yDeWlr4_9R58"
ADMIN_TOKEN = "8240568393:AAGmPeR7BAYBu2A1_fjkI-l2lkN7ZUdejS4"
ADMIN_ID = 6416284194

# Database setup
def setup_database():
    conn = sqlite3.connect('education_bot.db')
    c = conn.cursor()
    
    # Create tables for storing PDF links
    c.execute('''CREATE TABLE IF NOT EXISTS pdf_links
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  class_name TEXT,
                  subject TEXT,
                  sub_category TEXT,
                  topic_type TEXT,
                  pdf_link TEXT,
                  added_by INTEGER,
                  added_date TEXT)''')
    
    conn.commit()
    conn.close()

# Initialize database
setup_database()

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Navigation states dictionary for admin upload
admin_states = {}

# Main menu keyboards
def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("📚 Class 10th", callback_data='class_10')],
        [InlineKeyboardButton("📖 Class 9th", callback_data='class_9')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_class_10_subjects():
    keyboard = [
        [InlineKeyboardButton("🔬 Science", callback_data='cls10_science')],
        [InlineKeyboardButton("📝 Hindi", callback_data='cls10_hindi')],
        [InlineKeyboardButton("🏛️ History", callback_data='cls10_history')],
        [InlineKeyboardButton("🕉️ Sanskrit", callback_data='cls10_sanskrit')],
        [InlineKeyboardButton("🧮 Maths", callback_data='cls10_maths')],
        [InlineKeyboardButton("🔙 Back to Main Menu", callback_data='back_to_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_class_9_subjects():
    keyboard = [
        [InlineKeyboardButton("🔬 Science", callback_data='cls9_science')],
        [InlineKeyboardButton("📝 Hindi", callback_data='cls9_hindi')],
        [InlineKeyboardButton("🏛️ History", callback_data='cls9_history')],
        [InlineKeyboardButton("🕉️ Sanskrit", callback_data='cls9_sanskrit')],
        [InlineKeyboardButton("🧮 Maths", callback_data='cls9_maths')],
        [InlineKeyboardButton("🔙 Back to Main Menu", callback_data='back_to_main')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_science_categories(class_name):
    keyboard = [
        [InlineKeyboardButton("⚡ Physics", callback_data=f'{class_name}_physics')],
        [InlineKeyboardButton("🧪 Chemistry", callback_data=f'{class_name}_chemistry')],
        [InlineKeyboardButton("🧬 Biology", callback_data=f'{class_name}_biology')],
        [InlineKeyboardButton("🔙 Back", callback_data=f'back_to_{class_name}')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_topic_types(class_name, subject):
    keyboard = [
        [InlineKeyboardButton("📝 Subjective", callback_data=f'{class_name}_{subject}_subjective')],
        [InlineKeyboardButton("❓ Objective", callback_data=f'{class_name}_{subject}_objective')],
        [InlineKeyboardButton("📒 Notes", callback_data=f'{class_name}_{subject}_notes')],
        [InlineKeyboardButton("🔙 Back", callback_data=f'back_to_{class_name}_{subject}')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_admin_upload_keyboard(current_path):
    keyboard = [
        [InlineKeyboardButton("📤 Upload PDF", callback_data=f'upload_{current_path}')],
        [InlineKeyboardButton("🔙 Back", callback_data=f'admin_back_{current_path}')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # Welcome message
    welcome_text = f"✨ Welcome to SK Education, {user.first_name}! ✨\n\n"
    welcome_text += "📚 Select your class to get started:"
    
    # Send image with caption
    await update.message.reply_photo(
        photo="https://i.ibb.co/60SXL2kR/IMG-20260307-WA0001.jpg",
        caption=welcome_text,
        reply_markup=get_main_menu()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    user_id = query.from_user.id
    
    # Check if user is admin
    is_admin = (user_id == ADMIN_ID)
    
    # Handle back navigation
    if data == 'back_to_main':
        await query.edit_message_caption(
            caption="📚 Select your class:",
            reply_markup=get_main_menu()
        )
    
    # Class selections
    elif data == 'class_10':
        await query.edit_message_caption(
            caption="📚 Class 10th - Select Subject:",
            reply_markup=get_class_10_subjects()
        )
    
    elif data == 'class_9':
        await query.edit_message_caption(
            caption="📚 Class 9th - Select Subject:",
            reply_markup=get_class_9_subjects()
        )
    
    # Class 10 subject handlers
    elif data == 'cls10_science':
        await query.edit_message_caption(
            caption="🔬 Science - Select Category:",
            reply_markup=get_science_categories('cls10')
        )
    
    elif data.startswith('cls10_') and data not in ['cls10_science', 'cls10_physics', 'cls10_chemistry', 'cls10_biology']:
        subject = data.replace('cls10_', '')
        await query.edit_message_caption(
            caption=f"📚 Class 10th {subject.capitalize()} - Select Type:",
            reply_markup=get_topic_types('cls10', subject)
        )
    
    # Class 9 subject handlers
    elif data == 'cls9_science':
        await query.edit_message_caption(
            caption="🔬 Science - Select Category:",
            reply_markup=get_science_categories('cls9')
        )
    
    elif data.startswith('cls9_') and data not in ['cls9_science', 'cls9_physics', 'cls9_chemistry', 'cls9_biology']:
        subject = data.replace('cls9_', '')
        await query.edit_message_caption(
            caption=f"📚 Class 9th {subject.capitalize()} - Select Type:",
            reply_markup=get_topic_types('cls9', subject)
        )
    
    # Science subcategories
    elif data in ['cls10_physics', 'cls10_chemistry', 'cls10_biology', 
                  'cls9_physics', 'cls9_chemistry', 'cls9_biology']:
        parts = data.split('_')
        class_name = parts[0]
        subject = parts[1]
        await query.edit_message_caption(
            caption=f"📚 {class_name.upper()} {subject.capitalize()} - Select Type:",
            reply_markup=get_topic_types(class_name, subject)
        )
    
    # Topic type selections (Subjective, Objective, Notes)
    elif any(x in data for x in ['_subjective', '_objective', '_notes']):
        parts = data.split('_')
        class_name = parts[0]
        subject = parts[1]
        topic_type = parts[2]
        
        # Fetch PDF links from database
        conn = sqlite3.connect('education_bot.db')
        c = conn.cursor()
        c.execute('''SELECT pdf_link FROM pdf_links 
                     WHERE class_name=? AND subject=? AND topic_type=?
                     ORDER BY added_date DESC''', 
                  (class_name, subject, topic_type))
        pdfs = c.fetchall()
        conn.close()
        
        # Create display text
        display_text = f"📚 {class_name.upper()} - {subject.capitalize()} - {topic_type.capitalize()}\n\n"
        
        if pdfs:
            for i, pdf in enumerate(pdfs, 1):
                display_text += f"{i}. 📄 [Click here to download]({pdf[0]})\n"
        else:
            display_text += "❌ No PDFs available for this topic yet."
        
        display_text += "\n\n👇 Welcome to SK Education\n[Click here and download PDF smoothly](https://skeducation.ct.ws)"
        
        # Add admin upload button if user is admin
        if is_admin:
            current_path = f"{class_name}_{subject}_{topic_type}"
            await query.edit_message_caption(
                caption=display_text,
                reply_markup=get_admin_upload_keyboard(current_path),
                parse_mode='Markdown'
            )
        else:
            await query.edit_message_caption(
                caption=display_text,
                parse_mode='Markdown'
            )
    
    # Handle admin upload
    elif data.startswith('upload_'):
        current_path = data.replace('upload_', '')
        parts = current_path.split('_')
        class_name = parts[0]
        subject = parts[1]
        topic_type = parts[2]
        
        admin_states[user_id] = {
            'class': class_name,
            'subject': subject,
            'topic_type': topic_type,
            'waiting_for_link': True
        }
        
        await query.edit_message_caption(
            caption=f"📤 Send me the PDF link for:\n"
                   f"Class: {class_name}\n"
                   f"Subject: {subject}\n"
                   f"Type: {topic_type}\n\n"
                   f"Please send the full URL:"
        )
    
    # Handle back navigation for admin
    elif data.startswith('admin_back_'):
        current_path = data.replace('admin_back_', '')
        parts = current_path.split('_')
        class_name = parts[0]
        subject = parts[1]
        topic_type = parts[2]
        
        # Show the topic view again
        conn = sqlite3.connect('education_bot.db')
        c = conn.cursor()
        c.execute('''SELECT pdf_link FROM pdf_links 
                     WHERE class_name=? AND subject=? AND topic_type=?
                     ORDER BY added_date DESC''', 
                  (class_name, subject, topic_type))
        pdfs = c.fetchall()
        conn.close()
        
        display_text = f"📚 {class_name.upper()} - {subject.capitalize()} - {topic_type.capitalize()}\n\n"
        
        if pdfs:
            for i, pdf in enumerate(pdfs, 1):
                display_text += f"{i}. 📄 [Click here to download]({pdf[0]})\n"
        else:
            display_text += "❌ No PDFs available for this topic yet."
        
        display_text += "\n\n👇 Welcome to SK Education\n[Click here and download PDF smoothly](https://skeducation.ct.ws)"
        
        await query.edit_message_caption(
            caption=display_text,
            reply_markup=get_admin_upload_keyboard(current_path),
            parse_mode='Markdown'
        )
    
    # Handle back navigation for regular users
    elif data.startswith('back_to_'):
        back_to = data.replace('back_to_', '')
        
        if back_to == 'cls10':
            await query.edit_message_caption(
                caption="📚 Class 10th - Select Subject:",
                reply_markup=get_class_10_subjects()
            )
        elif back_to == 'cls9':
            await query.edit_message_caption(
                caption="📚 Class 9th - Select Subject:",
                reply_markup=get_class_9_subjects()
            )
        elif back_to in ['cls10_science', 'cls9_science']:
            class_name = back_to[:5]
            await query.edit_message_caption(
                caption="🔬 Science - Select Category:",
                reply_markup=get_science_categories(class_name)
            )
        elif '_' in back_to:
            parts = back_to.split('_')
            class_name = parts[0]
            subject = parts[1]
            await query.edit_message_caption(
                caption=f"📚 {class_name.upper()} {subject.capitalize()} - Select Type:",
                reply_markup=get_topic_types(class_name, subject)
            )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message_text = update.message.text
    
    # Check if user is in admin upload state
    if user_id in admin_states and admin_states[user_id].get('waiting_for_link'):
        state = admin_states[user_id]
        
        # Validate URL
        if message_text.startswith(('http://', 'https://')):
            # Save to database
            conn = sqlite3.connect('education_bot.db')
            c = conn.cursor()
            c.execute('''INSERT INTO pdf_links 
                        (class_name, subject, topic_type, pdf_link, added_by, added_date)
                        VALUES (?, ?, ?, ?, ?, ?)''',
                     (state['class'], state['subject'], state['topic_type'], 
                      message_text, user_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
            conn.close()
            
            # Clear admin state
            del admin_states[user_id]
            
            # Show confirmation with current PDFs
            conn = sqlite3.connect('education_bot.db')
            c = conn.cursor()
            c.execute('''SELECT pdf_link FROM pdf_links 
                         WHERE class_name=? AND subject=? AND topic_type=?
                         ORDER BY added_date DESC''', 
                      (state['class'], state['subject'], state['topic_type']))
            pdfs = c.fetchall()
            conn.close()
            
            display_text = f"✅ PDF added successfully!\n\n"
            display_text += f"📚 {state['class'].upper()} - {state['subject'].capitalize()} - {state['topic_type'].capitalize()}\n\n"
            
            if pdfs:
                for i, pdf in enumerate(pdfs, 1):
                    display_text += f"{i}. 📄 [Click here to download]({pdf[0]})\n"
            
            display_text += "\n\n👇 Welcome to SK Education\n[Click here and download PDF smoothly](https://skeducation.ct.ws)"
            
            current_path = f"{state['class']}_{state['subject']}_{state['topic_type']}"
            await update.message.reply_text(
                display_text,
                reply_markup=get_admin_upload_keyboard(current_path),
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text("❌ Please send a valid URL starting with http:// or https://")
    
    else:
        # If not admin, ignore other messages
        pass

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.warning(f'Update {update} caused error {context.error}')

def main():
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)
    
    # Start bot
    print("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()