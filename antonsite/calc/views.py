from typing import Any
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from . import models
from decimal import Decimal
from django.urls import reverse_lazy
import json

defaultResources: list[str] = [ "limestone", "iron_ore", "copper_ore", "caterium_ore", "coal", "raw_quartz", "sulfur", "bauxit", "uranium", "water", "crude_oil", "nitrogen_gas", "uranium_waste" ]


class ItemView(generic.ListView):
    model = models.ItemModel
    template_name = "index.html"
    paginate_by = 16

    def get_queryset(self):
        category = self.request.GET.get("category")
        qs = models.ItemModel.objects.filter(category="Ingots")
        if category:
            qs = models.ItemModel.objects.filter(category=category)
        return qs.order_by("item_name")

    def post(self, request, *args, **kwargs):
        item_query = self.request.POST.get("item_name")
        amount_query = self.request.POST.get("amount_query")
        self.request.session['item_query'] = item_query
        self.request.session['amount_query'] = amount_query
        self.request.session['stack'] = []
        return redirect("query_set")
    

class StackObject:
    def __init__(self, name: str, amount: float, diagram_tree_output: str = "", diagram_tree_depth: str = "", first: bool = False, last: bool = False) -> None:
        self.item_name: str = name
        self.item_name_readable: str = self.make_string_readable(name)
        self.needed_item_amount: float = amount
        self.diagram_tree_output: str = diagram_tree_output
        self.diagram_tree_depth: str = diagram_tree_depth
        self.first_object: bool = first
        self.last_object: bool = last

    def make_string_readable(self, item_name: str):
        return item_name.replace('_', ' ').title()
    

class RecipeView(generic.ListView):
    model = models.RecipeModel
    template_name = "detail_view.html"
    #stack = []

    def get_queryset(self):
        recipe_id = self.request.GET.get("recipe_id")
        recipe_inputs: models.InputModel = models.InputModel.objects.filter(recipe=recipe_id)
        self.stack = []
        self.stack = self.session_dict_to_stack(self.request.session.get('stack'))
        if self.stack == []:
            self.request.session['all_needed_machines']: dict[str, float] = {}
            self.request.session['all_needed_recipes_in_machines']: dict[str, float] = {}
            self.request.session['needed_default_resources']: dict[str, float] = {}
            self.request.session['factory_in_diagram']: dict[str, float] = {}
            initial_recipe = True
            item_query = self.request.session.get('item_query')
            amount_query = float(self.request.session.get('amount_query'))
            current_searched_item = StackObject(item_query, amount_query)
            self.request.session.modified = True
        else:
            initial_recipe = False
            current_searched_item: StackObject = self.stack[-1]
            item_query = current_searched_item.item_name
            amount_query = current_searched_item.needed_item_amount
            self.stack.pop()
        if recipe_id:
            output_amount: float = self.get_desired_output(item_query, recipe_id).amount
            needed_machines = float(amount_query) / float(output_amount)
            self.stack = self.add_to_stack(recipe_inputs, current_searched_item, needed_machines)
            print(json.dumps(self.request.session.get('stack'), indent=4))
            chosen_recipe: models.RecipeModel = models.RecipeModel.objects.filter(pk=recipe_id)[0]
            self.save_current_factory_status(current_searched_item, chosen_recipe, needed_machines, item_query, output_amount, initial_recipe)
            if len(self.stack) == 0:
                return None
            print(json.dumps(self.stack_to_session_dict(self.stack), indent=4))
            self.request.session['stack'] = self.stack_to_session_dict(self.stack)
            return models.RecipeModel.objects.filter(recipe_output_items__item_name=self.stack[-1].item_name).order_by('-normal_recipe')
        return models.RecipeModel.objects.filter(recipe_output_items__item_name=item_query).order_by('-normal_recipe')

    def render_to_response(self, context):
        recipe_id = self.request.GET.get("recipe_id")
        if recipe_id:
            if len(self.stack) == 0:
                return redirect('result')
        return super().render_to_response(context)
    
    def save_current_factory_status(self, searched_item: StackObject, chosen_recipe: models.RecipeModel, needed_machines, item_query: str, output_ampunt: float, initial_recipe: bool) -> None:

        self.request.session['all_needed_machines']: dict[str, float] = self.add_or_save_to_dict(self.request.session.get('all_needed_machines'), chosen_recipe.machine.machine_name_readable, float(needed_machines))
        if initial_recipe:
            self.request.session['all_needed_recipes_in_machines']: dict[str, float] = self.add_or_save_to_dict(self.request.session.get('all_needed_recipes_in_machines'), f"{chosen_recipe.machine.machine_name_readable} for {self.make_string_readable(item_query)}", float(needed_machines))
            self.request.session['factory_in_diagram']: dict[str, float] = self.add_or_save_to_dict(self.request.session.get('factory_in_diagram'), f"{self.make_string_readable(item_query)} in {float(needed_machines)} {chosen_recipe.machine.machine_name_readable}", float(needed_machines * output_ampunt))
        else:
            self.request.session['all_needed_recipes_in_machines']: dict[str, float] = self.add_or_save_to_dict(self.request.session.get('all_needed_recipes_in_machines'), f"{chosen_recipe.machine.machine_name_readable} for {searched_item.item_name_readable}", float(needed_machines))
            self.request.session['factory_in_diagram']: dict[str, float] = self.add_or_save_to_dict(self.request.session.get('factory_in_diagram'), f"{searched_item.diagram_tree_output}{searched_item.item_name_readable} in {float(needed_machines)} {chosen_recipe.machine.machine_name_readable}", float(needed_machines * output_ampunt))
        self.request.session.modified = True
        
    def add_to_stack(self, recipe_inputs: list[models.InputModel], last_searched_object: StackObject, needed_machines: float):
        for index, item in enumerate(recipe_inputs):
            tree_depth: str = last_searched_object.diagram_tree_depth
            tree_output: str = tree_depth
            if item.item_name in defaultResources:
                self.request.session['needed_default_resources']: dict[str, float] = self.add_or_save_to_dict(self.request.session.get('needed_default_resources'), item.item_name_readable, float(item.amount * needed_machines))
                continue
            else:
                if index == 0:
                    last_object: bool = True
                    tree_output += "└──"
                    tree_depth += "&nbsp;&nbsp;&nbsp;"
                else:
                    last_object: bool = False
                    tree_output += "├──"
                    tree_depth += "│&nbsp;&nbsp;"
                self.stack.append(StackObject(item.item_name, needed_machines * item.amount, diagram_tree_output=tree_output, diagram_tree_depth=tree_depth, last=last_object))
        return self.stack

    def add_or_save_to_dict(self, dictionary: dict[str, float], key: str, value: str) -> dict[str, float]:
        if dictionary.get(key) == None:
            dictionary[key] = value
            return dictionary
        dictionary[key] += value
        return dictionary
    
    def get_desired_output(self, searched_output_item: str, chosen_recipe_id) -> models.OutputModel:
        recipe_outputs: list[models.OutputModel] = models.OutputModel.objects.filter(recipe=chosen_recipe_id)
        for output in recipe_outputs:
            if output.item_name == searched_output_item:
                return output
        raise RuntimeError("Failed to find desired output item")
    
    def make_string_readable(self, item_name: str):
        return item_name.replace('_', ' ').title()

    def session_dict_to_stack(self, session_dict: dict[int, dict[str, str]]) -> list[StackObject]:
        stack: list[StackObject] = []
        for index in range(len(session_dict)):
            index = str(index)
            stack.append(StackObject(
                name=session_dict[index]["item_name"],
                amount=float(session_dict[index]["needed_item_amount"]),
                diagram_tree_output=session_dict[index]["diagram_tree_output"],
                diagram_tree_depth=session_dict[index]["diagram_tree_depth"],
                first=session_dict[index]["first_object"],
                last=session_dict[index]["last_object"]
            ))
        return stack
    
    def stack_to_session_dict(self, stack: list[StackObject]) -> dict[int, dict[str, str]]:
        session_dict: dict[int, dict[str, str]] = {}
        for index, stack_object in enumerate(stack):
            session_dict[index] = {
                "item_name": stack_object.item_name,
                "item_name_readable": stack_object.item_name_readable,
                "needed_item_amount": float(stack_object.needed_item_amount), # Value type needs to be changed from Decimal to float everywhere
                "diagram_tree_output": stack_object.diagram_tree_output,
                "diagram_tree_depth": stack_object.diagram_tree_depth,
                "first_object": stack_object.first_object,
                "last_object": stack_object.last_object,
            }
        return session_dict
    

class ResultView(generic.TemplateView):
    template_name = "result_view.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.print_dict(self.request.session.get('all_needed_machines'))
        self.print_dict(self.request.session.get('all_needed_recipes_in_machines'))
        self.print_dict(self.request.session.get('needed_default_resources'))
        self.print_dict(self.request.session.get('factory_in_diagram'))
        context["all_needed_machines"] = self.request.session.get('all_needed_machines')
        context["all_needed_recipes_in_machines"] = self.request.session.get('all_needed_recipes_in_machines')
        context["needed_default_resources"] = self.request.session.get('needed_default_resources')
        context["factory_in_diagram"] = self.request.session.get('factory_in_diagram')
        return context

    def print_dict(self, dictionary: dict[str, float]):
        for k, v in dictionary.items():
            print(k.replace('&nbsp;',' '), v)
        print()
