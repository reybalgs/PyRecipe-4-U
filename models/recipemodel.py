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
    def export_recipe(self):
        """
        This function exports the current recipe object as a JSON-encoded
        recipe (.rcpe) file.

        Actually just returns a JSON-encoded string
        """
        # Dump the object into a JSON-formatted string
        json_recipe = json.dumps({"name":self.name,"course":self.course, 
            "serving_size":self.servingSize,"ingredients":self.ingredients,
            "instructions":self.instructions}, separators=(',',':'))

        # Return the string
        return json_recipe

    def import_recipe(self, raw_json):
        """
        Parses a JSON-encoded .rcpe file and then sets it to itself.
        The string containing the [contents] of the JSON file is passed into
        this function.
        """
        # Put the decoded JSON string into a "raw" recipe object 
        raw_recipe = json.loads(raw_json)

        print raw_recipe # print it for now

        self.name = raw_recipe['name']
        self.course = raw_recipe['course']
        self.servingSize = raw_recipe['serving_size']
        self.ingredients = raw_recipe['ingredients']
        self.instructions = raw_recipe['instructions']

    def print_recipe_information(self):
        """
        A useful debugging function that prints the entirety of the recipe
        """
        # Print basic information
        print '\nName: ' + self.name
        print 'Course: ' + self.course
        print 'Serving Size: ' + str(self.servingSize)
        
        # Print the ingredients
        print '\nIngredients:'
        if len(self.ingredients) == 0:
            print 'No ingredients.'
        else:
            for ingredient in self.ingredients:
                print(ingredient['name'] + str(ingredient['quantity']) +
                    ingredient['unit'])

        # Print the instructions
        print '\nInstructions:'
        if len(self.instructions) == 0:
            print 'No instructions.'
        else:
            for instruction in self.instructions:
                print instruction

        # Print the filepaths of the images
        print '\nImage paths:'
        if len(self.images) == 0:
            print 'No images.'
        else:
            for filePath in self.images:
                print filePath

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
        self.images = []
