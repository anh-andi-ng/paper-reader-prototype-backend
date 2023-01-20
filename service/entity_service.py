

class EntityService:
    def __init__(self, keyword, db):
        self.keyword = keyword
        self.db = db

    def original(self):
        ent_ref = self.db.collection(u'entities').document(self.keyword).get()

        if ent_ref.exists:
            ent_dict = ent_ref.to_dict()
            max_level = 10 - sum(x == None for x in ent_dict.values())
            child_ent = list(self.db.collection(u'entities').where(
                u'level_' + str(max_level), u'==', self.keyword).stream())

            doc_list = [doc.to_dict() for doc in child_ent]
            return doc_list
        else:
            return {
                "message": u'No such document!'
            }

    def format_father(self, result, max_level):
        i = 1
        data = {}
        temp = {}
        while i <= max_level:
            if i == 1:
                temp = [{
                    'text': result['level_{}'.format(i)],
                    'id': i,
                    'isClickable': False,
                    'parentID': 'root',
                    'isExpanding': False
                }]
                data['root'] = temp
            else:
                temp = [{
                    'text': result['level_{}'.format(i)],
                    'id': i,
                    'isClickable': False,
                    'parentID': i - 1,
                    'isExpanding': False
                }]
                data["{}".format(i - 1)] = temp
            i += 1
        return data

    def format_child(self, result, max_level):
        i = 0
        data = []
        obj = {}
        child_obj = {}
        res = {}
        while i < len(result):
            level = max_level + 1 + i
            temp = {
                'text': result[i]['level_{}'.format(max_level+1)],
                'id': level,
                'isClickable': True,
                'parentID': max_level,
                'isExpanding': False
            }

            if result[i]['level_{}'.format(max_level+1)] in obj:
                if result[i]['level_{}'.format(max_level+2)]:
                    temp_child_obj = {
                        'text': result[i]['level_{}'.format(max_level+2)],
                        'id': level,
                        'isClickable': True,
                        'parentID': obj.get(result[i]['level_{}'.format(max_level+1)]),
                        'isExpanding': True
                    }
                    child_obj.update(
                        {obj.get(result[i]['level_{}'.format(max_level+1)]): [temp_child_obj]})
            else:
                if result[i]['level_{}'.format(max_level+2)]:
                    temp_child_obj = {
                        'text': result[i]['level_{}'.format(max_level+2)],
                        'id': level,
                        'isClickable': True,
                        'parentID': obj.get(result[i]['level_{}'.format(max_level+1)]),
                        'isExpanding': True
                    }
                    child_obj.update(
                        {obj.get(result[i]['level_{}'.format(max_level+1)]): [temp_child_obj]})
                obj[result[i]['level_{}'.format(
                    max_level+1)]] = level
                data.append(temp)
            i += 1
        res.update({"{}".format(max_level): data})
        res.update(child_obj)
        return res

    def find(self, keyword=None):
        keyword = self.keyword

        # keyword is empty
        if keyword == '':
            return {
                "message": u'Search term should not be empty!',
            }
        ent_ref = self.db.collection(u'entities').document(keyword).get()

        if ent_ref.exists:
            ent_dict = ent_ref.to_dict()
            max_level = 10 - sum(x == None for x in ent_dict.values())
            child_ent = list(self.db.collection(u'entities').where(
                u'level_' + str(max_level), u'==', keyword).stream())

            if len(child_ent) < 2:
                return {
                    "message": "The clicked entity is at the last level of the tree. Please go back!"
                }

            doc_list = [doc.to_dict() for doc in child_ent if doc.to_dict()[
                'level_'+str(max_level+1)]]
            data = self.format_father(doc_list[0], max_level)
            data.update(self.format_child(
                doc_list, max_level))
            return {
                "message": data
            }
        else:
            return {
                "message": u'No entity exists!',
            }
