
# handlers/commands.py

import os

import pandas as pd

from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from telegram.ext import ContextTypes

from config import ADMIN_ID



# In-memory Structured Stock Database grouped by Category

STOCK_DATABASE = {

    "clothing": {

        "display_name": "សម្លៀកបំពាក់",

        "items": {

            "អាវយឺត": {"stock": 50, "image": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500"},

            "ខោខូវប៊យ": {"stock": 30, "image": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=500"}

        }

    },

    "accessories": {

        "display_name": "សម្ភារៈ",

        "items": {

            "កាបូប": {"stock": 20, "image": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=500"},

            "ស្បែកជើង": {"stock": 15, "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500"}

        }

    }

}

ORDERS_LIST = []
HISTORY_LOG = []
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    """Generates the primary persistent bottom button pad."""

    admin_keyboard = [

        ["📋 មើលស្តុកទាំងអស់", "🔍 ស្វែងរកទំនិញ"],

        ["➕ បន្ថែមទំនិញចូល", "➖ កាត់ទំនិញចេញ"],

        ["⚠️ ទំនិញជិតអស់", "📜 មើលប្រវត្តិចូល/ចេញ"],

        ["📊 ទាញយករបាយការណ៍ Excel"]

    ]

    reply_markup = ReplyKeyboardMarkup(admin_keyboard, resize_keyboard=True)

    welcome_text = (

        "👨‍✈️ **សូមស្វាគមន៍ 🙏❤️**\n\n"

        "ប្រព័ន្ធគ្រប់គ្រងស្តុក (Smart Stock) រួចរាល់ហើយ。\n"

        "លោកអ្នកអាចប្រើប្រាស់ប៊ូតុងបញ្ជានៅខាងក្រោមបានយ៉ាងរហ័ស 👇"

    )

    await update.message.reply_text(text=welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    """Provides usage details for manual fallback commands."""

    help_text = (

        "🤖 **របៀបប្រើប្រាស់ Smart Stock Bot Manual Commands**\n\n"

        "ក្រៅពីការប្រើប៊ូតុង លោកអ្នកអាចវាយពាក្យបញ្ជាផ្ទាល់៖\n"

        "• ថែមស្តុក៖ `/stock_in [ឈ្មោះទំនិញ] [ចំនួន]`\n"

        "• កាត់ស្តុក៖ `/stock_out [ឈ្មោះទំនិញ] [ចំនួន]`\n"

        "• ស្វែងរក៖ `/find [ឈ្មោះទំនិញ]`"

    )

    await update.message.reply_text(text=help_text, parse_mode="Markdown")
# ==================== Text Keyboard Button Handlers ====================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    print(f"📩 Input received from button press: {text}")



    if text == "📋 មើលស្តុកទាំងអស់":

        keyboard = []

        for eng_key, cat_data in STOCK_DATABASE.items():

            khmer_name = cat_data["display_name"]

            keyboard.append([InlineKeyboardButton(f"📁 ប្រភេទ៖ {khmer_name}", callback_data=f"cat_{eng_key}")])

           
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("📂 **សូមជ្រើសរើសប្រភេទក្រុមទំនិញ៖**", reply_markup=reply_markup, parse_mode="Markdown")

    elif text == "🔍 ស្វែងរកទំនិញ":

        await update.message.reply_text("💡 ដើម្បីស្វែងរក សូមវាយ៖ `/find [ឈ្មោះទំនិញ]`\n*ឧទាហរណ៍៖* `/find អាវយឺត`", parse_mode="Markdown")

    elif text == "➕ បន្ថែមទំនិញចូល":

        await update.message.reply_text("💡 ដើម្បីថែមស្តុក សូមវាយ៖ `/stock_in [ឈ្មោះទំនិញ] [ចំនួន]`\n*ឧទាហរណ៍៖* `/stock_in អាវយឺត 20`", parse_mode="Markdown")

    elif text == "➖ កាត់ទំនិញចេញ":

        await update.message.reply_text("💡 ដើម្បីកាត់ស្តុកចេញ សូមវាយ៖ `/stock_out [ឈ្មោះទំនិញ] [ចំនួន]`\n*ឧទាហរណ៍៖* `/stock_out អាវយឺត 5`", parse_mode="Markdown")

    elif text == "⚠️ ទំនិញជិតអស់":

        low_stock = ""

        for cat_data in STOCK_DATABASE.values():

            for prod, info in cat_data["items"].items():

                if info["stock"] <= 15:

                    low_stock += f" {prod}: សល់ត្រឹមតែ **{info['stock']}** ទេ!\n"

        if not low_stock:

            low_stock = "✅ មិនមានទំនិញណាជិតអស់ពីស្តុកឡើយ។"

        await update.message.reply_text(low_stock, parse_mode="Markdown")


    elif text == "📜 មើលប្រវត្តិចូល/ចេញ":

        if not HISTORY_LOG:

            await update.message.reply_text("📜 មិនទាន់មានប្រវត្តិកែប្រែស្តុកនៅឡើយទេ។")

        else:

            log_text = "📜 **ប្រវត្តិនៃការកែប្រែស្តុក៖**\n\n" + "\n".join(HISTORY_LOG)

            await update.message.reply_text(log_text, parse_mode="Markdown")



    #  បានកែសម្រួល៖ បន្ថែមមុខងារបង្កើត និងនាំចេញឯកសារ Excel ពិតប្រាកដ

    # 📊 ទាញយករបាយការណ៍ Excel (បានធ្វើបច្ចុប្បន្នភាព៖ នាំចេញទាំងស្តុកបច្ចុប្បន្ន និងប្រវត្តិចូល/ចេញ)

    elif text == "📊 ទាញយករបាយការណ៍ Excel":

        await update.message.reply_text("⏳ កំពុងដំណើរការបង្កើតឯកសារ Excel បូករួមទាំងប្រវត្តិចូល/ចេញ សូមរង់ចាំមួយភ្លែត...")

       

        # === ១. រៀបចំទិន្នន័យសម្រាប់ Sheet ទី ១: ស្តុកបច្ចុប្បន្ន ===

        current_stock_list = []

        for eng_key, cat_data in STOCK_DATABASE.items():

            category_name = cat_data["display_name"]

            for prod_name, info in cat_data["items"].items():

                current_stock_list.append({

                    "ប្រភេទក្រុមទំនិញ": category_name,

                    "ឈ្មោះផលិតផល": prod_name,

                    "ចំនួនក្នុងស្តុកបច្ចុប្បន្ន": info["stock"]

                })

        df_stock = pd.DataFrame(current_stock_list)

        # === ២. រៀបចំទិន្នន័យសម្រាប់ Sheet ទី ២: ប្រវត្តិចូល/ចេញ ===

        history_list = []

        if HISTORY_LOG:

            for log in HISTORY_LOG:

                # បំបែកប្រភេទប្រតិបត្តិការដើម្បីឱ្យមើលទៅមានរបៀបក្នុង Excel

                status = "📥 ចូល" if "📥" in log or "ថែម" in log else "📤 ចេញ"

                # សម្អាតសញ្ញា Emoji ចេញខ្លះដើម្បីឱ្យអានស្រួលក្នុង Excel

                clean_log = log.replace("📥 ", "").replace("📤 ", "").replace("📦 ", "").replace("`", "")

                history_list.append({

                    "ប្រភេទប្រតិបត្តិការ": status,

                    "ព័ត៌មានលម្អិតនៃសកម្មភាព": clean_log

                })

        else:

            # ករណីមិនទាន់មានប្រវត្តិទាល់តែសោះ ត្រូវដាក់ទិន្នន័យគំរូការពារកុំឱ្យ Excel Blank

            history_list.append({

                "ប្រភេទប្រតិបត្តិការ": "មិនទាន់មាន",

                "ព័ត៌មានលម្អិតនៃសកម្មភាព": "មិនទាន់មានប្រវត្តិនៃការកែប្រែស្តុកចូល/ចេញនៅឡើយទេ"

            })

        df_history = pd.DataFrame(history_list)

       

# === ៣. ប្រើប្រាស់ ExcelWriter ដើម្បីបង្កើត Multi-Sheet Excel ===

        file_name = "stock_report.xlsx"

        try:

            with pd.ExcelWriter(file_name, engine="openpyxl") as writer:

                df_stock.to_excel(writer, sheet_name="ស្តុកបច្ចុប្បន្ន", index=False)

                df_history.to_excel(writer, sheet_name="ប្រវត្តិចូល_ចេញ", index=False)        

            # === ៤. ផ្ញើឯកសារត្រឡប់ទៅកាន់ Telegram (កែប្រែទៅជា HTML ទម្រង់សុវត្ថិភាព) ===

            with open(file_name, "rb") as excel_file:

                await update.message.reply_document(

                    document=excel_file,

                    filename=file_name,

                    # ✅ ប្តូរមកប្រើ Tag <b> របស់ HTML វិញ ធានាមិនអេរ៉ើ ១០០%

                    caption=(

                        "📊 <b>បានបង្កើតរបាយការណ៍ស្តុកគ្រប់ជ្រុងជ្រោយរួចរាល់!</b>\n\n"

                        "📂 ឈ្មោះឯកសារ៖ <code>stock_report.xlsx</code>\n"

                        "✨ <i>នៅក្នុងឯកសារនេះមានសន្លឹកកិច្ចការ ២ (Sheets)៖</i>\n"

                        "1️⃣ <b>ស្តុកបច្ចុប្បន្ន</b> (Current Inventory)\n"

                        "2️⃣ <b>ប្រវត្តិចូល_ចេញ</b> (Stock In/Out History)"

                    ),

                    parse_mode="HTML" # 🔥 ដូរពី Markdown ទៅជា HTML

                )

           

            os.remove(file_name)

           

        except Exception as e:

            await update.message.reply_text(f"❌ មានបញ្ហាក្នុងការបង្កើតឯកសារ៖ {e}")

# ==================== Inline Context Callback Handlers ====================



async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

   

    data = query.data

    chat_id = query.message.chat_id

  # 1. Entering a Category Group

    if data.startswith("cat_"):

        category_key = data.split("_")[1]

        category_data = STOCK_DATABASE.get(category_key, {})

        khmer_title = category_data.get("display_name", "មិនស្គាល់")

        products = category_data.get("items", {})

       

        keyboard = []

        for prod_name in products.keys():

            keyboard.append([InlineKeyboardButton(f"📦 {prod_name}", callback_data=f"prod_{category_key}_{prod_name}")])

       

        keyboard.append([InlineKeyboardButton("⬅️ ត្រឡប់ក្រោយ", callback_data="back_to_categories")])

        reply_markup = InlineKeyboardMarkup(keyboard)

       

        if query.message.photo:

            await query.message.delete()

            await context.bot.send_message(chat_id=chat_id, text=f"📋 **បញ្ជីទំនិញក្នុងក្រុម [{khmer_title}]៖**", reply_markup=reply_markup, parse_mode="Markdown")

        else:

            await query.edit_message_text(text=f"📋 **បញ្ជីទំនិញក្នុងក្រុម [{khmer_title}]៖**", reply_markup=reply_markup, parse_mode="Markdown")
    # 2. Rendering Product Detailed Inventory Card

    elif data.startswith("prod_"):

        _, category_key, prod_name = data.split("_")

        product_info = STOCK_DATABASE[category_key]["items"][prod_name]

    
        stock_count = product_info["stock"]

        image_url = product_info["image"]

        keyboard = [[InlineKeyboardButton("⬅️ ត្រឡប់ក្រោយ", callback_data=f"cat_{category_key}")]]

        reply_markup = InlineKeyboardMarkup(keyboard)

       

        await query.message.delete()

       

        caption_text = f"🛍️ **ព័ត៌មានលម្អិតពីទំនិញ៖**\n\n🆔 ឈ្មោះ៖ **{prod_name}**\n📊 ចំនួនក្នុងស្តុក៖ **{stock_count}**"

        await context.bot.send_photo(

            chat_id=chat_id,

            photo=image_url,

            caption=caption_text,

            reply_markup=reply_markup,

            parse_mode="Markdown"

        )



    # 3. Category Screen Escape Route Loop (Back action)

    elif data == "back_to_categories":

        keyboard = []

        for eng_key, cat_data in STOCK_DATABASE.items():

            khmer_name = cat_data["display_name"]

            keyboard.append([InlineKeyboardButton(f"📁 ប្រភេទ៖ {khmer_name}", callback_data=f"cat_{eng_key}")])

        reply_markup = InlineKeyboardMarkup(keyboard)

       

        if query.message.photo:

            await query.message.delete()

            await context.bot.send_message(chat_id=chat_id, text="📂 **សូមជ្រើសរើសប្រភេទក្រុមទំនិញ៖**", reply_markup=reply_markup, parse_mode="Markdown")

        else:

            await query.edit_message_text("📂 **សូមជ្រើសរើសប្រភេទក្រុមទំនិញ៖**", reply_markup=reply_markup, parse_mode="Markdown")



# ==================== Fallback Typing Commands ====================



async def stock_in_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        prod, qty = context.args[0], int(context.args[1])

        for cat_data in STOCK_DATABASE.values():

            if prod in cat_data["items"]:

                cat_data["items"][prod]["stock"] += qty

                HISTORY_LOG.append(f"📥 ថែម `{prod}` ចំនួន `+{qty}`")

                await update.message.reply_text(f"✅ បានថែម {prod} ចំនួន {qty} ទៅក្នុងស្តុក!")

                return

        await update.message.reply_text(f"❌ រកមិនឃើញឈ្មោះទំនិញ '{prod}' ក្នុងប្រព័ន្ធដើម្បីបន្ថែមទេ។")

    except:

        await update.message.reply_text("⚠️ វាយខុសទម្រង់! សូមប្រើ៖ `/stock_in [ឈ្មោះទំនិញ] [ចំនួន]`")



async def stock_out_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        prod, qty = context.args[0], int(context.args[1])

        for cat_data in STOCK_DATABASE.values():

            if prod in cat_data["items"]:

                if cat_data["items"][prod]["stock"] >= qty:

                    cat_data["items"][prod]["stock"] -= qty

                    HISTORY_LOG.append(f"📤 កាត់ `{prod}` ចំនួន `-{qty}`")

                    await update.message.reply_text(f"📉 បានកាត់ {prod} ចំនួន {qty} ចេញពីស្តុក!")

                else:

                    await update.message.reply_text("❌ ចំនួនក្នុងស្តុកមិនគ្រាន់សម្រាប់កាត់ចេញទេ!")

                return

        await update.message.reply_text(f"❌ រកមិនឃើញឈ្មោះទំនិញ '{prod}' ទេ។")

    except:

        await update.message.reply_text("⚠️ វាយខុសទម្រង់! សូមប្រើ៖ `/stock_out [ឈ្មោះទំនិញ] [ចំនួន]`")



async def find_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args: return

    prod = context.args[0]

    for cat_data in STOCK_DATABASE.values():

        if prod in cat_data["items"]:

            await update.message.reply_text(f"🔍 ជួបហើយ៖ **{prod}** មានចំនួន **{cat_data['items'][prod]['stock']}** ក្នុងស្តុក។", parse_mode="Markdown")

            return

    await update.message.reply_text("❌ រកមិនឃើញទំនិញនេះក្នុងប្រព័ន្ធទេ។")



async def get_order_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        prod, qty = context.args[0], int(context.args[1])

        for cat_data in STOCK_DATABASE.values():

            if prod in cat_data["items"]:

                if cat_data["items"][prod]["stock"] >= qty:

                    cat_data["items"][prod]["stock"] -= qty

                    cust_name = update.effective_user.first_name

                    ORDERS_LIST.append({"customer": cust_name, "product": prod, "qty": qty})

                    HISTORY_LOG.append(f"📦 លោក {cust_name} ទិញ `{prod}` ចំនួន `-{qty}`")

                    await update.message.reply_text(f"🎉 ការកុម្ម៉ង់ជោគជ័យ! អរគុណសម្រាប់ការទិញ {prod} ចំនួន {qty}។")

                else:

                    await update.message.reply_text("❌ សុំទោស ទំនិញក្នុងស្តុកមិនមានគ្រប់គ្រាន់ទេ។")

                return

        await update.message.reply_text("❌ គ្មានផលិតផលឈ្មោះនេះទេ។")

    except:

        await update.message.reply_text("⚠️ របៀបកុម្ម៉ង់៖ `/order [ឈ្មោះទំនិញ] [ចំនួន]`")



       

