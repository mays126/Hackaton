from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from keyboards import kb_main,main_user_menu_kb
from datebase import rolls,menu
from handlers import other as oth
from aiogram.dispatcher import FSMContext
from handlers.client import user_data



async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.reply('OK',reply_markup=kb_main)
        return
    await state.finish()
    await message.reply("OK", reply_markup=kb_main)


async def roll_order_start(callback: types.CallbackQuery):
    await oth.roll_order.adress.set()
    await callback.message.reply('Введите адресс доставки',reply_markup=main_user_menu_kb)
    await callback.answer('')

async def roll_order_adress(message: types.Message,state: FSMContext):
    async with state.proxy() as data:
        data['adress'] = message.text
    await oth.roll_order.next()
    await message.reply('Введите название выбранных ролов')

async def roll_order_name(message: types.Message,state: FSMContext):
    menu_data = menu.SelectTable('delivery.db')
    async with state.proxy() as data:
        data['name'] = message.text
        some_data = {}
        try:
            for i in menu_data:
                print(data['name'])
                if i[2] == 'sushi' and i[0] == data['name']:
                    some_data['id'] = rolls.maxID('delivery.db') + 1
                    some_data['photo'] = i[1]
                    some_data['username'] = user_data[0]
                    some_data['userpass'] = user_data[1]
                    some_data['user_adress'] = data['adress']
                    some_data['name'] = data['name']
                    some_data['price'] = i[2]
                    some_data['ingridients'] = i[3]
            rolls.addNewRoll([some_data['id'],some_data['photo'],some_data['username'],some_data['userpass'],some_data['user_adress'],some_data['name'],some_data['price'],some_data['ingridients']],'delivery.db')
            await message.reply('Заказ произведён успешно')
        except:
            await message.reply('Роллов с таким названием не существует',reply_markup=kb_main)
        finally:
            await state.finish()



def register_message_handlers_rolls(dp: Dispatcher):
    dp.register_message_handler(cancel,Text(equals='Назад',ignore_case=True),state='*')
    dp.register_callback_query_handler(roll_order_start,text = 'Ordered roll',state=None)
    dp.register_message_handler(roll_order_adress,state=oth.roll_order.adress)
    dp.register_message_handler(roll_order_name,state=oth.roll_order.name)
