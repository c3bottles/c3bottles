from flask_babel import lazy_gettext

from c3bottles.model import drop_point


class Category:
    """
    A category of drop points for different stuff, e.g. bottles, trash, etc.

    Different categories of drop points allow different teams or specialized
    groups within the same team to organize their work through the same
    frontend. Therefore, each drop point belongs to one category.
    """

    def __init__(self, category_id, name):
        self.category_id = category_id
        self.name = name
        self.metrics_name = str(name)

    def __str__(self):
        return str(self.name)

    def __len__(self):
        return drop_point.DropPoint.query.filter(
            drop_point.DropPoint.category_id == self.category_id,
            # noqa - pep wants is None, sqlAlchemy wants == None
            drop_point.DropPoint.removed == None
        ).count()

    @staticmethod
    def get(category_id):
        if category_id in all_categories:
            return all_categories.get(category_id)
        else:
            return all_categories.get(0)


"""
A dict of all categories.

The categories must be indexed by their integer id and their name should be a
lazy string so that l10n becomes easy. The ids kan be any integer but at least
the category with the id 0 must be present as it is the default fallback
category. If that one is not present, everything will fall apart.
"""
all_categories = {
    0: Category(0, lazy_gettext("Bottle Drop Point")),
    1: Category(1, lazy_gettext("Trashcan")),
}


def categories_sorted():
    """
    Get a list of all categories sorted by their human-readable name with
    respect to the user's language.

    :return: A list of all categories sorted by name.
    """
    return sorted(all_categories.values(), key=lambda i: str(i))
