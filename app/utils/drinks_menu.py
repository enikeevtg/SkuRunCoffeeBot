import asyncio
from typing import Dict, List
from database import requests as rq


# async def create_drinks_menu() -> Dict[str, List[str]]:
#     drinks = dict({})
#     categories = await rq.get_categories()
#     for category in categories:
#         key = f'category_{category.id}_{category.name}'
#         items = await rq.get_category_items(category.id)
#         values = []
#         for item in items:
#             values.append(f'item_{item.id}_{item.name}')
#         drinks[key] = values
#     return drinks


async def create_drinks_menu() -> Dict[str, List[str]]:
    print('create_drinks_menu')
    drinks: Dict[str, List[str]] = dict({})
    categories_names = dict({})
    categories = await rq.get_categories()
    for category in categories:
        drinks[f'category_{category.id}_{category.name}'] = []
        categories_names[category.id] = category.name
    items = await rq.get_all_items()
    for item in items:
        category_name = categories_names[item.category_id]
        drinks[f'category_{item.category_id}_{category_name}'].append(
            f'item_{item.id}_{item.name}')

    return drinks


if __name__ == '__main__':
    drinks = asyncio.run(create_drinks_menu())
    for k, v in drinks.items():
        print(k, '\n\t', v)
