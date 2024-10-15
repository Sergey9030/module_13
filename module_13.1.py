import asyncio


bowls = 5
async def start_strongman(name, power):
    print(f'Силач {name} начал соревнования.')
    for b in range(bowls):
        await asyncio.sleep(round(6/power))
        print(f'Силач {name} подня шар №:{b+1}.')
    print(f'Силач {name} закончил соревнования.')

async def start_tournament():
    strongman1 = asyncio.create_task(start_strongman('Юрий Белкин', 1))
    strongman2 = asyncio.create_task(start_strongman('Владимир Калиниченко', 2))
    strongman3 = asyncio.create_task(start_strongman('Михаил Кокляев', 3))
    await strongman1
    await strongman2
    await strongman3
    print('Турнир закончен. Победила дружба.')

asyncio.run(start_tournament())

