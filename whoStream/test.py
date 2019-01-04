from justwatch import JustWatch
my_conf = ['Netflix', 'Amazon Prime Video']


def id_to_name(id):
    if (id == 8):
        return "Netflix"
    if (id == 10):
        return "Amazon Prime Video"
    if (id==28):
        return "netzkino.de"
    if (id==171):
        return "Watchbox"
    return str(id)


def main():
    test =['nbhjbh Netflix', "hsadkjhj Amazon Prime "]
    for s in test:
        for k in my_conf:
            if s.__contains__(k):
                print("kkjh")

def get_best_provider():
    conf = "8,10"
    ret = []
    for st in str(conf).split(','):
        ret.append(id_to_name(int(st)))
    return ret



if __name__ == '__main__':
    main()
    jw = JustWatch(country='DE')
    r = jw.search_for_item(query='matrix')
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

    
