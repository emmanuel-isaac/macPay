from macPay.settings.base import SKILLTREE_API_URL, X_AUTH_TOKEN

import requests
import json

from apps.macpayuser.models import Fellow


# Method to check if word is present in string
def check_in_string(word, string):
    if word in string:
        return True
    else:
        return False


class SkillTree():
    def __init__(self):
        self.url = SKILLTREE_API_URL
        self.headers = {'X-AUTH-TOKEN': X_AUTH_TOKEN}

    def get_data(self, params, **kwargs):
        url = self.url
        headers = self.headers

        response = requests.get(url, params=params, headers=headers)
        return response.json()


def get_skilltree_data():
    # Make API request to SkillTree to get the data of all fellows
    skilltree_instance = SkillTree()

    # instantiate params
    params = {'page': 1}
    data = []

    # The API request
    while SkillTree.get_data(skilltree_instance, params):
        response = SkillTree.get_data(skilltree_instance, params)
        data = data + response
        params['page'] += 1
        continue

    return data


def get_fellows_data():
    data = get_skilltree_data()
    fellows = []
    for item in data:
        if item.get('cohort'):
            if check_in_string('Class', item.get('cohort').get('name')):
                fellows.append(item)
                continue
    return fellows


def get_emails(fellows, **kwargs):
    email_list = []
    for fellow in fellows:
        try:
            email_list.append(fellow.email)
            continue
        except AttributeError, e:
            email_list.append(fellow['email'])
            continue
        finally:
            pass
    return email_list


def get_new_emails():
    db_fellows = Fellow.objects.all()
    skilltree_fellows = get_fellows_data()
    db_fellows_emails = get_emails(db_fellows)
    skilltree_fellows_emails = get_emails(skilltree_fellows)
    new_emails = list(set(skilltree_fellows_emails) - set(db_fellows_emails))
    return (new_emails, skilltree_fellows)


def get_new_fellows():
    new_emails, skilltree_fellows = get_new_emails()
    new_fellows = []
    for fellow in skilltree_fellows:
        for email in new_emails:
            if fellow['email'] == email:
                new_fellows.append(fellow)
                continue
            else:
                continue
        continue
    return new_fellows


def sync_new_fellows():
    new_fellows = get_new_fellows()
    for new_fellow in new_fellows:
        fellow = Fellow(first_name=new_fellow['first_name'], last_name=new_fellow['last_name'],
                        email=new_fellow['email'])
        fellow.save()
        continue
    return 'Done'
