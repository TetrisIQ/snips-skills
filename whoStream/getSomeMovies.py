from justwatch import JustWatch

if __name__ == '__main__':
    just_watch = JustWatch()
    results_by_multiple = just_watch.search_for_item(
        page=1,
        page_size=1000,
        #page_size=10,
        providers=['nfx'],
        content_types=['show'],
        monetization_types=['flatrate'],
    )
    s = set()
    for i in range(0,len(results_by_multiple['items'])):
        try:
            s.add(results_by_multiple['items'][i]['title'])
        except KeyError:
            pass
    results_by_multiple = just_watch.search_for_item(
        page=1,
        page_size=1000,
        # page_size=10,
        providers=['amp'],
        content_types=['show'],
        monetization_types=['flatrate'],
    )
    for i in range(0,len(results_by_multiple['items'])):
        s.add(results_by_multiple['items'][i]['title'])

    for st in s:
        print(st)
