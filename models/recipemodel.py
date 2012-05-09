###############################################################################
#
# recipemodel.py
#
# Provides the class model for a recipe. The class model is passed around in
# the application proper, and it is from and to them that the .rcpe files are
# decoded and encoded.
#
###############################################################################

class RecipeModel():
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
