from django.core import serializers
from reposite.models import *
from discussions.models import *


def serialize_data_from_backup(origin_id=14):
    # Generate the json files for prototypes and dependencies.

    prototypes = ProjectPrototype.objects.filter(origin__id=origin_id)
    with open("prototypes.json", "w") as out:
        serializers.serialize("json", prototypes, stream=out)

    with open("prototype_elements.json", "w") as out:
        serializers.serialize("json", PrototypeMetaElement.objects.filter(prototype_project__origin__id=origin_id), stream=out)

    with open("prototype_tasks.json", "w") as out:
        serializers.serialize("json", ProjectTask.objects.filter(prototype_project__origin__id=origin_id), stream=out)

    with open("prototype_files.json", "w") as out:
        serializers.serialize("json", ProjectFile.objects.filter(project__origin__id=origin_id), stream=out)

    with open("posts.json", "w") as out:
        serializers.serialize("json", Post.objects.all(), stream=out)

    with open("prototype_comments.json", "w") as out:
        serializers.serialize("json", ProjectComment.objects.filter(project__origin__id=origin_id), stream=out)


def deserialize_data_from_files():
    # Open the json file for reading, deserialize, and save each to db.
    with open("prototypes.json", "r") as inputfile:
        data = serializers.deserialize("json", inputfile.read())
        for d in data:
            d.object.origin = None
            d.save()

    with open("prototype_elements.json", "r") as inputfile:
        data = serializers.deserialize("json", inputfile.read())
        for d in data:
            d.save()

    with open("prototype_tasks.json", "r") as inputfile:
        data = serializers.deserialize("json", inputfile.read())
        for d in data:
            d.save()

    with open("prototype_files.json", "r") as inputfile:
        data = serializers.deserialize("json", inputfile.read())
        for d in data:
            d.save()

    with open("posts.json", "r") as inputfile:
        data = serializers.deserialize("json", inputfile.read())
        for d in data:
            d.save()

    with open("prototype_comments.json", "r") as inputfile:
        data = serializers.deserialize("json", inputfile.read())
        for d in data:
            d.save()

