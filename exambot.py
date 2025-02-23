from telegram import Update, InputFile from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler

Define states

PAYMENT = 1

Admin Telegram ID

ADMIN_ID = 1852711786  # Replace with your Telegram ID

Available exams

EXAMS = { 'chemistry': {'price': '₹1999', 'upi_id': '8445382446@ptyes'}, 'maths': {'price': '₹1999', 'upi_id': '8445382446@ptyes'}, 'biology': {'price': '₹1999', 'upi_id': '8445382446@ptyes'} }

CBSE_EXAMS = { '10th': 'CBSE Class 10th Exam 2025: Starts from March 2025. Subjects: Maths, Science, English, Social Science.', '12th': 'CBSE Class 12th Exam 2025: Starts from March 2025. Streams: Science, Commerce, Arts. Practical exams in February.' }

LEAKED_EXAMS = ['12th Chemistry', '10th Maths', '12th Physics']

User database

user_purchases = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: await update.message.reply_text( 'Welcome to ExamBot! 📚\n\nUse /menu to see available exams, /cbse_exams for CBSE 2025 exam details, /leaked_exams to view leaked exams, or /help for more commands.' )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: exam_list = '\n'.join([f'{exam.capitalize()}: {details["price"]}' for exam, details in EXAMS.items()]) leaked_list = '\n'.join(LEAKED_EXAMS) await update.message.reply_text(f'Available Exams:\n{exam_list}\n\n💥 Leaked Exams:\n{leaked_list}\n\nUse /buy_exam [exam_name] to purchase.')

async def cbse_exams(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: cbse_details = '\n\n'.join([f'{cls}: {details}' for cls, details in CBSE_EXAMS.items()]) await update.message.reply_text(f'📋 CBSE 2025 Exams:\n\n{cbse_details}')

async def leaked_exams(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: leaked_list = '\n'.join(LEAKED_EXAMS) await update.message.reply_text(f'💥 Leaked Exams:\n{leaked_list}')

async def buy_exam(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: if len(context.args) == 0 or context.args[0].lower() not in EXAMS: await update.message.reply_text('Please specify a valid exam. Example: /buy_exam chemistry') return ConversationHandler.END

exam_name = context.args[0].lower()
context.user_data['exam_name'] = exam_name

upi_id = EXAMS[exam_name]['upi_id']
price = EXAMS[exam_name]['price']

await update.message.reply_text(
    f'Scan the QR code or use this UPI ID: {upi_id} to pay {price}. After payment, use /payment_success to confirm.'
)

return PAYMENT

async def payment_success(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: exam_name = context.user_data.get('exam_name') if exam_name: user_purchases[update.message.from_user.id] = exam_name await update.message.reply_text(f'Payment successful! You have purchased the {exam_name} exam.')

async def my_exams(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: user_id = update.message.from_user.id if user_id in user_purchases: exam_name = user_purchases[user_id] await update.message.reply_text(f'You have purchased the {exam_name} exam.') else: await update.message.reply_text('You have not purchased any exams yet.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: await update.message.reply_text( '🤖 ExamBot Commands:\n\n' '/menu - View available exams with prices\n' '/cbse_exams - View CBSE 2025 Class 10th and 12th exam details\n' '/leaked_exams - View leaked exams\n' '/buy_exam [exam_name] - Purchase an exam (e.g., /buy_exam chemistry)\n' '/payment_success - Confirm payment\n' '/my_exams - View purchased exams\n' '/help - View this help message' )

Admin Commands

async def admin_list_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: if update.message.from_user.id == ADMIN_ID: if user_purchases: users_list = '\n'.join([f'User {uid}: {exam}' for uid, exam in user_purchases.items()]) await update.message.reply_text(f'User Purchases:\n{users_list}') else: await update.message.reply_text('No users have purchased exams yet.')

Main function

def main() -> None: TOKEN = '7429297419:AAHOfZEPKl474CbP9vifohxkooboQT-skZg'

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('menu', menu))
app.add_handler(CommandHandler('cbse_exams', cbse_exams))
app.add_handler(CommandHandler('leaked_exams', leaked_exams))
app.add_handler(CommandHandler('my_exams', my_exams))
app.add_handler(CommandHandler('help', help_command))
app.add_handler(CommandHandler('admin_list_users', admin_list_users))

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('buy_exam', buy_exam)],
    states={PAYMENT: [CommandHandler('payment_success', payment_success)]},
    fallbacks=[]
)
app.add_handler(conv_handler)

print('Bot is running...')
app.run_polling()

if name == 'main': main()

