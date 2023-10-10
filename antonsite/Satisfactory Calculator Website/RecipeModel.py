def make_string_readable(item_name: str):
    return item_name.replace('_', ' ').title()


class ItemModel:
    def __init__(self, item_name: str, amount: float):
        self.item_name: str = item_name
        self.item_name_readable: str = make_string_readable(item_name)
        self.amount: float = amount

class RecipeModel(list):
    def __init__(self, recipe_in_string: str, machine: str, machine_index: int):
        self.machine_index: int = machine_index
        self.name_of_machine: str = machine
        self.name_of_machine_readable: str = make_string_readable(machine)

        self._recipe_array = recipe_in_string.split(", ")
        self.number_of_inputs: int = int(self._recipe_array[0])
        self.number_of_outputs: int = int(self._recipe_array[1])

        self.recipe_inputs: list[ItemModel] = []
        for i in range(0, self.number_of_inputs * 2, 2):
            item: str = self._recipe_array[i + 3]
            amount: float  = float(self._recipe_array[i + 4])
            self.recipe_inputs.append(ItemModel(item, amount))

        self.recipe_outputs: list[ItemModel] = []
        for i in range(0, self.number_of_outputs * 2, 2):
            item: str = self._recipe_array[i + 2 * self.number_of_inputs + 4]
            amount: float = float(self._recipe_array[i + 2 * self.number_of_inputs + 5])
            self.recipe_outputs.append(ItemModel(item, amount))
        
        self.__save_alternate_status(self._recipe_array)


    def has_output(self, searched_item) -> bool:
        for i, output in enumerate(self.recipe_outputs):
            if output.item_name == searched_item:
                self.desired_ouput_index: int = i
                self.desired_output_item_name: str = output.item_name
                self.desired_output_item_name_readable: str = output.item_name_readable
                return True
        return False



    def __save_alternate_status(self, recipe_array) -> None:
        if recipe_array[-1][0] == "n":
            self.is_alternate_bool: bool = False
            self.is_alternate_char = 'n'
        elif recipe_array[-1][0] == "a":
            self.is_alternate_bool: bool = True
            self.is_alternate_char = 'a'
        else:
            raise Exception("Recipe Alternate Error")
        

    def print_recipe(self):
        print(f"Machine: {self.name_of_machine_readable}, Inputs: {[(i.item_name_readable, i.amount) for i in self.recipe_inputs]}, Outputs: {[(o.item_name_readable, o.amount) for o in self.recipe_outputs]}, Alternate: {self.is_alternate_bool}")
        return self
