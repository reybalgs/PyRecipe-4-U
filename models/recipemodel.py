###############################################################################
#
# recipemodel.py
#
# Provides the class model for a recipe. The class model is passed around in
# the application proper, and it is from and to them that the .rcpe files are
# decoded and encoded.
#
###############################################################################

import simplejson as json

class RecipeModel():
    def export(self):
        """
        This function exports the current recipe object as a JSON-encoded
        recipe (.rcpe) file.

        Actually just returns a JSON-encoded string
        """
        # Dump the object into a JSON-formatted string
        json_recipe = json.dumps({"recipe": [{"name": self.name}, {"course": self.course}, 
            {"serving_size": self.servingSize}, {"ingredients": self.ingredients},
            {"instructions": self.instructions}]})

        # Return the string
        return json_recipe


    def import(self, raw_json):
        """
        Parses a JSON-encoded .rcpe file and then sets it to itself.
        The string containing the [contents] of the JSON file is passed into
        this function.
        """
        recipe = RecipeModel() # create a temporary recipe

        # Put the decoded JSON string into a "raw" recipe object 
        raw_recipe = json.loads(raw_json)

        print raw_recipe # print it for now
        # TODO Add the data of the raw recipe into the actual recipe

    def get_recipe(self, recipe):
        """
        Assigns a given recipe to this recipe.
        """
        self.name = recipe.name
        self.course = recipe.course
        self.servingSize = recipe.servingSize
        self.ingredients = recipe.ingredients
        self.instructions = recipe.instructions

    def __init__(self):
        self.name = 'noname'
        self.course = 'none'
        self.servingSize = 0
        self.ingredients = []
        self.instructions = []
