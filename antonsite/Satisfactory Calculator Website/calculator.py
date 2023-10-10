from pathlib import Path
from RecipeModel import RecipeModel, ItemModel

# pemis
# item_name = input("Input Item Name: ")
# amount = input("Input amount: ")

machines: list[str] = [ "assambler", "blender", "constructor", "foundry", "manufacturer", "packager", "particle_accelerator","refinery", "smelter" ]
defaultResources: list[str] = [ "limestone", "iron_ore", "copper_ore", "caterium_ore", "coal", "raw_quartz", "sulfur", "bauxit", "uranium", "water", "crude_oil", "nitrogen_gas", "uranium_waste" ]

def main() -> None:
    recipes_saved: list[RecipeModel] = import_database()
    found_recipes: list[RecipeModel] = search_for_recipes(recipes_saved, "reinforced_iron_plate")
    chosen_recipe: RecipeModel = choose_from_recipes(found_recipes).print_recipe()
    stack: list[ItemModel] = []
    stack = add_to_stack(stack, chosen_recipe.recipe_inputs)
    while len(stack) > 0:
        current_searched_item: ItemModel = stack[-1].item_name
        stack.pop()
        found_recipes: list[RecipeModel] = search_for_recipes(recipes_saved, current_searched_item)
        chosen_recipe: RecipeModel = choose_from_recipes(found_recipes)
        stack = add_to_stack(stack, chosen_recipe.recipe_inputs)
        print([i.item_name for i in stack])
    print("done")


def add_to_stack(stack: list[ItemModel], items: list[ItemModel]) -> list[ItemModel]:
    items.reverse()
    for item in items:
        if item.item_name in defaultResources:
            continue
        else:
            stack.append(item)

    return stack


def choose_from_recipes(found_recipes: list[RecipeModel]) -> RecipeModel:
    for index, recipe in enumerate(found_recipes):
        print(f"{index + 1}: ", end="")
        recipe.print_recipe()

    chosen_recipe: int = int(input(f"Choose Recipe (1 - {len(found_recipes)}): ")) - 1
    return found_recipes[chosen_recipe]


def sort_recipes_to_normal(recipes: list[RecipeModel]) -> list[RecipeModel]:
    if len(recipes) == 0 or recipes[0].is_alternate_bool == False:
        return recipes
    
    sorted_recipes: list[RecipeModel] = []
    default_recipe_index = 0
    for index, recipe in enumerate(recipes):
        if recipe.is_alternate_bool == False:
            default_recipe_index = index
            break
    
    sorted_recipes.append(recipes[default_recipe_index])

    for index, recipe in enumerate(recipes):
        if index == default_recipe_index:
            continue
        sorted_recipes.append(recipe)

    return sorted_recipes



def search_for_recipes(recipes_saved: list[RecipeModel], searched_output_item: str) -> list[RecipeModel]:
    found_recipes: list[RecipeModel] = []
    for recipe in recipes_saved:
        if recipe.has_output(searched_output_item):
            found_recipes.append(recipe)

    return sort_recipes_to_normal(found_recipes)


def import_database() -> list[RecipeModel]:
    recipes_in_model: list[RecipeModel] = []
    recipe_path: str = Path(__file__).parent / 'recipes'
    for index, machine in enumerate(machines):
        machine_file: str = recipe_path / f'{machine}.txt'
        with open(machine_file) as f:
            lines: list[str] = f.readlines()
            for line in lines:
                recipes_in_model.append(RecipeModel(line, machine, int(index)))

                # spliters = line.split(", ")
                # input_count = int(spliters[0])
                # output_count = int(spliters[1])
                # normal_recipe = is_normal_recipe(spliters[-1])

                # for i in range(0, input_count * 2, 2):
                #     item = spliters[i + 3]
                #     amount = spliters[i + 4]

                # for i in range(0, output_count * 2, 2):
                #     item = spliters[i + (2 * input_count) + 4]
                #     amount = spliters[i + (2 * input_count) + 5]
    return recipes_in_model


main()
