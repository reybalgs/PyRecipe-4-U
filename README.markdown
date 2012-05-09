PyRecipe-4-U
============

PyRecipe-4-U is a simple cooking recipe management application. It is a
redesign of a machine project for a college course of mine two years ago from
the time of this writing. The original project was written in C, ran from the
Windows command line only (because it used those Windows-only headers and
libraries), and it was ugly as hell.

This project aims to revitalize the old one by rewriting it in Python and
letting it run under the PySide Qt GUI Framework. It is aimed to be minimal and
cross-platform.

Features planned:
* Exporting and importing recipes through .rcpe files. .rcpe files are just
  text files that are encoded in the JSON format.
* Generate Shopping List - generates a calculated amount of ingredients
  required by a recipe if ever the serving size was manipulated.
* Detailed information on recipes - allows the user to create detailed lists
  of ingredients and instructions as well as pictures for the recipe.
