from polls.config import ItemType

class ItemsImporter:

    def import(items):
        children = {}
        update_date = None

        def add_item(item_dict):

            type = item_dict['type']
            parent_id = item_dict['parentId']
            if type == ItemType.OFFER.value:
                item = Offer(pk=item_dict['id'])
                item.price = item_dict['price']
            elif type == ItemType.CATEGORY.value:
                try:  # save current parent_category info
                    item = Category.objects.get(pk=item_dict['id'])
                except ObjectDoesNotExist:  # add new parent_category
                    item = Category(pk=item_dict['id'])
            else:
                raise ValueError

            item.name = item_dict['name']
            item.pk = item_dict['id']
            if parent_id is not None:
                item.parent_category = Category.objects.get(pk=parent_id)
            item.update_date = isoparse(update_date)
            print(f'item saved {item_dict}')
            item.commit()

            if item.pk in children:  # children not added yet
                for child in children[item.pk]:
                    add_item(child)
                children[item.pk].clear()

        update_date = batch['updateDate']
        items = batch['items']

        for item in items:
            item['update_date'] = update_date
            parent = item['parentId']
            # print(parent is None)
            if parent is None or parent == 'None' or Category.objects.filter(pk=parent).exists():
                try:
                    add_item(item)
                except:
                    return Response('{"code": 400,"message": "Validation Failed"}', status=400)
            else:  # Parent parent_category does not exist yet
                if parent not in children:
                    children[parent] = []
                children[parent].append(item)

        print(f'items not saved {children}')