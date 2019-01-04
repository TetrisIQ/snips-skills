from justwatch import JustWatch


def id_to_name(id):
    if (id == 8):
        return "Netflix"
    if (id == 9):
        return "Amazon Prime Video"
    return str(id)


if __name__ == '__main__':
    jw = JustWatch(country='DE')
    r = jw.search_for_item(query='hangover')
    set = set()
    try:
        for i in range(0,len(r)):
            for j in range(0,len(r['items'][i]['offers'])):
                if r['items'][i]['offers'][j]['monetization_type'].__contains__('flatrate'):
                    titel = r['items'][i]['title']
                    provider_id = r['items'][i]['offers'][j]['provider_id']
                    set.add("{} kann auf {} kostenlos angesehen werden".format(titel,id_to_name(provider_id)))
    except KeyError:
        pass
    print(set)

    
